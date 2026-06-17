"use client";

/**
 * Act 3 — PROCESS (5앱 협업 트랙)
 * 이 챕터는 사이트의 본진. 사람 명령 ↔ AI 응답을 통해 "AI가 만든 게 아니라,
 * AI를 잘 다룬 우리가 만든 것"임을 증거화한다.
 *
 * 현재 3개 prompt 수록 — 세 가지 다른 협업 결을 보여줌:
 *   #32  짧은 명령 + 큰 맥락  ("하던거 해봐라")
 *   #29  구체 비전 + 이터레이션  ("v7 시안. Apple Liquid Glass로.")
 *   #50  반박 모먼트  ("왜 그대로냐?")
 *
 * 이후 5앱별로 prompt가 추가될 자리. 현재 prompt 3개는 보호자앱·온보딩 트랙.
 */

type Meta = { id: string; app: string; date: string };

/* ─────────────────────────────────────────────────────────────────
   Chapter intro — Act 3 시작
   ───────────────────────────────────────────────────────────────── */
function ChapterIntro() {
  return (
    <section
      id="act3-intro"
      className="relative w-full bg-black"
      style={{ height: "180vh" }}
    >
      <div className="sticky top-0 flex h-screen w-full items-center justify-center overflow-hidden px-6 md:px-16">
        <div className="flex max-w-4xl flex-col items-center gap-14 text-center md:gap-16">
          <div
            className="font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
            style={{
              fontSize: "clamp(0.72rem, 0.95vw, 0.86rem)",
              letterSpacing: "0.28em",
            }}
          >
            <span className="mr-3 font-bold text-white">ACT 3</span>PROCESS
          </div>

          <h2
            className="font-sans font-semibold leading-[1.02] tracking-tight text-white"
            style={{ fontSize: "clamp(2.6rem, 7.8vw, 7.2rem)" }}
          >
            다섯 앱,
            <br />
            우리가 만든 방식.
          </h2>

          <p
            className="max-w-xl leading-[1.55] tracking-tight text-[color:var(--color-key-soft)]"
            style={{ fontSize: "clamp(1rem, 1.55vw, 1.35rem)" }}
          >
            한 줄 명령 뒤엔 수십 줄의 맥락이, 짧은 결과 뒤엔 수십 번의 합의가
            있었다.
          </p>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Prompt header — 메타 한 줄
   ───────────────────────────────────────────────────────────────── */
function PromptMeta({ id, app, date }: Meta) {
  return (
    <div
      className="flex flex-wrap items-center justify-center gap-3 font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
      style={{
        fontSize: "clamp(0.62rem, 0.85vw, 0.78rem)",
        letterSpacing: "0.22em",
      }}
    >
      <span className="font-bold text-white">PROMPT #{id}</span>
      <span className="inline-block size-[3px] rounded-full bg-white/20" />
      <span>{app}</span>
      <span className="inline-block size-[3px] rounded-full bg-white/20" />
      <span>{date}</span>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Prompt scene — 단일 명령 (CommandScene 패턴 차용)
   ───────────────────────────────────────────────────────────────── */
function PromptScene({
  meta,
  quote,
  size = "huge",
  wrap = false,
}: {
  meta: Meta;
  quote: string;
  size?: "huge" | "large";
  wrap?: boolean;
}) {
  const fs =
    size === "huge"
      ? "clamp(1.9rem, 5.6vw, 5.6rem)"
      : "clamp(1.6rem, 4.2vw, 4.4rem)";

  return (
    <section
      className="relative w-full bg-black"
      style={{ height: "180vh" }}
    >
      <div className="sticky top-0 flex h-screen w-full items-center justify-center overflow-hidden px-6 md:px-16">
        <div className="flex max-w-[96vw] flex-col items-center gap-12 md:gap-14">
          <PromptMeta {...meta} />
          <p
            className={`text-center font-mono font-medium leading-[1.18] tracking-tight text-white ${
              wrap ? "max-w-[28ch]" : "whitespace-nowrap"
            }`}
            style={{ fontSize: fs }}
          >
            <span className="mr-[0.45em] font-normal text-[color:var(--color-key)]">
              &gt;
            </span>
            &quot;{quote}&quot;
          </p>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Prompt scene — 두 줄 반박 (PROMPT #50 전용)
   ───────────────────────────────────────────────────────────────── */
function PromptSceneRebuttal({
  meta,
  first,
  second,
  gapLabel,
}: {
  meta: Meta;
  first: string;
  second: string;
  gapLabel: string;
}) {
  const fs = "clamp(1.6rem, 4.2vw, 4.4rem)";
  return (
    <section
      className="relative w-full bg-black"
      style={{ height: "180vh" }}
    >
      <div className="sticky top-0 flex h-screen w-full items-center justify-center overflow-hidden px-6 md:px-16">
        <div className="flex max-w-[96vw] flex-col items-center gap-6 md:gap-7">
          <PromptMeta {...meta} />

          <p
            className="max-w-[28ch] text-center font-mono font-medium leading-[1.18] tracking-tight text-white"
            style={{ fontSize: fs }}
          >
            <span className="mr-[0.45em] font-normal text-[color:var(--color-key)]">
              &gt;
            </span>
            &quot;{first}&quot;
          </p>

          <div
            className="my-1 font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
            style={{
              fontSize: "clamp(0.66rem, 0.86vw, 0.78rem)",
              letterSpacing: "0.18em",
            }}
          >
            {gapLabel}
          </div>

          <p
            className="max-w-[28ch] text-center font-mono font-medium leading-[1.18] tracking-tight text-white"
            style={{ fontSize: fs }}
          >
            <span className="mr-[0.45em] font-normal text-[color:var(--color-key)]">
              &gt;
            </span>
            &quot;{second}&quot;
          </p>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Result gallery — 결과 신 공용 헤더 (FailuresGallery 패턴 차용)
   ───────────────────────────────────────────────────────────────── */
function GalleryHeader({
  title,
  accent,
  trace,
}: {
  title: React.ReactNode;
  accent?: string;
  trace: React.ReactNode;
}) {
  return (
    <div className="mx-auto mb-16 max-w-3xl text-center md:mb-20">
      <h3
        className="font-sans font-semibold leading-[1.12] tracking-tight text-white"
        style={{ fontSize: "clamp(1.7rem, 3.6vw, 3rem)" }}
      >
        {title}
      </h3>
      <p
        className="mx-auto mt-8 max-w-[40rem] leading-[1.72] tracking-tight text-[color:var(--color-key-soft)]"
        style={{ fontSize: "clamp(0.92rem, 1.15vw, 1.04rem)" }}
      >
        {trace}
      </p>
      {accent ? null : null}
    </div>
  );
}

function Signature({ items }: { items: { num: string; label: string }[] }) {
  return (
    <div
      className="mt-16 flex flex-wrap items-center justify-center gap-x-10 gap-y-3 text-center font-mono text-[color:var(--color-fg-dim)] md:mt-20"
      style={{
        fontSize: "clamp(0.78rem, 1vw, 0.92rem)",
        letterSpacing: "0.06em",
      }}
    >
      {items.map((it, i) => (
        <span key={i} className="flex items-center gap-3">
          <span className="font-semibold text-white">{it.num}</span>
          <span>{it.label}</span>
          {i < items.length - 1 ? (
            <span className="ml-3 text-white/20">→</span>
          ) : null}
        </span>
      ))}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Result #32 — ONBOARDING 7화면 그리드
   ───────────────────────────────────────────────────────────────── */
const obScreens = [
  { id: "ob01", name: "시작 화면" },
  { id: "ob02", name: "로그인 / 회원가입" },
  { id: "ob03", name: "소셜 로그인" },
  { id: "ob04", name: "역할 선택" },
  { id: "ob05", name: "역할별 인트로" },
  { id: "ob06", name: "동의 (동적)" },
  { id: "ob07", name: "프로필 입력" },
];

function Result32() {
  return (
    <section className="relative w-full bg-[#0e1014] py-24 md:py-32">
      <div className="mx-auto max-w-6xl px-6 md:px-12">
        <GalleryHeader
          title={
            <>
              한 줄 명령에 화면{" "}
              <span className="text-[color:var(--color-key)]">7개</span>가
              나왔다.
            </>
          }
          trace={
            <>
              AI가 한 일 8단계 — 로그인 분기, 소셜 로그인, 역할 카드, 역할별
              인트로, 동의 동적 주입, 프로필 자동 포맷, 슬라이드 버그 수정, v7
              배경 적용. 짧은 명령이 가능했던 건{" "}
              <strong className="font-semibold text-white">
                그 전까지 함께 쌓은 v7 톤·역할 구조·UX 원칙
              </strong>
              이 이미 그 한 줄 안에 들어 있었기 때문이다.
            </>
          }
        />

        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 sm:gap-5 lg:grid-cols-4 lg:gap-6">
          {obScreens.map((s) => (
            <ScreenThumb key={s.id} id={s.id} name={s.name} />
          ))}
        </div>

        <Signature
          items={[
            { num: "1", label: "줄 명령" },
            { num: "8", label: "단계 작업" },
            { num: "9", label: "HTML 파일" },
          ]}
        />
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Result #29 — v7 Liquid Glass 6 이터레이션 + 최종
   ───────────────────────────────────────────────────────────────── */
const iter29 = [
  { n: "ITER 01", label: "4열 그리드" },
  { n: "ITER 02", label: "2열 그리드" },
  { n: "ITER 03", label: "인라인" },
  { n: "ITER 04", label: "4칸 그리드" },
];

function Result29() {
  return (
    <section className="relative w-full bg-[#0e1014] py-24 md:py-32">
      <div className="mx-auto max-w-5xl px-6 md:px-12">
        <GalleryHeader
          title={
            <>
              같은 카드를{" "}
              <span className="text-[color:var(--color-key)]">6번</span>{" "}
              다시 짰다.
            </>
          }
          trace={
            <>
              Liquid Glass 한 줄로 시작했지만, AI 일일 리포트 카드 하나를 두고{" "}
              <strong className="font-semibold text-white">
                수십 건의 피드백
              </strong>
              이 오갔다. 4열 → 2열 → 인라인 → 4칸 → 2×2 bento까지 — 우리가
              매번 &ldquo;이건 아냐&rdquo;라고 잡았기 때문에 최종이 만들어졌다.
            </>
          }
        />

        {/* Iteration trail */}
        <div className="mb-10 flex items-stretch gap-3 overflow-x-auto pb-2 md:gap-4">
          {iter29.map((it, i) => (
            <div key={i} className="flex items-center gap-3 md:gap-4">
              <div
                className="flex aspect-[1.4/1] min-w-[7rem] flex-1 flex-col justify-between rounded-[10px] border border-white/8 bg-white/[0.025] px-3 py-3"
                style={{ minWidth: "7rem" }}
              >
                <span
                  className="font-mono font-medium text-[color:var(--color-fg-dim)]"
                  style={{
                    fontSize: "0.6rem",
                    letterSpacing: "0.12em",
                  }}
                >
                  {it.n}
                </span>
                <span className="text-[0.78rem] font-medium text-[color:var(--color-key-soft)]">
                  {it.label}
                </span>
              </div>
              <span className="shrink-0 font-mono text-[0.85rem] text-[color:var(--color-fg-dim)]">
                →
              </span>
            </div>
          ))}
          <div
            className="flex aspect-[1.4/1] min-w-[7rem] flex-1 flex-col justify-between rounded-[10px] border bg-[rgba(44,122,252,0.06)] px-3 py-3"
            style={{
              borderColor: "rgba(44,122,252,0.32)",
              minWidth: "7rem",
            }}
          >
            <span
              className="font-mono font-medium text-[color:var(--color-accent-pale)]"
              style={{ fontSize: "0.6rem", letterSpacing: "0.12em" }}
            >
              FINAL
            </span>
            <span className="text-[0.78rem] font-medium text-white">
              2×2 Bento
            </span>
          </div>
        </div>

        {/* Hero screen card */}
        <div className="mx-auto max-w-[18rem]">
          <div
            className="relative flex aspect-[9/19.5] flex-col justify-end overflow-hidden rounded-3xl border border-white/8 p-5"
            style={{
              background:
                "linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%)",
            }}
          >
            <div
              aria-hidden
              className="pointer-events-none absolute inset-x-0 top-0 h-[40%]"
              style={{
                background:
                  "radial-gradient(ellipse at top, rgba(44,122,252,0.18) 0%, transparent 65%)",
              }}
            />
            <div
              className="mb-1.5 font-mono text-[0.7rem] text-[color:var(--color-fg-dim)]"
              style={{ letterSpacing: "0.10em" }}
            >
              g-guardian-live.html
            </div>
            <div className="text-[0.95rem] font-medium text-white">
              v7 홈화면 · Liquid Glass
            </div>
          </div>
        </div>

        <Signature
          items={[
            { num: "1", label: "비전" },
            { num: "6", label: "이터레이션" },
            { num: "1", label: "합의" },
          ]}
        />
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Result #50 — 반박 → 자기 진단 → 정정
   ───────────────────────────────────────────────────────────────── */
function Result50() {
  const bars = [
    { m: "11월", h: 17 },
    { m: "12월", h: 60 },
    { m: "1월", h: 93 },
    { m: "2월", h: 14 },
    { m: "3월", h: 83 },
    { m: "4월", h: 100 },
  ];

  return (
    <section className="relative w-full bg-[#0e1014] py-24 md:py-32">
      <div className="mx-auto max-w-5xl px-6 md:px-12">
        <GalleryHeader
          title={
            <>
              틀린 건 우리가{" "}
              <span className="text-[color:var(--color-key)]">먼저</span>{" "}
              잡았다.
            </>
          }
          trace={
            <>
              AI는 1차에{" "}
              <code className="rounded bg-white/5 px-1.5 py-0.5 font-mono text-[0.82em] text-white">
                height %
              </code>{" "}
              값만 바꿨고 — 화면은 그대로였다. 우리가 한 줄로 잡자 AI가 원인을
              자기 진단하고{" "}
              <strong className="font-semibold text-white">
                구조 자체를 다시 짰다
              </strong>
              . 우리가 잘 다룬 협업은 정답을 받는 게 아니라, 틀린 답을 알아채는
              일이다.
            </>
          }
        />

        {/* Rebuttal steps */}
        <div className="mx-auto grid max-w-3xl grid-cols-1 gap-4 md:grid-cols-2">
          <div
            className="rounded-[12px] border border-white/10 bg-white/[0.025] px-5 py-5"
          >
            <div
              className="mb-2 font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
              style={{ fontSize: "0.66rem", letterSpacing: "0.15em" }}
            >
              AI 1차 시도
            </div>
            <p className="text-[0.9rem] leading-[1.55] text-[color:var(--color-key-soft)]">
              <code className="rounded bg-white/5 px-1.5 py-0.5 font-mono text-[0.82em] text-white">
                height: X%
              </code>{" "}
              값만 변경. 화면은 그대로.{" "}
              <code className="rounded bg-white/5 px-1.5 py-0.5 font-mono text-[0.82em] text-white">
                .trend-chart {`{ align-items: flex-end }`}
              </code>{" "}
              때문에 자식 열에 height가 잡히지 않음.
            </p>
          </div>

          <div
            className="rounded-[12px] border px-5 py-5"
            style={{
              background: "rgba(44,122,252,0.04)",
              borderColor: "rgba(44,122,252,0.22)",
            }}
          >
            <div
              className="mb-2 font-mono font-medium uppercase text-[color:var(--color-accent-pale)]"
              style={{ fontSize: "0.66rem", letterSpacing: "0.15em" }}
            >
              AI 2차 — 구조 재설계
            </div>
            <p className="text-[0.9rem] leading-[1.55] text-[color:var(--color-key-soft)]">
              <code className="rounded bg-white/5 px-1.5 py-0.5 font-mono text-[0.82em] text-white">
                align-items: stretch
              </code>{" "}
              +{" "}
              <code className="rounded bg-white/5 px-1.5 py-0.5 font-mono text-[0.82em] text-white">
                .trend-col {`{ height: 100% }`}
              </code>{" "}
              으로 컨테이너 구조 자체 수정. Y축 90만~120만 기준 % 재계산.
            </p>
          </div>
        </div>

        {/* Chart result */}
        <div className="mx-auto mt-12 max-w-3xl rounded-[14px] border border-white/8 bg-white/[0.025] px-6 pt-8 pb-5 md:px-8">
          <div className="mb-3 grid h-36 grid-cols-6 items-end gap-2">
            {bars.map((b, i) => (
              <div
                key={i}
                className="rounded-t-[4px]"
                style={{
                  height: `${b.h}%`,
                  background:
                    "linear-gradient(180deg, rgba(244,245,247,0.85) 0%, rgba(244,245,247,0.55) 100%)",
                }}
              />
            ))}
          </div>
          <div
            className="grid grid-cols-6 gap-2 text-center font-mono text-[0.7rem] text-[color:var(--color-fg-dim)]"
            style={{ letterSpacing: "0.05em" }}
          >
            {bars.map((b) => (
              <span key={b.m}>{b.m}</span>
            ))}
          </div>
        </div>

        <Signature
          items={[
            { num: "1", label: "반박" },
            { num: "1", label: "자기 진단" },
            { num: "1", label: "구조 정정" },
          ]}
        />
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   PROMPT VIDEO — 4단 명령 정밀화 (이터레이션 다이얼로그)
   ───────────────────────────────────────────────────────────────── */
function PromptSceneVideo({
  commands,
}: {
  commands: { label: string; text: string }[];
}) {
  return (
    <section
      className="relative w-full bg-black"
      style={{ height: "200vh" }}
    >
      <div className="sticky top-0 flex h-screen w-full items-center justify-center overflow-hidden px-6 md:px-16">
        <div className="flex max-w-[96vw] flex-col items-center gap-6 md:gap-7">
          <div
            className="flex flex-wrap items-center justify-center gap-3 font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
            style={{
              fontSize: "clamp(0.62rem, 0.85vw, 0.78rem)",
              letterSpacing: "0.22em",
            }}
          >
            <span className="font-bold text-white">PROMPT — VIDEO</span>
            <span className="inline-block size-[3px] rounded-full bg-white/20" />
            <span>Higgsfield Cinema</span>
            <span className="inline-block size-[3px] rounded-full bg-white/20" />
            <span>2026.04</span>
          </div>

          {commands.map((cmd, i) => (
            <div key={i} className="flex flex-col items-center gap-2">
              <div
                className="font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
                style={{
                  fontSize: "clamp(0.62rem, 0.8vw, 0.74rem)",
                  letterSpacing: "0.18em",
                }}
              >
                {cmd.label}
              </div>
              <p
                className="max-w-[44ch] text-center font-mono font-medium leading-[1.22] tracking-tight text-white"
                style={{ fontSize: "clamp(1.05rem, 2.2vw, 2rem)" }}
              >
                <span className="mr-[0.45em] font-normal text-[color:var(--color-key)]">
                  &gt;
                </span>
                &ldquo;{cmd.text}&rdquo;
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   RESULT VIDEO ITER — iter1~3 포스터 + 설명
   (iter4 = 다음 챕터 Act 6 피날레)
   ───────────────────────────────────────────────────────────────── */
function ResultVideoIter() {
  const iters = [
    {
      src: "/media/poster/iter1.jpg",
      label: "ITER 01",
      note: "‘Korean hospital, doctor running.' 한 줄로. 미국식 인테리어가 나왔다.",
    },
    {
      src: "/media/poster/iter2.jpg",
      label: "ITER 02",
      note: "‘301호 302호, 형광등, 백색 핸드레일.' 한국 디테일을 박자 분위기가 살았다.",
    },
    {
      src: "/media/poster/iter3.jpg",
      label: "ITER 03",
      note: "@김미영 같은 AI 인플루언서 핸들로 캐스팅 고정. 컷 사이 인물 일치.",
    },
  ];

  return (
    <section className="relative w-full bg-[#0e1014] py-24 md:py-32">
      <div className="mx-auto max-w-6xl px-6 md:px-12">
        <GalleryHeader
          title={
            <>
              네 번 명령에 영상이{" "}
              <span className="text-[color:var(--color-key)]">한 편씩</span>{" "}
              정밀해졌다.
            </>
          }
          trace={
            <>
              1차는 미국식이었고, 2차는 한국식이었고, 3차는 인물이 일치했다.
              우리가 매번{" "}
              <strong className="font-semibold text-white">
                무엇을 더 정확히 요구해야 하는지
              </strong>{" "}
              알아갔기 때문에 영상이 매번 더 좋아졌다.
            </>
          }
        />

        <div className="grid grid-cols-1 gap-5 md:grid-cols-3 md:gap-6">
          {iters.map((it) => (
            <div key={it.label} className="flex flex-col gap-3">
              <div className="relative aspect-video overflow-hidden rounded-xl border border-white/8">
                <img
                  src={it.src}
                  alt=""
                  className="absolute inset-0 h-full w-full object-cover"
                  draggable={false}
                />
                <div
                  className="absolute inset-0"
                  style={{
                    background:
                      "linear-gradient(180deg, transparent 40%, rgba(0,0,0,0.7) 100%)",
                  }}
                />
                <div
                  className="absolute bottom-3 left-3 font-mono font-medium text-white"
                  style={{
                    fontSize: "0.7rem",
                    letterSpacing: "0.14em",
                  }}
                >
                  {it.label}
                </div>
              </div>
              <p
                className="text-[0.86rem] leading-[1.55] text-[color:var(--color-key-soft)]"
              >
                {it.note}
              </p>
            </div>
          ))}
        </div>

        <Signature
          items={[
            { num: "4", label: "단 명령" },
            { num: "3", label: "이터 (선공개)" },
            { num: "1", label: "최종 영상 — 다음 챕터" },
          ]}
        />
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Common — Screen thumbnail
   ───────────────────────────────────────────────────────────────── */
function ScreenThumb({ id, name }: { id: string; name: string }) {
  return (
    <div
      className="group relative flex aspect-[9/19.5] flex-col justify-end overflow-hidden rounded-[18px] border border-white/8 p-4 transition-[border-color,transform] duration-300 ease-out hover:-translate-y-1 hover:border-white/16"
      style={{
        background:
          "linear-gradient(180deg, rgba(255,255,255,0.045) 0%, rgba(255,255,255,0.02) 100%)",
      }}
    >
      <div
        aria-hidden
        className="pointer-events-none absolute inset-x-0 top-0 h-[36%]"
        style={{
          background:
            "radial-gradient(ellipse at top, rgba(255,255,255,0.04) 0%, transparent 60%)",
        }}
      />
      <div
        className="mb-1 font-mono text-[0.66rem] font-medium text-[color:var(--color-fg-dim)]"
        style={{ letterSpacing: "0.10em" }}
      >
        {id}
      </div>
      <div className="text-[0.85rem] font-medium leading-[1.3] text-[color:var(--color-key-soft)]">
        {name}
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Chapter outro — Act 3 마무리, 새 framing 명시
   ───────────────────────────────────────────────────────────────── */
function ChapterOutro() {
  return (
    <section className="relative w-full bg-black">
      <div className="flex min-h-screen w-full flex-col items-center justify-center px-6 py-32 text-center md:px-16">
        <div className="flex max-w-[50rem] flex-col items-center gap-12">
          <div
            className="font-mono font-medium uppercase text-[color:var(--color-fg-dim)]"
            style={{
              fontSize: "clamp(0.7rem, 0.9vw, 0.82rem)",
              letterSpacing: "0.28em",
            }}
          >
            ACT 3 · CLOSE
          </div>
          <p
            className="font-sans font-semibold leading-[1.18] tracking-tight text-white"
            style={{ fontSize: "clamp(1.8rem, 4.6vw, 4.2rem)" }}
          >
            AI가 만든 게 아니다.
            <br />
            <span className="font-medium text-[color:var(--color-fg-dim)]">
              AI를 잘 다룬
            </span>{" "}
            <em className="text-[color:var(--color-key)] not-italic">우리</em>
            가
            <br />
            만든 것이다.
          </p>
        </div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────────────────────────
   Public — 챕터 전체
   ───────────────────────────────────────────────────────────────── */
export function AppTracksChapter() {
  return (
    <>
      <ChapterIntro />

      <PromptScene
        meta={{ id: "32", app: "ONBOARDING", date: "2026.04.12" }}
        quote="하던거 해봐라."
      />
      <Result32 />

      <PromptScene
        meta={{ id: "29", app: "보호자앱 · 홈", date: "2026.04.12" }}
        quote="v7 시안. Apple Liquid Glass로."
        size="large"
        wrap
      />
      <Result29 />

      <PromptSceneRebuttal
        meta={{ id: "50", app: "보호자앱 · 결제 차트", date: "2026.04.13" }}
        first="표에 들쑥날쑥 그래프 더미데이터 만들어줘."
        second="왜 그대로냐?"
        gapLabel="— AI 1차 작업 —"
      />
      <Result50 />

      <PromptSceneVideo
        commands={[
          { label: "1차", text: "Korean hospital, doctor running." },
          { label: "다시.", text: "301호 302호, 형광등, 백색 핸드레일." },
          {
            label: "다시.",
            text: "@김미영 같은 AI 인플루언서 핸들로 캐스팅 고정.",
          },
          {
            label: "4차에서 멈췄다.",
            text: "렌즈·조명·카메라 워크. talking animatedly로 립싱크만.",
          },
        ]}
      />
      <ResultVideoIter />

      <ChapterOutro />
    </>
  );
}
