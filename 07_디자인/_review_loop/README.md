# Auto Review Loop

Claude(구현) ↔ Codex(리뷰) 자동 루프.

설계: `07_디자인/CLAUDE_CODEX_AUTO_LOOP_PLAN_V2_20260510.md`
가이드: `_GUIDE.md` (사람용 풀), `_GUIDE_COMPACT.md` (AI 호출용)

## 빠른 시작

### 1. dry-run으로 한 번 확인

```bash
./scripts/review-loop.sh --dry-run tokens-only "$(cat <<'EOF'
# 작업 요청

## Allowed files

- 07_디자인/tokens/tokens.css

## Request

dry-run 동작 확인용.
EOF
)"
```

worktree와 폴더가 생성되고 AI 호출 없이 종료된다.

### 2. 실제 루프

```bash
./scripts/review-loop.sh tokens-only
```

`REQUEST.md` 가 에디터로 열린다. `## Allowed files` 와 `## Request` 채우고 저장하면 자동 진행. 5~15분.

### 3. 결과

- 변경 결과: `/tmp/haru-anbu-loops/<루프이름>/` (worktree)
- 산출물 사본: `07_디자인/_review_loop/<루프이름>/`
- 사람 읽기용 LOG: `LOG.md`
- 기계 판정: `round-N/codex-*.json`

스크립트는 절대 commit/push 안 한다. PASS여도 사람이 worktree에서 diff 확인 후 직접 머지.

### 4. 머지 또는 폐기

```bash
# OK이면 메인 브랜치로 머지
git merge loop/2026-05-10_tokens-only

# 폐기
git worktree remove /tmp/haru-anbu-loops/2026-05-10_tokens-only
git branch -D loop/2026-05-10_tokens-only
```

## 옵션

```bash
./scripts/review-loop.sh --help
```

| 옵션 | 기본 |
|---|---|
| `--no-worktree` | off (worktree 사용이 기본) |
| `--rounds N` | 1 (최대 2) |
| `--verify MODE` | static |
| `--budget USD` | 3 |
| `--dry-run` | off |

## 제약

- macOS bash 3.2 호환
- 의존: `git`, `jq`, `claude`, `codex`. static verify는 `python3` 또는 `rg`.
- 한 번에 한 루프만 (lock 파일).
- 첫 실행 전 `codex login status`, `claude` 인증 확인.

## 폴더 구조

```txt
07_디자인/_review_loop/
├── _GUIDE.md
├── _GUIDE_COMPACT.md
├── _TEMPLATE/
│   ├── REQUEST.md
│   └── meta.json
├── schemas/
│   └── codex-verdict.schema.json
└── <YYYY-MM-DD>_<name>/    # 루프마다 생성
    ├── REQUEST.md
    ├── GUIDE_SNAPSHOT.md
    ├── meta.json
    ├── diff.patch
    ├── LOG.md
    ├── command.log
    ├── stdio/              # AI 호출 stdout/stderr
    └── round-N/
        ├── claude-work.{md,json}
        ├── codex-review.{md,json}
        ├── claude-response.{md,json}
        └── codex-final.{md,json}
```

## 첫 루프 권장 요청

`tokens-only` 로 작게 시작. REQUEST 본문 예시는 `CLAUDE_CODEX_AUTO_LOOP_PLAN_V2_20260510.md` 12절 참조.
