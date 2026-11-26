// rhwp 「개체 속성」 창이 열린 상태에서 page.evaluate 로 실행: 비율 유지 끄고 높이(mm)를 넣고 설정.
// 쓰는 법: 파일에서 마지막 "(h, w) =>" 부터 떼어(lastIndexOf) page.evaluate(`(${fn})(54.35)`) — w(너비 mm)는 줄일 때만
(h, w) => {
  const vis = [...document.querySelectorAll("input")].filter(i => i.offsetParent);
  const lab = i => (i.closest("label")?.textContent || i.parentElement?.textContent || "");
  const keep = vis.find(i => i.type === "checkbox" && lab(i).trim() === "비율 유지");
  const nums = vis.filter(i => i.type === "number" && i.classList.contains("dialog-input"));
  const W = nums[0], H = nums[1];
  if (!keep || !H) return { ok: false, why: "창 없음" };
  if (keep.checked) keep.click();
  const set = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
  if (w) { set.call(W, String(w)); W.dispatchEvent(new Event("input", { bubbles: true })); W.dispatchEvent(new Event("change", { bubbles: true })); }
  set.call(H, String(h));
  H.dispatchEvent(new Event("input", { bubbles: true }));
  H.dispatchEvent(new Event("change", { bubbles: true }));
  const before = { w: W.value, h: H.value, keep: keep.checked };
  const btn = [...document.querySelectorAll("button")].find(b => b.offsetParent && /^설정/.test(b.textContent.trim()));
  btn.click();
  return { ok: true, before };
}
