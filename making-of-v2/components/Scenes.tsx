"use client";

import dynamic from "next/dynamic";
import { Suspense } from "react";

/* ─────────────────────────────────────────────────────────────────
   7-Act 구성 (2026-05-22 확정)
   ───────────────────────────────────────────────────────────────
   Act 1  Cold open    역할부여     OpeningPromptScene
   Act 2  Scale shot   양           AutoStatsScene (앞으로 이동 + 카피 톤 조정)
   Act 3  Process      사례         AppTracksChapter (NEW 본진)
   Act 4  Self-crit    정직         FailuresGalleryScene
   Act 5  Method       학습         PromptGrammarScene (Video 앞에서 이동)
   Act 6  Video        결과         VideoScene × 4 (중간 → 마지막)
   Act 7  Close        닫음         FinalScene + CreditsScene

   삭제/흡수된 신 (AppTracksChapter로 압축됨):
     ProblemDiscoveryScene · PersonasInterlude · JtbdInterlude ·
     MatrixInterlude · BlueOceanInterlude · LogoEvolutionScene ·
     DesignIterationScene · CodeMaterializeScene · CompletedDesignsScene
     + 도입 CommandScene 3개 ("누구를/그들이/시장에서")
   ───────────────────────────────────────────────────────────────── */

import { OpeningPromptScene } from "@/components/scenes/OpeningPromptScene";
import { LineScene } from "@/components/scenes/LineScene";
import { AutoStatsScene } from "@/components/scenes/AutoStatsScene";
import { FinalScene } from "@/components/scenes/FinalScene";
import { CreditsScene } from "@/components/scenes/CreditsScene";

const AppTracksChapter = dynamic(() =>
  import("@/components/scenes/AppTracksChapter").then(
    (m) => m.AppTracksChapter
  )
);
const PromptGrammarScene = dynamic(() =>
  import("@/components/scenes/PromptGrammarScene").then(
    (m) => m.PromptGrammarScene
  )
);
const FailuresGalleryScene = dynamic(() =>
  import("@/components/scenes/FailuresGalleryScene").then(
    (m) => m.FailuresGalleryScene
  )
);
const VideoScene = dynamic(
  () => import("@/components/scenes/VideoScene").then((m) => m.VideoScene),
  { ssr: false }
);

export function Scenes() {
  return (
    <main className="relative w-full bg-black text-white">
      <Suspense fallback={<div className="h-screen bg-black" />}>

        {/* ═══ Act 1 · Cold open — 역할부여 ═══ */}
        <OpeningPromptScene />

        {/* ═══ Act 2 · Scale shot — "이만큼 했다" 양 ═══ */}
        <div id="nav-scale" className="block" />
        <AutoStatsScene />

        {/* ═══ Act 3 · Process — 5앱 협업 트랙 (본진) ═══ */}
        <div id="nav-process" className="block" />
        <AppTracksChapter />

        {/* ═══ Act 4 · Self-crit — 정직 ═══ */}
        <div id="nav-failures" className="block" />
        <LineScene
          id="s-wrong"
          text="근데 자주 틀렸다."
          size="huge"
          color="text-[color:var(--color-key)]"
        />
        <FailuresGalleryScene />

        {/* ═══ Act 5 · Method — 학습 ═══ */}
        <div id="nav-method" className="block" />
        <PromptGrammarScene />

        {/* ═══ Act 6 · Video — 피날레 (영상만, iter4 hero) ═══
            영상 이터레이션 다이얼로그(1~3차 명령 정밀화)는 Act 3 PromptSceneVideo로 이동.
            여기는 최종 결과 한 편만. */}
        <div id="nav-video" className="block" />
        <VideoScene
          id="s-iter4"
          src="/media/video/iter4.mp4"
          src480="/media/video/iter4-480.mp4"
          poster="/media/poster/iter4.jpg"
          caption="렌즈·조명·카메라 워크. ‘talking animatedly'로 립싱크만. 한국어 더빙은 후처리."
          hero
        />

        {/* ═══ Act 7 · Close — 닫음 ═══ */}
        <FinalScene />
        <CreditsScene />

      </Suspense>
    </main>
  );
}
