# review-loop.prompts.sh — AI step invocations
# Sourced by review-loop.sh. Uses helpers from review-loop.lib.sh.

# ---------------- Claude work ----------------
# Args: round, RD, workdir, loop_dir, baseline_ref
step_claude_work() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4 base=$5
  local prompt; prompt=$(_prompt_claude_work "$round" "$RD" "$workdir" "$loop_dir")
  local out="$RD/claude-work.md"
  local stderr_file="$loop_dir/stdio/claude-work-r${round}.stderr"

  ( cd "$workdir" && claude -p \
      --permission-mode acceptEdits \
      --max-budget-usd "$BUDGET" \
      --output-format text \
      --add-dir "$workdir" \
      --model "$CLAUDE_MODEL" \
      --append-system-prompt "$(_compact_guide "$loop_dir")" \
      "$prompt" ) \
    > "$loop_dir/stdio/claude-work-r${round}.stdout" \
    2> "$stderr_file" \
    || die "claude work failed (round $round). see $stderr_file" 4 CLAUDE_FAILED

  [ -f "$RD/claude-work.md" ]   || die "claude did not write claude-work.md" 4 CLAUDE_OUTPUT_MISSING
  [ -f "$RD/claude-work.json" ] || die "claude did not write claude-work.json" 4 CLAUDE_OUTPUT_MISSING
}

# ---------------- Claude respond ----------------
step_claude_respond() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4 base=$5
  local prompt; prompt=$(_prompt_claude_respond "$round" "$RD" "$workdir" "$loop_dir")
  local stderr_file="$loop_dir/stdio/claude-respond-r${round}.stderr"

  ( cd "$workdir" && claude -p \
      --permission-mode acceptEdits \
      --max-budget-usd "$BUDGET" \
      --output-format text \
      --add-dir "$workdir" \
      --model "$CLAUDE_MODEL" \
      --append-system-prompt "$(_compact_guide "$loop_dir")" \
      "$prompt" ) \
    > "$loop_dir/stdio/claude-respond-r${round}.stdout" \
    2> "$stderr_file" \
    || die "claude respond failed (round $round). see $stderr_file" 4 CLAUDE_FAILED

  [ -f "$RD/claude-response.md" ]   || die "claude did not write claude-response.md" 4 CLAUDE_OUTPUT_MISSING
  [ -f "$RD/claude-response.json" ] || die "claude did not write claude-response.json" 4 CLAUDE_OUTPUT_MISSING
}

# ---------------- Codex review (read-only) ----------------
step_codex_review() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4
  local prompt; prompt=$(_prompt_codex_review "$round" "$RD" "$workdir" "$loop_dir")
  local stdout_file="$loop_dir/stdio/codex-review-r${round}.stdout"
  local stderr_file="$loop_dir/stdio/codex-review-r${round}.stderr"
  local last="$RD/codex-review.md"

  local args=(
    -C "$workdir"
    -s read-only
    --ephemeral
    --skip-git-repo-check
    -o "$last"
  )
  [ -n "$CODEX_MODEL" ] && args+=( -m "$CODEX_MODEL" )

  codex exec "${args[@]}" "$prompt" \
    > "$stdout_file" \
    2> "$stderr_file" \
    || die "codex review failed (round $round). see $stderr_file" 5 CODEX_FAILED

  [ -f "$last" ] || die "codex did not produce review markdown" 5 CODEX_OUTPUT_MISSING
  extract_last_json_block "$last" "$RD/codex-review.json" \
    || die "codex review markdown missing trailing JSON block" 6 BAD_VERDICT
}

# ---------------- Codex final (read-only) ----------------
step_codex_final() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4
  local prompt; prompt=$(_prompt_codex_final "$round" "$RD" "$workdir" "$loop_dir")
  local stdout_file="$loop_dir/stdio/codex-final-r${round}.stdout"
  local stderr_file="$loop_dir/stdio/codex-final-r${round}.stderr"
  local last="$RD/codex-final.md"

  local args=(
    -C "$workdir"
    -s read-only
    --ephemeral
    --skip-git-repo-check
    -o "$last"
  )
  [ -n "$CODEX_MODEL" ] && args+=( -m "$CODEX_MODEL" )

  codex exec "${args[@]}" "$prompt" \
    > "$stdout_file" \
    2> "$stderr_file" \
    || die "codex final failed (round $round). see $stderr_file" 5 CODEX_FAILED

  [ -f "$last" ] || die "codex did not produce final markdown" 5 CODEX_OUTPUT_MISSING
  extract_last_json_block "$last" "$RD/codex-final.json" \
    || die "codex final markdown missing trailing JSON block" 6 BAD_VERDICT
}

# ---------------- prompts ----------------

_compact_guide() {
  local loop_dir=$1
  cat "$loop_dir/GUIDE_SNAPSHOT.md"
}

_prompt_claude_work() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4
  cat <<EOF
You are Claude in the Haru Anbu auto review loop. Round $round, step "work".

REQUIRED reading (in order):
1. $loop_dir/GUIDE_SNAPSHOT.md
2. $loop_dir/REQUEST.md
3. $loop_dir/LOG.md (if non-empty — prior rounds)
4. $loop_dir/diff.patch (if non-empty)

Rules:
- Modify ONLY files listed in REQUEST.md "Allowed files" or matching its "Allowed-file globs".
- 이모지 금지. iconify fluent filled 계열만.
- 토큰 SoT: 07_디자인/tokens/tokens.css.
- glass 사용은 보호자앱/AI리포트/온보딩/플로팅 탭바만.
- 의료진/요양보호사 입력/환자 핵심 CTA/SOS 는 flat surface.
- Do NOT modify files under $loop_dir EXCEPT your own outputs in $RD/.
- Do NOT touch _GUIDE.md, _GUIDE_COMPACT.md, GUIDE_SNAPSHOT.md, LOG.md, meta.json.
- Do NOT run git commit / push.

Tasks:
1. Implement the request inside the allowed scope.
2. Write $RD/claude-work.md with sections:
   - 변경 파일 (목록)
   - 의도 (1-3줄)
   - 걱정되는 부분 (있으면)
   - Codex 리뷰 포인트 (있으면)
3. Write $RD/claude-work.json matching:
   {
     "actor":"claude","step":"work","round":$round,
     "started_at":"...", "ended_at":"...",
     "changed_files":["..."],
     "intent_summary":"...",
     "concerns":["..."],
     "review_focus":["..."]
   }
4. Stop. Print "DONE" to stdout.
EOF
}

_prompt_claude_respond() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4
  cat <<EOF
You are Claude in the Haru Anbu auto review loop. Round $round, step "response".

REQUIRED reading:
1. $loop_dir/GUIDE_SNAPSHOT.md
2. $loop_dir/REQUEST.md
3. $RD/claude-work.md (your own prior work this round)
4. $RD/codex-review.md (Codex review you must address)
5. $RD/codex-review.json (must_fix, recommendations)
6. $loop_dir/diff.patch

Rules:
- Apply ALL must_fix items from codex-review.json.
- Apply recommendations only if compatible with REQUEST scope. Skip otherwise; document reason.
- Stay strictly within Allowed files / globs.
- Do not commit or push.

Tasks:
1. Modify source files as needed (same scope rules as round work).
2. Write $RD/claude-response.md with sections:
   - 반영한 항목 (must_fix / recommendations 구분)
   - 반영하지 않은 항목 + 이유
   - 추가 변경 파일
3. Write $RD/claude-response.json matching:
   {
     "actor":"claude","step":"response","round":$round,
     "applied":[{"item_ref":"must_fix[0]","note":"..."}],
     "skipped":[{"item_ref":"recommendations[0]","reason":"..."}],
     "additional_changed_files":["..."]
   }
4. Stop. Print "DONE" to stdout.
EOF
}

_prompt_codex_review() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4
  cat <<EOF
You are Codex in the Haru Anbu auto review loop. Round $round, step "review".
You are READ-ONLY. You cannot modify any file. The harness has placed you in read-only sandbox.

REQUIRED reading:
1. $loop_dir/GUIDE_SNAPSHOT.md
2. $loop_dir/REQUEST.md
3. $loop_dir/diff.patch
4. $RD/claude-work.md
5. $RD/claude-work.json
6. The actual files listed in claude-work.json.changed_files

Apply six review lenses (compact guide section "리뷰 6대 기준"):
1. 토큰 일관성   2. 역할 테마 일관성   3. UX/UI 적합성
4. Glass 사용 원칙   5. 접근성   6. 아이콘/문서 규칙

Output: print MARKDOWN to your final message with sections
- 총평
- 반드시 수정 (issues that must be fixed before merge)
- 개선 권장 (nice-to-have, can defer)
- 유지하면 좋은 점
- 확인한 파일

THEN end your final message with a fenced JSON block (the harness parses it):

\`\`\`json
{
  "actor":"codex",
  "step":"review",
  "round":$round,
  "verdict":"PASS|PASS_WITH_NOTES|FAIL|ESCALATED",
  "must_fix":[{"file":"path","line":0,"issue":"..."}],
  "recommendations":[{"file":"path","issue":"..."}],
  "kept_well":["..."],
  "files_inspected":["..."],
  "scope_violations":[]
}
\`\`\`

Verdict rules:
- FAIL if "must_fix" non-empty.
- PASS_WITH_NOTES if must_fix empty and recommendations non-empty.
- PASS if both empty.
- ESCALATED if request is ambiguous, conflicts with rules, or design judgment must be human.
  In that case include "reason_for_escalation" as a string field.

Constraint: do not modify any file. Do not propose tools that write.
EOF
}

_prompt_codex_final() {
  local round=$1 RD=$2 workdir=$3 loop_dir=$4
  cat <<EOF
You are Codex final QA in the Haru Anbu auto review loop. Round $round, step "final".
You are READ-ONLY.

REQUIRED reading:
1. $loop_dir/GUIDE_SNAPSHOT.md
2. $loop_dir/REQUEST.md (특히 Done criteria)
3. $loop_dir/diff.patch (refreshed)
4. $RD/codex-review.md and codex-review.json (your own previous review)
5. $RD/claude-response.md and claude-response.json
6. The actual updated files

Decide: were all must_fix items addressed? Are Done criteria met? Was scope respected?

Output markdown:
- 총평
- 남은 이슈
- 최종 판단

THEN final fenced JSON block:

\`\`\`json
{
  "actor":"codex",
  "step":"final",
  "round":$round,
  "verdict":"PASS|PASS_WITH_NOTES|FAIL|ESCALATED",
  "remaining_issues":["..."],
  "scope_violations":[]
}
\`\`\`

Same verdict rules as review step. Do not modify any file.
EOF
}
