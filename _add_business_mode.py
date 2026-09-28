#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_add_business_mode.py — добавляет Business Chinese как отдельный режим.

Что делает:
  1. Создаёт web/static/business.html (из HTML-шаблона)
  2. Патчит web/server.py — добавляет /business route
  3. Патчит web/static/app.js — карточка в меню + navigate
  4. Добавляет i18n ключи menu_business / business_sub в 6 языков
Все записи — с валидацией баланса, без сюрпризов.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "web"
STATIC = WEB / "static"
APP = STATIC / "app.js"
I18N = STATIC / "i18n.js"
SERVER = WEB / "server.py"
BUSINESS = STATIC / "business.html"

# ============================================================
# 1. HTML страницы Business
# ============================================================
BUSINESS_HTML = r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>商务中文 · Business Chinese</title>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<script>
tailwind.config = {
  theme: { extend: {
    fontFamily: { sans: ['Inter', 'sans-serif'] },
    colors: { brand: {
      cyan: '#7fd1e6', light: '#e0f4f9', navy: '#1a365d',
      dark: '#0f172a', accent: '#3b82f6'
    }}
  }}
}
</script>
<style>
.bg-dotted-pattern {
  background-color: #f4fafd;
  background-image: radial-gradient(#bce4f0 1.5px, transparent 1.5px);
  background-size: 24px 24px;
}
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
</head>
<body class="bg-gray-50 text-slate-800 font-sans h-screen flex overflow-hidden">

<aside class="w-64 bg-white shadow-lg z-20 flex flex-col h-full border-r border-gray-100">
  <a href="/" class="h-16 flex items-center px-6 border-b border-brand-light bg-brand-light/30 hover:bg-brand-light/60 transition-colors cursor-pointer">
    <div class="flex items-center gap-2 text-brand-navy font-bold text-sm tracking-tight">
      <i class="fa-solid fa-arrow-left text-brand-cyan text-lg"></i>
      <span>← HSK 5 Learner</span>
    </div>
  </a>

  <div class="h-16 flex items-center px-6 border-b border-brand-light">
    <div class="flex items-center gap-2 text-brand-navy font-bold text-sm tracking-tight">
      <i class="fa-solid fa-book-open text-brand-cyan text-lg"></i>
      <span>商务中文<br>БИЗНЕС-КИТАЙСКИЙ</span>
    </div>
  </div>

  <nav class="flex-1 py-6 px-4 space-y-2 overflow-y-auto">
    <a href="#" class="flex items-center gap-3 px-4 py-3 bg-brand-light text-brand-navy rounded-lg font-medium transition-colors">
      <i class="fa-solid fa-border-all w-5 text-center text-brand-cyan"></i> Модули
    </a>
    <a href="#" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:bg-gray-50 hover:text-brand-navy rounded-lg font-medium transition-colors">
      <i class="fa-solid fa-layer-group w-5 text-center"></i> SRS Карточки
    </a>
    <a href="#" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:bg-gray-50 hover:text-brand-navy rounded-lg font-medium transition-colors">
      <i class="fa-solid fa-briefcase w-5 text-center"></i> Кейсы
    </a>
    <a href="#" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:bg-gray-50 hover:text-brand-navy rounded-lg font-medium transition-colors">
      <i class="fa-solid fa-envelope-open-text w-5 text-center"></i> Практика E-mail
    </a>
    <a href="#" class="flex items-center gap-3 px-4 py-3 text-slate-500 hover:bg-gray-50 hover:text-brand-navy rounded-lg font-medium transition-colors">
      <i class="fa-solid fa-chart-simple w-5 text-center"></i> Прогресс
    </a>
  </nav>

  <div class="p-4 border-t border-gray-100 text-xs text-slate-400 text-center">
    Основано на учебнике (主课本):<br>Business Chinese
  </div>
</aside>

<main class="flex-1 flex flex-col h-full overflow-hidden bg-dotted-pattern relative">
  <header class="h-16 bg-brand-cyan/20 backdrop-blur-sm border-b border-white/50 flex items-center justify-between px-8 z-10">
    <h1 class="text-xl font-bold text-brand-navy tracking-wide">Dashboard</h1>
    <div class="flex items-center gap-3 cursor-pointer hover:bg-white/40 p-2 rounded-lg transition-colors">
      <div class="w-8 h-8 rounded-full bg-brand-navy text-white flex items-center justify-center shadow-sm">
        <i class="fa-solid fa-user text-sm"></i>
      </div>
      <span class="text-sm font-medium text-brand-navy" id="biz-user">Гость</span>
    </div>
  </header>

  <div class="flex-1 flex overflow-hidden">
    <div class="flex-1 overflow-y-auto p-8">
      <div class="mb-8">
        <h2 class="text-3xl font-bold text-brand-navy mb-2">С возвращением!</h2>
        <p class="text-slate-600 font-medium">Ваша следующая цель: <span class="text-brand-accent font-semibold">Прием делегации (Модуль 1)</span></p>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
          <div class="absolute top-0 right-0 w-24 h-24 bg-brand-light rounded-bl-full -z-10 transition-transform group-hover:scale-110"></div>
          <div class="flex justify-center mb-6 h-20 items-end">
            <i class="fa-solid fa-users text-5xl text-brand-cyan drop-shadow-sm"></i>
          </div>
          <h3 class="font-bold text-brand-navy text-lg mb-1">МОДУЛЬ 1: ПРИЕМ КЛИЕНТОВ</h3>
          <p class="text-sm text-slate-500 mb-1">Урок 1: Встреча в аэропорту</p>
          <p class="text-sm text-slate-500 mb-5">Темы: Банкет, Презентация</p>
          <div class="flex items-center justify-between text-xs font-bold text-brand-navy mb-2"><span>ПРОГРЕСС</span><span>65%</span></div>
          <div class="w-full bg-gray-100 rounded-full h-2"><div class="bg-brand-navy h-2 rounded-full" style="width:65%"></div></div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
          <div class="flex justify-center mb-6 h-20 items-end">
            <i class="fa-solid fa-clipboard-check text-5xl text-brand-cyan drop-shadow-sm opacity-80"></i>
          </div>
          <h3 class="font-bold text-brand-navy text-lg mb-1">МОДУЛЬ 2: ИНСПЕКЦИЯ</h3>
          <p class="text-sm text-slate-500 mb-1">Урок 4: Посещение производства</p>
          <p class="text-sm text-slate-500 mb-5">Темы: Котировки, Логистика</p>
          <div class="inline-block px-3 py-1 bg-gray-100 text-slate-500 text-xs font-semibold rounded-full mt-2">Не начато</div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
          <div class="flex justify-center mb-6 h-20 items-end">
            <i class="fa-solid fa-bullhorn text-5xl text-brand-cyan drop-shadow-sm"></i>
          </div>
          <h3 class="font-bold text-brand-navy text-lg mb-1">МОДУЛЬ 3: ПРОДВИЖЕНИЕ</h3>
          <p class="text-sm text-slate-500 mb-1">Урок 7: Маркетинг ИИ-решений</p>
          <p class="text-sm text-slate-500 mb-5">Темы: Веб-семинары, Скидки</p>
          <div class="flex items-center justify-between text-xs font-bold text-brand-navy mb-2"><span>ПРОГРЕСС</span><span>10%</span></div>
          <div class="w-full bg-gray-100 rounded-full h-2"><div class="bg-brand-navy h-2 rounded-full" style="width:10%"></div></div>
        </div>

        <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow cursor-pointer group relative overflow-hidden">
          <div class="flex justify-center mb-6 h-20 items-end">
            <i class="fa-solid fa-handshake text-5xl text-brand-cyan drop-shadow-sm opacity-80"></i>
          </div>
          <h3 class="font-bold text-brand-navy text-lg mb-1">МОДУЛЬ 4: ВЫСТАВКИ</h3>
          <p class="text-sm text-slate-500 mb-1">Урок 10: Питчинг на стенде</p>
          <p class="text-sm text-slate-500 mb-5">Темы: B2B Контакты, Образцы</p>
          <div class="inline-block px-3 py-1 bg-gray-100 text-slate-500 text-xs font-semibold rounded-full mt-2">Не начато</div>
        </div>
      </div>
    </div>

    <aside class="w-80 bg-white/80 backdrop-blur-md border-l border-brand-light p-6 overflow-y-auto">
      <h3 class="text-lg font-bold text-brand-navy mb-4">Быстрый доступ</h3>

      <div class="bg-white p-4 rounded-xl shadow-sm border border-brand-light mb-4">
        <h4 class="font-bold text-slate-800 text-sm mb-1">SRS Тренировка</h4>
        <p class="text-xs text-slate-500 mb-3">500 Ключевых слов BCT (B)</p>
        <button class="w-full bg-brand-cyan hover:bg-[#68c3da] text-brand-navy font-bold py-2 px-4 rounded-lg text-sm transition-colors shadow-sm">Начать тренировку</button>
      </div>

      <div class="bg-white p-4 rounded-xl shadow-sm border border-brand-light mb-6">
        <h4 class="font-bold text-slate-800 text-sm mb-1">Кейсы</h4>
        <p class="text-xs text-slate-500 mb-3">Симуляция переговоров 1.3</p>
        <button class="w-full bg-white hover:bg-gray-50 text-brand-navy border border-brand-cyan font-bold py-2 px-4 rounded-lg text-sm transition-colors">Возобновить</button>
      </div>

      <h3 class="text-lg font-bold text-brand-navy mb-3">Sentence Mining</h3>
      <div class="space-y-3">
        <div class="bg-white p-3 rounded-lg shadow-sm border border-gray-100 hover:border-brand-cyan transition-colors cursor-pointer">
          <p class="text-sm font-medium text-slate-800 mb-1">1. 我们的新产品具有先进的AI功能。</p>
          <p class="text-xs text-slate-500 mb-2 font-mono">(Wǒmen de xīn chǎnpǐn jùyǒu xiānjìn de AI gōngnéng.)</p>
          <p class="text-xs text-brand-navy/80 italic">— Наш новый продукт обладает передовыми функциями ИИ.</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm border border-gray-100 hover:border-brand-cyan transition-colors cursor-pointer">
          <p class="text-sm font-medium text-slate-800 mb-1">2. 欢迎各位来我公司参观考察。</p>
          <p class="text-xs text-slate-500 mb-2 font-mono">(Huānyíng gèwèi lái wǒ gōngsī cānguān kǎochá.)</p>
          <p class="text-xs text-brand-navy/80 italic">— Добро пожаловать в нашу компанию для визита и инспекции.</p>
        </div>
        <div class="bg-white p-3 rounded-lg shadow-sm border border-gray-100 hover:border-brand-cyan transition-colors cursor-pointer">
          <p class="text-sm font-medium text-slate-800 mb-1">3. 请问贵公司的主要市场在哪里？</p>
          <p class="text-xs text-slate-500 mb-2 font-mono">(Qǐngwèn guì gōngsī de zhǔyào shìchǎng zài nǎlǐ?)</p>
          <p class="text-xs text-brand-navy/80 italic">— Скажите, пожалуйста, где находится основной рынок вашей компании?</p>
        </div>
      </div>
    </aside>
  </div>
</main>

<script>
// Показать имя пользователя, если залогинен
fetch("/api/auth/me", {credentials:"same-origin"})
  .then(r => r.ok ? r.json() : null)
  .then(u => {
    if (u && u.name) {
      const el = document.getElementById("biz-user");
      if (el) el.textContent = u.name;
    }
  })
  .catch(() => {});
</script>
</body>
</html>
'''

# ============================================================
# 2. route для server.py
# ============================================================
SERVER_ROUTE = '''

@app.route("/business")
def business_page():
    """Страница Business Chinese."""
    return send_from_directory(str(DATA.parent / "web" / "static"), "business.html")

'''

# ============================================================
# 3. запись в app.js меню
# ============================================================
MENU_ENTRY = '  { key: "menu_business", sub: "business_sub", route: "business", color: "amber", icon: "💼" },\n'

# ============================================================
# 4. i18n ключи
# ============================================================
I18N_VALUES = {
    "ru": ("Бизнес-китайский", "商务中文 · Business Chinese"),
    "en": ("Business Chinese", "商务中文 · Business Chinese"),
    "tk": ("Biznes hytaý dili", "商务中文 · Business Chinese"),
    "uz": ("Biznes xitoy tili", "商务中文 · Business Chinese"),
    "tg": ("Забони хитоии тиҷоратӣ", "商务中文 · Business Chinese"),
    "id": ("Bahasa Mandarin Bisnis", "商务中文 · Business Chinese"),
}


def validate(src, label):
    if src.count("`") % 2 != 0:
        return False, f"{label}: backtick odd"
    if src.count("{") != src.count("}"):
        return False, f"{label}: braces {src.count('{')}/{src.count('}')}"
    return True, "OK"


def write_business():
    if BUSINESS.exists():
        print("business.html уже есть — не перезаписываю")
        return
    BUSINESS.write_text(BUSINESS_HTML, encoding="utf-8")
    print(f"OK: создан {BUSINESS.relative_to(ROOT)}  ({len(BUSINESS_HTML)} символов)")


def patch_server():
    src = SERVER.read_text(encoding="utf-8")
    if 'route("/business")' in src:
        print("server.py уже пропатчен")
        return
    # Вставляем перед /static route
    marker = '@app.route("/static/'
    if marker not in src:
        print("!! не нашёл @app.route(\"/static/ — патчи server.py вручную")
        return
    src = src.replace(marker, SERVER_ROUTE + marker, 1)

    ok, reason = validate(src, "server.py")
    print("server.py:", reason)
    if not ok:
        print("!! НЕ пишу server.py")
        return

    bak = SERVER.with_suffix(SERVER.suffix + ".pre_business.bak")
    shutil.copy2(SERVER, bak)
    SERVER.write_text(src, encoding="utf-8")
    print("OK: server.py — добавлен /business")
    print(f"   бэкап: {bak.name}")


def patch_app():
    src = APP.read_text(encoding="utf-8")
    if "menu_business" in src:
        print("app.js уже пропатчен")
        return

    # 1. Найти строку с menu_lessons и вставить нашу после неё
    m = re.search(r'(\{[^}]*key:\s*"menu_lessons"[^}]*\},\s*\n)', src)
    if not m:
        print("!! не нашёл menu_lessons в app.js")
        return
    src = src[:m.end()] + MENU_ENTRY + src[m.end():]

    # 2. В navigate добавить ветку
    nav_marker = 'else if (p[0] === "srs") renderSrs();'
    if nav_marker not in src:
        print("!! не нашёл else if (p[0] === \"srs\") в navigate()")
        return
    src = src.replace(
        nav_marker,
        'else if (p[0] === "business") window.location.href = "/business";\n  ' + nav_marker,
        1,
    )

    ok, reason = validate(src, "app.js")
    print("app.js:", reason)
    if not ok:
        print("!! НЕ пишу app.js")
        return

    bak = APP.with_suffix(APP.suffix + ".pre_business.bak")
    shutil.copy2(APP, bak)
    APP.write_text(src, encoding="utf-8")
    print("OK: app.js — карточка + navigate")
    print(f"   бэкап: {bak.name}")


def patch_i18n():
    src = I18N.read_text(encoding="utf-8")
    if "menu_business" in src:
        print("i18n.js уже пропатчен")
        return

    for lang, (title, sub) in I18N_VALUES.items():
        m = re.search(r'^([ \t]*)' + lang + r'\s*:\s*\{', src, re.MULTILINE)
        if not m:
            print(f"  !! нет блока {lang}")
            continue
        indent = m.group(1)
        # Вставим сразу после {
        start = src.find("{", m.start()) + 1
        insertion = (
            f'\n{indent}  menu_business: "{title}",'
            f'\n{indent}  business_sub: "{sub}",'
        )
        src = src[:start] + insertion + src[start:]

    ok, reason = validate(src, "i18n.js")
    print("i18n.js:", reason)
    if not ok:
        print("!! НЕ пишу i18n.js")
        return

    bak = I18N.with_suffix(I18N.suffix + ".pre_business.bak")
    shutil.copy2(I18N, bak)
    I18N.write_text(src, encoding="utf-8")
    print("OK: i18n.js — ключи menu_business / business_sub")
    print(f"   бэкап: {bak.name}")


def main():
    print("=" * 60)
    print("ДОБАВЛЕНИЕ BUSINESS CHINESE")
    print("=" * 60)
    write_business()
    print()
    patch_server()
    print()
    patch_app()
    print()
    patch_i18n()
    print()
    print("=" * 60)
    print("ГОТОВО")
    print("Перезапусти сервер: Ctrl+C → py web\\server.py")
    print("Открой http://127.0.0.1:5000 → в меню появится карточка")
    print("= " * 30)


if __name__ == "__main__":
    main()