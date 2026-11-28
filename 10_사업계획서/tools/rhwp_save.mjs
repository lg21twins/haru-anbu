// 사용: ego-browser nodejs < rhwp_save.mjs  (TaskSpace 9, 저장 경로 고정 — 필요 시 수정)
const SPACE = 9, NAME = "하루안부_달란트_참가신청서", OUT = "/Users/yechanshon/Desktop/하루안부_달란트_참가신청서.hwp";
const task = await taskSpace(SPACE); const page = task.page("p1");
await page.keyboard.press("Escape").catch(() => {});
await page.evaluate(() => { window.showSaveFilePicker = undefined; });
await page.evaluate(() => window.rhwpStudio.automation.execute("file:save-as-hwp"));
await page.waitForTimeout(700);
let s = await page.snapshot();
const tb = s.match(/파일 이름\(N\):"\s*\n\s*textbox \[ref=(\d+)\]/)[1];
await page.fill("@" + tb, NAME);
for (let attempt = 0; attempt < 3; attempt++) {
  await page.waitForTimeout(400);
  s = await page.snapshot();
  const m = s.match(/button \[ref=(\d+)\]\s*\n\s*text "확인"/);
  if (!m) break;
  const dl = page.waitForEvent("download", { timeout: 8000 });
  await page.click("@" + m[1], { label: "confirm save" });
  try { const d = await dl; await d.saveAs(OUT); console.log("saved", OUT); break; } catch (e) { console.log("retry", attempt); }
}
