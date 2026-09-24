# -*- coding: utf-8 -*-
"""Чинит положение bootApp в app.js."""
import shutil
from pathlib import Path

APP = Path(__file__).resolve().parent / "web" / "static" / "app.js"
src = APP.read_text(encoding="utf-8")

# Маркер: bootApp вставлен внутрь hashchange-обработчика
MARKER = 'window.addEventListener("hashchange", () => {\nasync function bootApp() {'
idx = src.find(MARKER)
if idx == -1:
    if "async function bootApp" in src and src.find("async function bootApp") < src.find("hashchange"):
        print("i: bootApp уже на месте")
        raise SystemExit(0)
    print("!! не нашёл повреждённый блок")
    raise SystemExit(1)

head = src[:idx]

# Убираем преждевременные вызовы
head = head.replace(
    'drawBackgroundPattern();\nnavigate(window.location.hash.slice(1) || "menu");\nsetTimeout(maybeShowAnnouncement, 350);\n\n',
    '',
    1,
)

TAIL = '''async function bootApp() {
  const h = window.location.hash || "";
  const qs = window.location.search || "";
  const path = window.location.pathname || "";

  // 1) ссылка активации
  let actToken = null;
  if (h.startsWith("#activate/")) actToken = h.slice("#activate/".length);
  else if (path.startsWith("/activate/")) actToken = path.slice("/activate/".length);
  else {
    const m1 = qs.match(/[?&]activate[=/]([^&#]+)/);
    if (m1) actToken = decodeURIComponent(m1[1]);
  }
  if (actToken) {
    if (typeof HSKAuth !== "undefined") await HSKAuth.doActivate(actToken);
    return;
  }

  // 2) ссылка сброса пароля
  let resetToken = null;
  if (h.startsWith("#reset/")) resetToken = h.slice("#reset/".length);
  else if (path.startsWith("/reset/")) resetToken = path.slice("/reset/".length);
  else {
    const m2 = qs.match(/[?&]reset[=/]([^&#]+)/);
    if (m2) resetToken = decodeURIComponent(m2[1]);
  }
  if (resetToken) {
    if (typeof renderReset === "function") await renderReset(resetToken);
    return;
  }

  // 3) обычный вход
  try {
    const r = await fetch("/api/auth/me", { credentials: "same-origin" });
    const j = await r.json();
    if (!j.user) {
      if (typeof HSKAuth !== "undefined") HSKAuth.showAuthScreen("login");
      return;
    }
    window.HSK_USER = j.user;
    if (typeof HSKAuth !== "undefined") await HSKAuth.loadProgress();
    drawBackgroundPattern();
    navigate(window.location.hash.slice(1) || "menu");
    setTimeout(maybeShowAnnouncement, 350);
  } catch (e) {
    document.getElementById("app").innerHTML =
      `<div style="padding:40px;color:#FF6B6B;font-size:14px">Ошибка соединения: ${e.message}</div>`;
  }
}

window.addEventListener("lang_changed", () => {
  navigate(window.location.hash.slice(1) || "menu");
});
window.addEventListener("resize", () => {
  const c = document.getElementById("bg-pattern");
  if (c) { c.innerHTML = ""; c.dataset.drawn = "0"; }
  drawBackgroundPattern();
});
window.addEventListener("hashchange", () => {
  const h = window.location.hash || "";
  if (h.startsWith("#activate/") || h.startsWith("#reset/")) return;
  navigate(window.location.hash.slice(1) || "menu");
});

bootApp();
'''

bak = APP.with_suffix(".js.pre_boot_fix.bak")
if not bak.exists():
    shutil.copy2(APP, bak)
    print(f"бэкап: {bak.name}")

APP.write_text(head + TAIL, encoding="utf-8")
print("OK: bootApp вынесен на верхний уровень")