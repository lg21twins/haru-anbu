# review-loop.lib.sh — helpers for review-loop.sh
# bash 3.2 compatible. Sourced, not executed.

#---------------------------------------------------------------------- log/die
log() { printf '[review-loop] %s\n' "$*" >&2; }

die() {
  local msg=$1
  local code=${2:-1}
  local tag=${3:-}
  printf '[review-loop] ERROR: %s\n' "$msg" >&2
  if [ -n "${LOOP_DIR:-}" ] && [ -f "${LOOP_DIR:-}/meta.json" ]; then
    set_meta_field ".status" '"done"' || true
    set_meta_field ".result" "$(jq -Rn --arg v "${tag:-FAIL}" '$v')" || true
  fi
  exit "$code"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing command: $1" 1
}

#---------------------------------------------------------------------- locks/signals
acquire_lock_or_die() {
  local lock=$1 name=$2
  if mkdir "$lock" 2>/dev/null; then
    printf '%s\n%s\n' "$$" "$name" > "$lock/info"
    LOCK_DIR="$lock"
    return 0
  fi
  local who="(unknown)"
  [ -f "$lock/info" ] && who=$(tr '\n' ' ' < "$lock/info")
  die "another loop is running: $who. Remove $lock if stale." 7
}

release_lock() {
  local lock=$1
  [ -d "$lock" ] && rm -rf "$lock" || true
}

on_exit() {
  [ -n "${LOCK_DIR:-}" ] && release_lock "$LOCK_DIR" || true
}

on_signal() {
  log "interrupted"
  if [ -n "${LOOP_DIR:-}" ] && [ -f "${LOOP_DIR:-}/meta.json" ]; then
    set_meta_field ".status" '"interrupted"' || true
  fi
  exit 130
}

#---------------------------------------------------------------------- naming
unique_loop_name() {
  local root=$1 date=$2 name=$3
  local base="${date}_${name}"
  local candidate="$base"
  local n=2
  while [ -e "$root/$candidate" ]; do
    candidate="${base}_${n}"
    n=$((n+1))
  done
  printf '%s' "$candidate"
}

#---------------------------------------------------------------------- worktree
ensure_clean_tree() {
  local repo=$1
  if [ -n "$(git -C "$repo" status --porcelain)" ]; then
    die "working tree is not clean (use default --worktree mode, or commit/stash first)" 6
  fi
}

#---------------------------------------------------------------------- meta.json
init_meta() {
  local f=$1
  local ts; ts=$(iso_now)
  jq -n \
    --arg loop "$LOOP_NAME" \
    --arg started "$ts" \
    --arg base "$BASELINE_REF" \
    --arg wt "$WORKDIR" \
    --arg br "$BRANCH" \
    --arg cm "$CLAUDE_MODEL" \
    --arg xm "$CODEX_MODEL" \
    --arg ce "$CODEX_EFFORT" \
    --argjson rounds "$ROUNDS" \
    --arg budget "$BUDGET" \
    --arg verify "$VERIFY" \
    '{
      loop:$loop, status:"init", round:0, max_rounds:$rounds, result:null,
      started_at:$started, ended_at:null,
      baseline_ref:$base, worktree:$wt, branch:$br,
      models:{claude:$cm, codex:(if $xm=="" then null else $xm end), codex_effort:$ce},
      budget_usd:($budget|tonumber),
      verify:{mode:$verify, passed:null, checks:[]},
      history:[]
    }' > "$f"
}

set_meta_field() {
  local path=$1 value=$2
  local f="${LOOP_DIR}/meta.json"
  [ -f "$f" ] || return 0
  local tmp; tmp=$(mktemp)
  jq "$path = $value" "$f" > "$tmp" && mv "$tmp" "$f"
}

set_meta_status() {
  local status=$1 round=$2
  local ts; ts=$(iso_now)
  local f="$LOOP_DIR/meta.json"
  local tmp; tmp=$(mktemp)
  jq --arg s "$status" --argjson r "$round" --arg t "$ts" \
     '.status=$s | .round=$r | (.history += [{step:$s, round:$r, at:$t}])' \
     "$f" > "$tmp" && mv "$tmp" "$f"
}

iso_now() { date +%Y-%m-%dT%H:%M:%S%z; }

#---------------------------------------------------------------------- request parsing
write_request_with_body() {
  local f=$1 body=$2
  # If body already contains a structured Allowed files section, write as-is.
  if printf '%s' "$body" | grep -q '^## Allowed files'; then
    printf '%s\n' "$body" > "$f"
    return 0
  fi
  cat > "$f" <<EOF
# 작업 요청

## Allowed files

<!-- 인자로 전달된 body는 자유 형식이라 allowlist를 자동 추출할 수 없습니다.
     이 섹션을 직접 채우거나, body에 '## Allowed files' 섹션을 포함하세요. -->

## Request

$body

## Done criteria

-
EOF
}

# parse_allowlist: fills global arrays ALLOWED_FILES, ALLOWED_GLOBS
parse_allowlist() {
  local f=$1
  local in_files=0 in_globs=0
  while IFS= read -r line; do
    case "$line" in
      "## Allowed files"*) in_files=1; in_globs=0; continue ;;
      "## Allowed-file globs"*) in_files=0; in_globs=1; continue ;;
      "## "*) in_files=0; in_globs=0; continue ;;
    esac
    if [ $in_files -eq 1 ] || [ $in_globs -eq 1 ]; then
      case "$line" in
        "- "*)
          local item="${line#- }"
          item="$(printf '%s' "$item" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"
          [ -n "$item" ] || continue
          [ "$item" = "<!-- 정확한 경로. 한 줄에 하나씩. 비어있으면 abort. -->" ] && continue
          if [ $in_files -eq 1 ]; then ALLOWED_FILES+=("$item"); else ALLOWED_GLOBS+=("$item"); fi
          ;;
      esac
    fi
  done < "$f"
}

#---------------------------------------------------------------------- scope enforcement
# is_allowed_path <path> -- <files...> -- <globs...>
is_allowed_path() {
  local p=$1
  shift
  # forbidden first (cannot be overridden)
  case "$p" in
    .env|.env.*|*/.env|*/.env.*) return 1 ;;
    secrets/*|*/secrets/*) return 1 ;;
    package.json|package-lock.json|yarn.lock|*/package.json|*/package-lock.json|*/yarn.lock) return 1 ;;
  esac
  local mode="files"
  while [ $# -gt 0 ]; do
    if [ "$1" = "--" ]; then mode="globs"; shift; continue; fi
    if [ "$mode" = "files" ]; then
      [ "$p" = "$1" ] && return 0
    else
      case "$p" in
        $1) return 0 ;;
      esac
    fi
    shift
  done
  return 1
}

# enforce_scope <workdir> <baseline> <files...> -- <globs...>
enforce_scope() {
  local workdir=$1 base=$2; shift 2
  # collect tracked-changed and untracked files
  local violators=()
  local f
  # tracked vs baseline
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if ! is_allowed_path "$f" "$@"; then violators+=("$f"); fi
  done < <(git -C "$workdir" -c core.quotepath=false diff --name-only "$base"...HEAD 2>/dev/null; git -C "$workdir" -c core.quotepath=false diff --name-only 2>/dev/null)
  # untracked
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    if ! is_allowed_path "$f" "$@"; then violators+=("$f"); fi
  done < <(git -C "$workdir" -c core.quotepath=false ls-files --others --exclude-standard 2>/dev/null)

  if [ ${#violators[@]} -gt 0 ]; then
    log "scope violations:"
    local v
    for v in "${violators[@]}"; do log "  - $v"; done
    die "scope violation" 3 FAIL_SCOPE_VIOLATION
  fi
}

#---------------------------------------------------------------------- diff.patch
refresh_diff_patch() {
  local workdir=$1 base=$2 out=$3; shift 3
  if [ $# -eq 0 ]; then
    git -C "$workdir" -c core.quotepath=false diff "$base" > "$out" || true
  else
    git -C "$workdir" -c core.quotepath=false add -N -- "$@" 2>/dev/null || true
    git -C "$workdir" -c core.quotepath=false diff "$base" -- "$@" > "$out" || true
  fi
}

#---------------------------------------------------------------------- verdict
read_verdict() {
  local f=$1
  [ -f "$f" ] || die "verdict file missing: $f" 6 BAD_VERDICT
  jq -e -r '
    if (.actor == "codex")
       and (.step == "review" or .step == "final")
       and (.verdict | IN("PASS","PASS_WITH_NOTES","FAIL","ESCALATED"))
    then .verdict
    else error("invalid verdict json")
    end
  ' "$f" 2>/dev/null || die "invalid verdict json: $f" 6 BAD_VERDICT
}

# extract last fenced JSON block from a markdown file
extract_last_json_block() {
  local md=$1 out=$2
  awk '
    BEGIN { inblock=0; saved="" }
    /^```json[[:space:]]*$/ { inblock=1; buf=""; next }
    /^```[[:space:]]*$/ { if (inblock) { saved=buf; inblock=0 }; next }
    { if (inblock) buf = buf $0 "\n" }
    END { printf "%s", saved }
  ' "$md" > "$out"
  [ -s "$out" ] || return 1
  return 0
}

#---------------------------------------------------------------------- LOG.md build
build_log_md() {
  local d=$1
  local f="$d/LOG.md"
  local result; result=$(jq -r '.result // "in-progress"' "$d/meta.json")
  local rounds; rounds=$(jq -r '.round' "$d/meta.json")
  local loop;   loop=$(jq -r '.loop' "$d/meta.json")
  {
    printf '%s\n' '---'
    printf 'loop: %s\n' "$loop"
    printf 'status: %s\n' "$(jq -r '.status' "$d/meta.json")"
    printf 'result: %s\n' "$result"
    printf 'rounds: %s\n' "$rounds"
    printf 'generated_by: review-loop.sh\n'
    printf '%s\n\n' '---'
    printf '# Loop log\n\n'
    local r f h
    for r in "$d"/round-*; do
      [ -d "$r" ] || continue
      for h in claude-work codex-review claude-response codex-final; do
        f="$r/$h.md"
        if [ -f "$f" ]; then
          printf '## %s — %s\n\n' "$(basename "$r")" "$h"
          cat "$f"
          printf '\n\n---\n\n'
        fi
      done
    done
  } > "$f"
}

#---------------------------------------------------------------------- copy back
copy_artifacts_to_main_if_worktree() {
  local workdir=$1 mainrepo=$2 rel=$3
  if [ "$workdir" != "$mainrepo" ]; then
    mkdir -p "$mainrepo/$rel"
    # rsync if available, else cp
    if command -v rsync >/dev/null 2>&1; then
      rsync -a "$workdir/$rel/" "$mainrepo/$rel/"
    else
      cp -R "$workdir/$rel/." "$mainrepo/$rel/"
    fi
  fi
}

#---------------------------------------------------------------------- static verify
static_verify() {
  local workdir=$1; shift
  local files=("$@")
  local ok=1
  [ ${#files[@]} -gt 0 ] || { return 0; }

  # build absolute paths
  local absfiles=()
  local f
  for f in "${files[@]}"; do absfiles+=("$workdir/$f"); done

  if command -v rg >/dev/null 2>&1; then
    local emoji_pcre='[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}\x{2700}-\x{27BF}]'
    if rg --pcre2 -q "$emoji_pcre" -- "${absfiles[@]}" 2>/dev/null; then
      log "static verify: emoji found in allowed files"
      ok=0
    fi
  else
    # python fallback
    if python3 - "${absfiles[@]}" <<'PY'
import re, sys
pat = re.compile(r'[\U0001F300-\U0001FAFF☀-➿]')
hits = 0
for p in sys.argv[1:]:
    try:
        with open(p, 'r', encoding='utf-8') as fh:
            for i, line in enumerate(fh, 1):
                if pat.search(line):
                    print(f'{p}:{i}:{line.rstrip()}')
                    hits += 1
    except FileNotFoundError:
        pass
sys.exit(1 if hits else 0)
PY
    then : ; else
      log "static verify: emoji found in allowed files"
      ok=0
    fi
  fi
  [ $ok -eq 1 ]
}

#---------------------------------------------------------------------- finalize
finalize() {
  local result=$1 loop_dir=$2 loop_rel=$3 workdir=$4 mainrepo=$5 branch=$6 use_wt=$7
  local ts; ts=$(iso_now)
  set_meta_field ".status" '"done"'
  set_meta_field ".result" "$(jq -Rn --arg v "$result" '$v')"
  set_meta_field ".ended_at" "$(jq -Rn --arg v "$ts" '$v')"
  build_log_md "$loop_dir"
  copy_artifacts_to_main_if_worktree "$workdir" "$mainrepo" "$loop_rel"

  # summary
  local notes
  notes=$(collect_recommendations "$loop_dir")
  printf '\n[review-loop] done.\n'
  printf '[review-loop] result:    %s\n' "$result"
  if [ "$use_wt" -eq 1 ]; then
    printf '[review-loop] worktree:  %s\n' "$workdir"
    printf '[review-loop] branch:    %s\n' "$branch"
  fi
  printf '[review-loop] log:       %s\n' "$mainrepo/$loop_rel/LOG.md"
  printf '[review-loop] diff:      %s\n' "$mainrepo/$loop_rel/diff.patch"
  if [ -n "$notes" ]; then
    printf '[review-loop] notes:\n%s\n' "$notes"
  fi
  printf '[review-loop] next:      review the diff and merge by hand. Auto loop never commits.\n'

  case "$result" in
    PASS|PASS_WITH_NOTES) exit 0 ;;
    FAIL|ESCALATED)       exit 2 ;;
    *)                    exit 9 ;;
  esac
}

collect_recommendations() {
  local d=$1
  local r out=""
  for r in "$d"/round-*; do
    [ -d "$r" ] || continue
    for f in "$r/codex-review.json" "$r/codex-final.json"; do
      [ -f "$f" ] || continue
      while IFS= read -r line; do
        out+="  - $line"$'\n'
      done < <(jq -r '.recommendations[]?.issue // empty' "$f" 2>/dev/null)
    done
  done
  printf '%s' "$out"
}
