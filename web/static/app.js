// HSK 5 Learner — веб-версия
const app = document.getElementById("app");

// ============================================================
// Хранилище прогресса (localStorage)
// ============================================================
const LS = {
  activity: "hsk5_activity",       // {"2026-09-23": 5, ...}
  lessons:  "hsk5_lessons_opened", // ["1.1", "1.2", ...]
  srs:      "hsk5_srs",            // {"细节": {ease, interval, due, reps}}
  settings: "hsk5_settings",       // {sessionSize, newPerDay}
};

function lsGet(key, def) {
  try {
    const v = localStorage.getItem(key);
    return v ? JSON.parse(v) : def;
  } catch (e) { return def; }
}
function lsSet(key, val) {
  try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) {}
  if (typeof HSKAuth !== "undefined" && HSKAuth.syncKey) {
    HSKAuth.syncKey(key, val);
  }
}

function todayStr() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function markActivity(delta = 1) {
  const a = lsGet(LS.activity, {});
  const t = todayStr();
  a[t] = (a[t] || 0) + delta;
  lsSet(LS.activity, a);
}

function markLessonOpened(unit, lesson) {
  const l = lsGet(LS.lessons, []);
  const id = `${unit}.${lesson}`;
  if (!l.includes(id)) {
    l.push(id);
    lsSet(LS.lessons, l);
  }
  markActivity(1);
}

// ============================================================
// Локализация: обратная связь
// ============================================================
const FB = {
  ru: { menu_title: "Обратная связь", menu_sub: "Написать разработчику",
    page_title: "Обратная связь", hint: "Нашли ошибку или есть пожелание? Напишите.",
    name: "Ваше имя (необязательно)", name_ph: "Аноним",
    message: "Сообщение", message_ph: "Опишите проблему или идею...",
    send: "Отправить", empty: "Введите текст", sending: "Отправляю...",
    sent: "Спасибо! Сообщение отправлено.", error: "Не удалось отправить." },
  tk: { menu_title: "Yza baglanyşyk", menu_sub: "Işläp taýýarlaýja ýaz",
    page_title: "Yza baglanyşyk", hint: "Ýalňyşlyk tapdyňyzmy? Ýazyň.",
    name: "Adyňyz (hökman däl)", name_ph: "Näbelli",
    message: "Habar", message_ph: "Meseläni beýan ediň...",
    send: "Ibermek", empty: "Tekst giriziň", sending: "Iberýärin...",
    sent: "Sag boluň!", error: "Iberip bolmady." },
  en: { menu_title: "Feedback", menu_sub: "Write to the developer",
    page_title: "Feedback", hint: "Found a bug? Write to me.",
    name: "Your name (optional)", name_ph: "Anonymous",
    message: "Message", message_ph: "Describe problem or idea...",
    send: "Send", empty: "Enter a message", sending: "Sending...",
    sent: "Thanks! Message sent.", error: "Could not send." },
};
function tFb(k) {
  const l = (typeof getLang === "function" ? getLang() : "ru");
  return (FB[l] || FB.ru)[k] || FB.ru[k] || k;
}

// ============================================================
// Общая локализация
// ============================================================
const UI_T = {
  ru: {
    vocab_search_ph: "Поиск по ханзи, пиньиню или переводу...",
    unit_all: "Все юниты", empty: "Ничего не найдено",
    col_lesson: "Урок", col_hanzi: "汉字", col_pinyin: "Pinyin",
    col_pos: "POS", col_trans: "Перевод",
    grammar_search_ph: "Поиск по правилу или тексту...",
    grammar_total: "правил",
    compare_search_ph: "Поиск по паре слов...",
    compare_common: "Общее", compare_diff: "Различия",
    analyzer_title: "Анализатор иероглифов",
    analyzer_ph: "Введите иероглиф или слово...",
    analyzer_hint: "Например: 细, 电台, 抱怨",
    analyzer_nothing: "Ничего не найдено по этому запросу",
    analyzer_found_in: "Найдено в уроках",
    // Activity
    act_title: "Активность",
    act_total: "Действий всего",
    act_active: "Активных дней",
    act_streak: "Текущий стрик",
    act_best: "Лучший день",
    act_days: "дней",
    act_less: "Меньше",
    act_more: "Больше",
    // Progress
    prg_title: "Прогресс",
    prg_lessons_done: "Уроков открыто",
    prg_words_studied: "Слов в SRS",
    prg_streak: "Стрик",
    prg_today: "Сегодня действий",
    prg_week: "За 7 дней",
    prg_month: "За 30 дней",
    prg_total: "Всего действий",
    prg_reset: "Сбросить прогресс",
    prg_reset_ok: "Прогресс сброшен",
    prg_reset_confirm: "Точно сбросить весь прогресс? Это нельзя отменить.",
    // SRS
    srs_title: "Повторение (SRS)",
    srs_start: "Начать сессию",
    srs_size: "Размер сессии",
    srs_all_done: "Все карточки на сегодня повторены!",
    srs_due: "Карточек к повторению",
    srs_total: "Всего карточек",
    srs_known: "Знаю",
    srs_reveal: "Показать ответ",
    srs_again: "Забыл",
    srs_hard: "Трудно",
    srs_good: "Хорошо",
    srs_easy: "Легко",
    srs_finish: "Сессия завершена",
    srs_correct: "Правильно",
    srs_again_short: "Ещё",
    srs_scope: "Диапазон",
    srs_pick_lessons: "Уроки",
    srs_pick_all: "Все",
    srs_pick_none: "Снять",
    srs_pick_empty: "Выберите хотя бы один урок",
  },
  tk: {
    vocab_search_ph: "Hanzi, pinyin ýa-da terjime boýunça gözle...",
    unit_all: "Ähli bölümler", empty: "Hiç zat tapylmady",
    col_lesson: "Sapak", col_hanzi: "汉字", col_pinyin: "Pinyin",
    col_pos: "POS", col_trans: "Terjime",
    grammar_search_ph: "Düzgün boýunça gözle...",
    grammar_total: "düzgün",
    compare_search_ph: "Söz jübüti boýunça gözle...",
    compare_common: "Umumy", compare_diff: "Tapawut",
    analyzer_title: "Ieroglif analizatory",
    analyzer_ph: "Ieroglif ýa-da söz giriziň...",
    analyzer_hint: "Meselem: 细, 电台, 抱怨",
    analyzer_nothing: "Bu sorag boýunça hiç zat tapylmady",
    analyzer_found_in: "Sapaklarda tapyldy",
    act_title: "Işjeňlik",
    act_total: "Jemi hereketler",
    act_active: "Işjeň günler",
    act_streak: "Häzirki streak",
    act_best: "Iň gowy gün",
    act_days: "gün",
    act_less: "Az", act_more: "Köp",
    prg_title: "Ösüş",
    prg_lessons_done: "Açylan sapaklar",
    prg_words_studied: "SRS-de sözler",
    prg_streak: "Streak",
    prg_today: "Şu gün",
    prg_week: "7 günde",
    prg_month: "30 günde",
    prg_total: "Jemi hereketler",
    prg_reset: "Ösüşi pozmak",
    prg_reset_ok: "Ösüş pozuldy",
    prg_reset_confirm: "Ösüşi pozmalymy? Yzyna gaýtaryp bolmaz.",
    srs_title: "Gaýtalama (SRS)",
    srs_start: "Sessiýany başla",
    srs_size: "Sessiýa ululygy",
    srs_all_done: "Bu gün üçin ähli kartlar gaýtalandy!",
    srs_due: "Gaýtalamaga degişli kartlar",
    srs_total: "Jemi kartlar",
    srs_known: "Bilýärin",
    srs_reveal: "Jogaby görkez",
    srs_again: "Ýatdan çykardym",
    srs_hard: "Kyn",
    srs_good: "Gowy",
    srs_easy: "Aňsat",
    srs_finish: "Sessiýa tamamlandy",
    srs_correct: "Dogry",
    srs_again_short: "Ýene",
    srs_scope: "Aralyk",
    srs_pick_lessons: "Sapaklar",
    srs_pick_all: "Ählisi",
    srs_pick_none: "Aýyr",
    srs_pick_empty: "Iň bolmanda bir sapak saýlaň",
  },
  en: {
    vocab_search_ph: "Search by hanzi, pinyin or translation...",
    unit_all: "All units", empty: "Nothing found",
    col_lesson: "Lesson", col_hanzi: "汉字", col_pinyin: "Pinyin",
    col_pos: "POS", col_trans: "Translation",
    grammar_search_ph: "Search by rule or text...",
    grammar_total: "rules",
    compare_search_ph: "Search by word pair...",
    compare_common: "Common", compare_diff: "Differences",
    analyzer_title: "Hanzi analyzer",
    analyzer_ph: "Enter a character or word...",
    analyzer_hint: "Example: 细, 电台, 抱怨",
    analyzer_nothing: "Nothing found for this query",
    analyzer_found_in: "Found in lessons",
    act_title: "Activity",
    act_total: "Total actions",
    act_active: "Active days",
    act_streak: "Current streak",
    act_best: "Best day",
    act_days: "days",
    act_less: "Less", act_more: "More",
    prg_title: "Progress",
    prg_lessons_done: "Lessons opened",
    prg_words_studied: "Words in SRS",
    prg_streak: "Streak",
    prg_today: "Today",
    prg_week: "Last 7 days",
    prg_month: "Last 30 days",
    prg_total: "Total actions",
    prg_reset: "Reset progress",
    prg_reset_ok: "Progress reset",
    prg_reset_confirm: "Reset all progress? This cannot be undone.",
    srs_title: "Review (SRS)",
    srs_start: "Start session",
    srs_size: "Session size",
    srs_all_done: "All cards reviewed for today!",
    srs_due: "Cards due",
    srs_total: "Total cards",
    srs_known: "Known",
    srs_reveal: "Show answer",
    srs_again: "Again",
    srs_hard: "Hard",
    srs_good: "Good",
    srs_easy: "Easy",
    srs_finish: "Session finished",
    srs_correct: "Correct",
    srs_again_short: "Again",
    srs_scope: "Scope",
    srs_pick_lessons: "Lessons",
    srs_pick_all: "All",
    srs_pick_none: "Clear",
    srs_pick_empty: "Pick at least one lesson",
  },
};
function tU(k) {
  const l = (typeof getLang === "function" ? getLang() : "ru");
  return (UI_T[l] || UI_T.ru)[k] || UI_T.ru[k] || k;
}

// ============================================================
// Фон
// ============================================================
function drawBackgroundPattern() {
  const c = document.getElementById("bg-pattern");
  if (!c || c.dataset.drawn === "1") return;
  c.dataset.drawn = "1";
  const BG = "汉字学习研究书道文心画意诗词歌赋";
  const M = "xyabfπ√∞θαβΔ";
  const w = window.innerWidth, h = window.innerHeight;
  let seed = 42;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647; };
  for (let i = 0; i < 30; i++) {
    const s = document.createElement("span");
    s.textContent = BG[Math.floor(rnd() * BG.length)];
    s.style.left = (rnd() * (w + 100) - 50) + "px";
    s.style.top = (rnd() * (h + 100) - 50) + "px";
    s.style.fontSize = (40 + rnd() * 90) + "px";
    c.appendChild(s);
  }
  for (let i = 0; i < 22; i++) {
    const s = document.createElement("span");
    s.className = "math";
    s.textContent = M[Math.floor(rnd() * M.length)];
    s.style.left = (rnd() * w) + "px";
    s.style.top = (rnd() * h) + "px";
    s.style.fontSize = (14 + rnd() * 16) + "px";
    c.appendChild(s);
  }
}

// ============================================================
// Меню
// ============================================================
const MENU_ITEMS = [
  { key: "menu_lessons",      sub: "lessons_sub",      route: "lessons",   color: "blue",   icon: "📚" },
  { key: "menu_vocab",        sub: "vocab_sub",        route: "vocab",     color: "orange", icon: "📓" },
  { key: "menu_srs",          sub: "srs_sub",          route: "srs",       color: "teal",   icon: "🔁" },
  { key: "menu_activity",     sub: "activity_sub",     route: "activity",  color: "purple", icon: "📊" },
  { key: "menu_progress",     sub: "progress_sub",     route: "progress",  color: "green",  icon: "📈" },
  { key: "menu_analyzer",     sub: "analyzer_sub",     route: "analyzer",  color: "pink",   icon: "🔍" },
  { key: "menu_grammar",      sub: "grammar_sub",      route: "grammar",   color: "purple", icon: "📝" },
  { key: "menu_compare",      sub: "compare_sub",      route: "compare",   color: "teal",   icon: "⚖" },
  { key: "menu_achievements", sub: "achievements_sub", route: "achievements", color: "orange", icon: "🏆" },
  { key: "menu_settings",     sub: "settings_sub",     route: "settings",  color: "blue",   icon: "⚙" },
];

function renderMainMenu() {
  app.innerHTML = `
    <div class="header">
      <span class="logo">中文</span>
      <span class="dot">·</span>
      <span class="app-name">${t("app_name")}</span>
    </div>
    <div class="version">v0.1.0 · web</div>
    <div class="main-layout">
      <div class="menu-list" id="menu-list"></div>
      <div class="sidebar" id="sidebar"></div>
    </div>`;
  const list = document.getElementById("menu-list");
  for (const item of MENU_ITEMS) {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="card-icon ${item.color}">${item.icon}</div>
      <div class="card-text">
        <div class="card-title">${t(item.key).replace(/^[^\s]+\s*/, "")}</div>
        <div class="card-sub">${t(item.sub)}</div>
      </div>
      <div class="card-chevron">›</div>`;
    card.addEventListener("click", () => navigate(item.route));
    list.appendChild(card);
  }
  const fb = document.createElement("div");
  fb.className = "card";
  fb.innerHTML = `
    <div class="card-icon teal">✉</div>
    <div class="card-text">
      <div class="card-title">${tFb("menu_title")}</div>
      <div class="card-sub">${tFb("menu_sub")}</div>
    </div>
    <div class="card-chevron">›</div>`;
  fb.addEventListener("click", () => navigate("feedback"));
  list.appendChild(fb);

  const lessons = lsGet(LS.lessons, []);
  const act = lsGet(LS.activity, {});
  const todayCount = act[todayStr()] || 0;

  let streak = 0;
  const d = new Date();
  while (true) {
    const s = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    if (act[s]) { streak++; d.setDate(d.getDate() - 1); } else break;
  }

  const sb = document.getElementById("sidebar");
  sb.innerHTML = `
    <div class="continue-card" id="btn-continue">
      <div class="continue-icon">▶</div>
      <div>
        <div class="continue-title">${t("continue")}</div>
        <div class="continue-sub">${lessons.length ? "Уроки" : "Начни с Урока 1.1"}</div>
      </div>
    </div>
    <button class="side-btn" id="btn-lang">
      <span style="font-size:18px">🌐</span>
      <span>${langName()}</span>
    </button>
    ${!(window.HSK_USER && window.HSK_USER.guest) ? `<button class="side-btn" id="btn-profile">
      <span style="font-size:18px">${(window.HSK_USER && window.HSK_USER.avatar) || "👤"}</span>
      <span>${(window.HSK_USER && window.HSK_USER.name) || "Профиль"}</span>
    </button>` : ""}
    ${(window.HSK_USER && window.HSK_USER.is_admin) ? `
    <button class="side-btn" id="btn-admin" style="color:#FFB84D">
      <span style="font-size:18px">👑</span>
      <span>Админка</span>
    </button>` : ""}
    ${!(window.HSK_USER && window.HSK_USER.guest) ? `<button class="side-btn" id="btn-logout" style="color:#FF6B6B">
      <span style="font-size:18px">⎋</span>
      <span>Выйти</span>
    </button>` : ""}
    <div class="streak-card">
      <div style="font-size:28px">🔥</div>
      <div>
        <div class="streak-num">${streak}</div>
        <div class="streak-label">${t("streak")}</div>
      </div>
    </div>
    <div class="progress-bar-container">
      <div class="progress-header">
        <span>${t("course_progress")}</span>
        <span>${lessons.length}/18</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" style="width: ${Math.round(lessons.length / 18 * 100)}%"></div>
      </div>
    </div>
    <div style="font-size:12px;color:#8B9AAB;margin-top:8px;text-align:center">
      ${tU("prg_today")}: ${todayCount}
    </div>`;
  document.getElementById("btn-continue").addEventListener("click", () => navigate("lessons"));
  document.getElementById("btn-lang").addEventListener("click", () => cycleLang());
  const btnProf = document.getElementById("btn-profile");
  const btnOut = document.getElementById("btn-logout");
  const btnAdmin = document.getElementById("btn-admin");
  if (btnAdmin) btnAdmin.addEventListener("click", () => navigate("admin"));
  if (btnProf) btnProf.addEventListener("click", () => navigate("profile"));
  if (btnOut) btnOut.addEventListener("click", () => {
    if (confirm("Выйти из аккаунта? Прогресс сохранён на сервере.")) {
      HSKAuth.logout();
    }
  });
}
function langName() {
  return { ru: "Сменить язык", tk: "Dili çalyş", en: "Change language" }[getLang()];
}
function cycleLang() {
  const o = ["ru", "tk", "en"], c = getLang();
  setLang(o[(o.indexOf(c) + 1) % o.length]);
}

// ============================================================
// Список уроков
// ============================================================
const UNIT_TITLES = {
  1: { zh: "了解生活", ru: "Понимание жизни", tk: "Durmuşy düşünmek", en: "Understanding Life" },
  2: { zh: "谈古说今", ru: "О прошлом и настоящем", tk: "Geçmiş we häzirki zaman", en: "Past and Present" },
  3: { zh: "倾听故事", ru: "Слушаем истории", tk: "Hekaýalary diňlemek", en: "Listening to Stories" },
  4: { zh: "走近科学", ru: "Ближе к науке", tk: "Ylyma ýakynlaşmak", en: "Approaching Science" },
  5: { zh: "放眼世界", ru: "Взгляд на мир", tk: "Dünýä nazary", en: "Seeing the World" },
  6: { zh: "修养身心", ru: "Душа и тело", tk: "Ruhy we beden", en: "Cultivating Body and Mind" },
};
const UNIT_COLORS = { 1: "#3A6088", 2: "#3A7060", 3: "#7A6030",
  4: "#5A4A88", 5: "#3A7080", 6: "#7A3A60" };

async function renderLessons() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">📚 ${t("menu_lessons").replace(/^[^\s]+\s*/, "")}</span></div>
    <div class="version">${t("lessons_sub")}</div>
    <div id="lessons-content" class="loading">${t("loading")}</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  try {
    const r = await fetch("/api/lessons");
    const ls = await r.json();
    const byUnit = {};
    for (const l of ls) { (byUnit[l.unit] = byUnit[l.unit] || []).push(l); }
    const cont = document.getElementById("lessons-content");
    cont.classList.remove("loading");
    cont.innerHTML = "";
    const opened = lsGet(LS.lessons, []);
    for (const u of Object.keys(byUnit).sort()) {
      const block = document.createElement("div");
      block.className = "unit-block";
      const tt = UNIT_TITLES[u] || {};
      const tr = tt[getLang()] || tt.en || "";
      block.innerHTML = `
        <div class="unit-header">
          <span class="unit-label">UNIT ${u}</span>
          <span class="unit-name">${tt.zh || ""} · ${tr}</span>
        </div>`;
      for (const l of byUnit[u]) {
        const row = document.createElement("div");
        row.className = "lesson-row";
        const color = UNIT_COLORS[l.unit] || "#3A6088";
        const zh = (l.title && l.title.zh) || `Урок ${l.unit}.${l.lesson}`;
        const trT = (l.title && (l.title[getLang()] || l.title.en)) || "";
        const done = opened.includes(`${l.unit}.${l.lesson}`);
        row.innerHTML = `
          <div class="lesson-num" style="background:${color}">${l.unit}.${l.lesson}</div>
          <div class="lesson-titles">
            <div class="lesson-zh">${zh}</div>
            <div class="lesson-tr">${trT}</div>
          </div>
          <div class="card-chevron">${done ? "✓" : "›"}</div>`;
        row.addEventListener("click", () => navigate(`lesson/${l.unit}/${l.lesson}`));
        block.appendChild(row);
      }
      cont.appendChild(block);
    }
  } catch (e) {
    document.getElementById("lessons-content").innerHTML =
      `<div style="color:#FF6B6B">Ошибка: ${e.message}</div>`;
  }
}

// ============================================================
// Хелпер: фильтр по юнитам
// ============================================================
function makeUnitFilter(container, onPick) {
  const units = ["all", 1, 2, 3, 4, 5, 6];
  let cur = "all";
  function draw() {
    container.innerHTML = "";
    for (const u of units) {
      const b = document.createElement("button");
      const label = u === "all" ? tU("unit_all") : `Unit ${u}`;
      const active = u === cur;
      b.textContent = label;
      b.style.cssText =
        `padding:6px 14px;border-radius:8px;font-size:13px;cursor:pointer;` +
        `border:1px solid ${active ? "#66B2FF" : "#444"};` +
        `background:${active ? "#4a9eff" : "transparent"};color:#fff`;
      b.addEventListener("click", () => { cur = u; draw(); onPick(cur); });
      container.appendChild(b);
    }
  }
  draw();
  return () => cur;
}

// ============================================================
// СЛОВАРЬ
// ============================================================
let vocabCache = null;

async function renderVocab() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">📓 ${t("menu_vocab").replace(/^[^\s]+\s*/, "")}</span></div>
    <div class="version">${t("vocab_sub")}</div>
    <div class="content-card" style="margin-top:14px">
      <input id="search" type="text" placeholder="${tU("vocab_search_ph")}"
             style="width:100%;padding:10px;border-radius:8px;border:1px solid #444;background:#0e1620;color:#fff;font-size:15px;box-sizing:border-box">
      <div id="filters" style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap"></div>
      <div id="status" style="margin-top:12px;font-size:13px;color:#8B9AAB"></div>
    </div>
    <div id="table-wrap" style="margin-top:12px"></div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  if (!vocabCache) {
    try { vocabCache = await (await fetch("/api/vocab")).json(); }
    catch (e) { vocabCache = []; }
  }
  let query = "", unit = "all";
  const getUnit = makeUnitFilter(document.getElementById("filters"), (u) => { unit = u; table(); });
  function table() {
    unit = getUnit();
    const lang = getLang();
    const items = vocabCache.filter(w => {
      if (unit !== "all" && w.unit !== unit) return false;
      if (!query) return true;
      const q = query.toLowerCase();
      const m = w.meaning || {};
      return (w.hanzi || "").includes(q)
          || (w.pinyin || "").toLowerCase().includes(q)
          || ((m[lang] || m.en || "").toLowerCase().includes(q));
    });
    document.getElementById("status").textContent =
      `${items.length} / ${vocabCache.length} · ${t("vocab_words")}`;
    const wrap = document.getElementById("table-wrap");
    if (!items.length) {
      wrap.innerHTML = `<div class="loading" style="padding:30px">${tU("empty")}</div>`;
      return;
    }
    let html = `<div class="content-card"><table class="vocab-table"><thead><tr>
      <th style="width:70px">${tU("col_lesson")}</th>
      <th style="width:80px">${tU("col_hanzi")}</th>
      <th style="width:120px">${tU("col_pinyin")}</th>
      <th style="width:55px">${tU("col_pos")}</th>
      <th>${tU("col_trans")}</th>
    </tr></thead><tbody>`;
    for (const w of items) {
      const m = w.meaning || {};
      const tr = m[lang] || m.en || "";
      html += `<tr>
        <td style="color:#8B9AAB;font-size:13px">${w.unit}.${w.lesson}</td>
        <td class="cell-hanzi">${escapeHtml(w.hanzi)}</td>
        <td class="cell-pinyin">${escapeHtml(w.pinyin)}</td>
        <td class="cell-pos">${escapeHtml(w.pos)}</td>
        <td>${escapeHtml(tr)}</td></tr>`;
    }
    wrap.innerHTML = html + "</tbody></table></div>";
  }
  document.getElementById("search").addEventListener("input", e => {
    query = e.target.value.trim(); table();
  });
  table();
}

// ============================================================
// ГРАММАТИКА
// ============================================================
let grammarCache = null;

async function renderGrammar() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">📝 ${t("menu_grammar").replace(/^[^\s]+\s*/, "")}</span></div>
    <div class="version">${t("grammar_sub")}</div>
    <div class="content-card" style="margin-top:14px">
      <input id="search" type="text" placeholder="${tU("grammar_search_ph")}"
             style="width:100%;padding:10px;border-radius:8px;border:1px solid #444;background:#0e1620;color:#fff;font-size:15px;box-sizing:border-box">
      <div id="filters" style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap"></div>
      <div id="status" style="margin-top:12px;font-size:13px;color:#8B9AAB"></div>
    </div>
    <div id="list" style="margin-top:12px"></div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  if (!grammarCache) {
    try { grammarCache = await (await fetch("/api/grammar")).json(); }
    catch (e) { grammarCache = []; }
  }
  let query = "", unit = "all";
  const getUnit = makeUnitFilter(document.getElementById("filters"), (u) => { unit = u; draw(); });
  function draw() {
    unit = getUnit();
    const lang = getLang();
    const items = grammarCache.filter(g => {
      if (unit !== "all" && g.unit !== unit) return false;
      if (!query) return true;
      const q = query.toLowerCase();
      const ex = (g.explanation || {})[lang] || (g.explanation || {}).en || "";
      return (g.word || "").toLowerCase().includes(q) || ex.toLowerCase().includes(q);
    });
    document.getElementById("status").textContent =
      `${items.length} / ${grammarCache.length} · ${tU("grammar_total")}`;
    const wrap = document.getElementById("list");
    if (!items.length) {
      wrap.innerHTML = `<div class="loading" style="padding:30px">${tU("empty")}</div>`;
      return;
    }
    wrap.innerHTML = "";
    for (const g of items) {
      const card = document.createElement("div");
      card.className = "grammar-card";
      const expl = (g.explanation && (g.explanation[lang] || g.explanation.en)) || "";
      let exs = "";
      for (let i = 0; i < (g.examples || []).length; i++) {
        const e = g.examples[i];
        const eTr = e[lang] || e.en || "";
        exs += `<div class="grammar-example">
          <div class="ex-zh">${i + 1}. ${escapeHtml(e.zh || "")}</div>
          <div class="ex-tr">${escapeHtml(eTr)}</div></div>`;
      }
      card.innerHTML = `
        <div class="grammar-head">
          <span class="grammar-word">${escapeHtml(g.word || "")}</span>
          <span class="grammar-pos" style="margin-left:10px;color:#8B9AAB;font-size:13px">
            ${g.unit}.${g.lesson} · ${escapeHtml(g.pos || "")}</span>
        </div>
        <div class="grammar-expl">${escapeHtml(expl)}</div>
        ${exs}`;
      wrap.appendChild(card);
    }
  }
  document.getElementById("search").addEventListener("input", e => {
    query = e.target.value.trim(); draw();
  });
  draw();
}

// ============================================================
// СРАВНЕНИЕ СЛОВ
// ============================================================
let compareCache = null;

async function renderCompare() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">⚖ ${t("menu_compare").replace(/^[^\s]+\s*/, "")}</span></div>
    <div class="version">${t("compare_sub")}</div>
    <div class="content-card" style="margin-top:14px">
      <input id="search" type="text" placeholder="${tU("compare_search_ph")}"
             style="width:100%;padding:10px;border-radius:8px;border:1px solid #444;background:#0e1620;color:#fff;font-size:15px;box-sizing:border-box">
      <div id="filters" style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap"></div>
      <div id="status" style="margin-top:12px;font-size:13px;color:#8B9AAB"></div>
    </div>
    <div id="list" style="margin-top:12px"></div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  if (!compareCache) {
    try { compareCache = await (await fetch("/api/compare")).json(); }
    catch (e) { compareCache = []; }
  }
  let query = "", unit = "all";
  const getUnit = makeUnitFilter(document.getElementById("filters"), (u) => { unit = u; draw(); });
  function draw() {
    unit = getUnit();
    const lang = getLang();
    const items = compareCache.filter(c => {
      if (unit !== "all" && c.unit !== unit) return false;
      if (!query) return true;
      const q = query.toLowerCase();
      const cm = (c.common || {})[lang] || (c.common || {}).en || "";
      return (c.word_a || "").toLowerCase().includes(q)
          || (c.word_b || "").toLowerCase().includes(q)
          || cm.toLowerCase().includes(q);
    });
    document.getElementById("status").textContent = `${items.length} / ${compareCache.length}`;
    const wrap = document.getElementById("list");
    if (!items.length) {
      wrap.innerHTML = `<div class="loading" style="padding:30px">${tU("empty")}</div>`;
      return;
    }
    wrap.innerHTML = "";
    for (const c of items) {
      const card = document.createElement("div");
      card.className = "compare-card";
      const cm = (c.common && (c.common[lang] || c.common.en)) || "";
      let diffs = "";
      for (const d of (c.differences || [])) {
        const dt = d[lang] || d.en || "";
        diffs += `<div class="compare-diff-item">${escapeHtml(dt)}</div>`;
      }
      card.innerHTML = `
        <div class="compare-head">${escapeHtml(c.word_a || "")}
          <span style="color:#8B9AAB;font-weight:400;font-size:13px;margin-left:8px">
            ${c.unit}.${c.lesson}</span>
        </div>
        <div class="compare-common">≈ ${tU("compare_common")}</div>
        <div class="compare-common-text">${escapeHtml(cm)}</div>
        <div class="compare-diff-title">≠ ${tU("compare_diff")}</div>
        ${diffs}`;
      wrap.appendChild(card);
    }
  }
  document.getElementById("search").addEventListener("input", e => {
    query = e.target.value.trim(); draw();
  });
  draw();
}

// ============================================================
// АНАЛИЗАТОР ИЕРОГЛИФОВ
// ============================================================
async function renderAnalyzer() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">🔍 ${tU("analyzer_title")}</span></div>
    <div class="version">${tU("analyzer_hint")}</div>
    <div class="content-card" style="margin-top:14px">
      <input id="q" type="text" placeholder="${tU("analyzer_ph")}" autofocus
             style="width:100%;padding:12px;border-radius:8px;border:1px solid #444;background:#0e1620;color:#fff;font-size:20px;box-sizing:border-box">
    </div>
    <div id="result" style="margin-top:14px"></div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  if (!vocabCache) {
    try { vocabCache = await (await fetch("/api/vocab")).json(); }
    catch (e) { vocabCache = []; }
  }
  const lang = getLang();
  function draw() {
    const q = document.getElementById("q").value.trim();
    const wrap = document.getElementById("result");
    if (!q) { wrap.innerHTML = ""; return; }
    const matches = vocabCache.filter(w =>
      (w.hanzi || "").includes(q) || (w.pinyin || "").toLowerCase().includes(q.toLowerCase()));
    if (!matches.length) {
      wrap.innerHTML = `<div class="loading" style="padding:30px">${tU("analyzer_nothing")}</div>`;
      return;
    }
    wrap.innerHTML = "";
    for (const w of matches) {
      const m = w.meaning || {};
      const tr = m[lang] || m.en || "";
      const card = document.createElement("div");
      card.className = "content-card";
      card.style.marginBottom = "10px";
      card.innerHTML = `
        <div style="display:flex;align-items:baseline;gap:16px;flex-wrap:wrap">
          <div class="cell-hanzi" style="font-size:44px;font-weight:700">${escapeHtml(w.hanzi)}</div>
          <div class="cell-pinyin" style="font-size:18px;color:#8B9AAB">${escapeHtml(w.pinyin)}</div>
          <div style="font-size:13px;color:#8B9AAB">${escapeHtml(w.pos)}</div>
          <div style="font-size:18px;margin-left:auto;color:#66B2FF">${escapeHtml(tr)}</div>
        </div>
        <div style="margin-top:8px;font-size:13px;color:#8B9AAB">${tU("analyzer_found_in")}: ${w.unit}.${w.lesson}</div>`;
      wrap.appendChild(card);
    }
  }
  document.getElementById("q").addEventListener("input", draw);
}

// ============================================================
// ACTIVITY (heatmap 365 дней)
// ============================================================
function renderActivity() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">📊 ${tU("act_title")}</span></div>
    <div id="content" class="loading">${t("loading")}</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));

  const act = lsGet(LS.activity, {});
  const content = document.getElementById("content");
  content.classList.remove("loading");

  // Статистика
  let total = 0, activeDays = 0, bestDay = 0, bestDate = "";
  for (const [d, c] of Object.entries(act)) {
    total += c;
    if (c > 0) activeDays++;
    if (c > bestDay) { bestDay = c; bestDate = d; }
  }
  let streak = 0;
  const dd = new Date();
  while (true) {
    const s = `${dd.getFullYear()}-${String(dd.getMonth() + 1).padStart(2, "0")}-${String(dd.getDate()).padStart(2, "0")}`;
    if (act[s]) { streak++; dd.setDate(dd.getDate() - 1); } else break;
  }

  // Heatmap 53 недели × 7 дней
  const WEEKS = 53, CELL = 14, GAP = 3;
  const totalW = WEEKS * (CELL + GAP);
  const totalH = 7 * (CELL + GAP);

  // находим начало — понедельник 52 недели назад
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const start = new Date(today);
  start.setDate(start.getDate() - (WEEKS * 7 - 1));
  // выравниваем на понедельник
  const dow = (start.getDay() + 6) % 7;
  start.setDate(start.getDate() - dow);

  const cellsByWeek = [];
  const cur = new Date(start);
  for (let w = 0; w < WEEKS; w++) {
    const week = [];
    for (let d = 0; d < 7; d++) {
      const s = `${cur.getFullYear()}-${String(cur.getMonth() + 1).padStart(2, "0")}-${String(cur.getDate()).padStart(2, "0")}`;
      const future = cur > today;
      week.push({ date: s, count: future ? -1 : (act[s] || 0) });
      cur.setDate(cur.getDate() + 1);
    }
    cellsByWeek.push(week);
  }

  function level(c) {
    if (c < 0) return -1;
    if (c === 0) return 0;
    if (c <= 2) return 1;
    if (c <= 5) return 2;
    if (c <= 10) return 3;
    return 4;
  }
  function color(lv) {
    return ["#1a2430", "#0e4429", "#006d32", "#26a641", "#39d353"][lv + 1] || "#1a2430";
  }

  let svg = `<svg width="${totalW}" height="${totalH}" style="display:block;max-width:100%">`;
  for (let w = 0; w < WEEKS; w++) {
    for (let d = 0; d < 7; d++) {
      const { date, count } = cellsByWeek[w][d];
      const lv = level(count);
      if (lv < 0) continue;
      const x = w * (CELL + GAP), y = d * (CELL + GAP);
      svg += `<rect x="${x}" y="${y}" width="${CELL}" height="${CELL}" rx="2" fill="${color(lv)}"><title>${date}: ${count}</title></rect>`;
    }
  }
  svg += "</svg>";

  content.innerHTML = `
    <div class="content-card" style="margin-top:14px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px;margin-bottom:14px">
        <div>
          <div style="font-size:24px;font-weight:700;color:#66B2FF">${total}</div>
          <div style="font-size:12px;color:#8B9AAB">${tU("act_total")}</div>
        </div>
        <div>
          <div style="font-size:24px;font-weight:700;color:#66B2FF">${activeDays}</div>
          <div style="font-size:12px;color:#8B9AAB">${tU("act_active")}</div>
        </div>
        <div>
          <div style="font-size:24px;font-weight:700;color:#66B2FF">${streak} ${tU("act_days")}</div>
          <div style="font-size:12px;color:#8B9AAB">${tU("act_streak")}</div>
        </div>
        <div>
          <div style="font-size:24px;font-weight:700;color:#66B2FF">${bestDay}</div>
          <div style="font-size:12px;color:#8B9AAB">${tU("act_best")}${bestDate ? " · " + bestDate : ""}</div>
        </div>
      </div>
      <div style="overflow-x:auto;padding-bottom:8px">${svg}</div>
      <div style="display:flex;align-items:center;gap:6px;margin-top:10px;font-size:12px;color:#8B9AAB">
        <span>${tU("act_less")}</span>
        <span style="display:inline-block;width:14px;height:14px;background:#1a2430;border-radius:2px"></span>
        <span style="display:inline-block;width:14px;height:14px;background:#0e4429;border-radius:2px"></span>
        <span style="display:inline-block;width:14px;height:14px;background:#006d32;border-radius:2px"></span>
        <span style="display:inline-block;width:14px;height:14px;background:#26a641;border-radius:2px"></span>
        <span style="display:inline-block;width:14px;height:14px;background:#39d353;border-radius:2px"></span>
        <span>${tU("act_more")}</span>
      </div>
    </div>`;
}

// ============================================================
// PROGRESS
// ============================================================
function renderProgress() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">📈 ${tU("prg_title")}</span></div>
    <div id="content" class="loading">${t("loading")}</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));

  const act = lsGet(LS.activity, {});
  const lessons = lsGet(LS.lessons, []);
  const srs = lsGet(LS.srs, {});

  let total = 0, activeDays = 0;
  for (const c of Object.values(act)) { total += c; if (c > 0) activeDays++; }

  let streak = 0;
  const dd = new Date();
  while (true) {
    const s = `${dd.getFullYear()}-${String(dd.getMonth() + 1).padStart(2, "0")}-${String(dd.getDate()).padStart(2, "0")}`;
    if (act[s]) { streak++; dd.setDate(dd.getDate() - 1); } else break;
  }

  const today = act[todayStr()] || 0;
  let week = 0, month = 0;
  const now = new Date();
  for (let i = 0; i < 30; i++) {
    const d = new Date(now); d.setDate(d.getDate() - i);
    const s = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    const c = act[s] || 0;
    if (i < 7) week += c;
    month += c;
  }

  const srsWords = Object.keys(srs).length;
  const srsLearned = Object.values(srs).filter(r => r.reps >= 3).length;

  const content = document.getElementById("content");
  content.classList.remove("loading");
  content.innerHTML = `
    <div class="content-card" style="margin-top:14px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:18px">
        <div>
          <div style="font-size:28px;font-weight:700;color:#66B2FF">${lessons.length} / 18</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_lessons_done")}</div>
          <div class="progress-bar" style="margin-top:8px">
            <div class="progress-fill" style="width: ${Math.round(lessons.length / 18 * 100)}%"></div>
          </div>
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#66B2FF">${srsWords}</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_words_studied")}</div>
          ${srsWords ? `<div style="font-size:12px;color:#5CD68E;margin-top:4px">${tU("srs_known")}: ${srsLearned}</div>` : ""}
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#FFB84D">${streak} 🔥</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_streak")}</div>
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#5CD68E">${today}</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_today")}</div>
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#8B9AAB">${week}</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_week")}</div>
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#8B9AAB">${month}</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_month")}</div>
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#8B9AAB">${total}</div>
          <div style="font-size:12px;color:#8B9AAB;margin-top:4px">${tU("prg_total")} · ${activeDays} ${tU("act_days")}</div>
        </div>
      </div>
      <button id="reset" style="margin-top:20px;padding:10px 20px;border-radius:8px;background:transparent;color:#FF6B6B;border:1px solid #FF6B6B;cursor:pointer;font-size:14px">
        ${tU("prg_reset")}
      </button>
    </div>`;

  document.getElementById("reset").addEventListener("click", () => {
    if (!confirm(tU("prg_reset_confirm"))) return;
    localStorage.removeItem(LS.activity);
    localStorage.removeItem(LS.lessons);
    localStorage.removeItem(LS.srs);
    alert(tU("prg_reset_ok"));
    renderProgress();
  });
}

// ============================================================
// SRS
// ============================================================
let srsSession = null;

// --- SRS: выбор уроков ---
const SRS_LESSONS_KEY = "hsk5_srs_lessons";
let _srsHanziMap = null;
function srsBuildHanziMap() {
  if (_srsHanziMap) return _srsHanziMap;
  _srsHanziMap = {};
  for (const w of (vocabCache || [])) {
    if (w && w.hanzi) _srsHanziMap[w.hanzi] = { unit: w.unit, lesson: w.lesson };
  }
  return _srsHanziMap;
}
function srsGetLessonSel() {
  const raw = lsGet(SRS_LESSONS_KEY, "all");
  if (raw === "all") return "all";
  if (!Array.isArray(raw)) return "all";
  return raw;
}
function srsSetLessonSel(sel) { lsSet(SRS_LESSONS_KEY, sel); }
function srsHanziInSel(hanzi, sel) {
  if (sel === "all") return true;
  if (!Array.isArray(sel) || !sel.length) return false;
  const map = srsBuildHanziMap();
  const info = map[hanzi];
  if (!info || !info.unit || !info.lesson) return false;
  return sel.indexOf("u" + info.unit + "_l" + info.lesson) >= 0;
}


function srsLoad() { return lsGet(LS.srs, {}); }
function srsSave(data) { lsSet(LS.srs, data); }

// ============================================================
// AnkiDroid-style SRS (SM-2 with learning steps)
// ============================================================
function srsDefaultSettings() {
  return {
    learnSteps: [1, 10],
    relearnSteps: [10],
    graduatingInterval: 1,
    easyInterval: 4,
    startingEase: 2.5,
    minEase: 1.3,
    easyBonus: 1.3,
    hardMultiplier: 1.2,
    maxInterval: 365 * 5,
    newIntervalAfterLapse: 0,
    delayBonus: true,
  };
}
const SRS_SETTINGS_KEY = "hsk5_srs_settings";
const SRS_MIN = 60 * 1000;
const SRS_DAY = 24 * 60 * SRS_MIN;

function srsGetSettings() {
  const stored = lsGet(SRS_SETTINGS_KEY, {});
  return Object.assign(srsDefaultSettings(), stored || {});
}
function srsSaveSettings(s) { lsSet(SRS_SETTINGS_KEY, s); }

function srsCardDefaults(now) {
  const cfg = srsGetSettings();
  return {
    state: "new", stepIndex: 0, due: now,
    interval: 0, ease: cfg.startingEase, reps: 0, lapses: 0,
  };
}

function srsMigrateCard(card, now) {
  if (!card || typeof card !== "object") return srsCardDefaults(now);
  if (card.state) return card;
  const cfg = srsGetSettings();
  if ((card.reps || 0) >= 1 && (card.interval || 0) >= 1) card.state = "review";
  else card.state = "new";
  card.stepIndex = card.stepIndex || 0;
  if (!card.ease) card.ease = cfg.startingEase;
  return card;
}

function srsStateLabel(card) {
  if (!card) return "NEW";
  return ({ new: "NEW", learning: "LEARN", review: "REVIEW", relearning: "RELEARN" }[card.state || "new"]) || "NEW";
}

function srsFmtMs(ms) {
  if (ms < 60 * 1000) return Math.round(ms / 1000) + "s";
  if (ms < 60 * 60 * 1000) return Math.round(ms / (60 * 1000)) + "m";
  if (ms < 24 * 60 * 60 * 1000) return (ms / (60 * 60 * 1000)).toFixed(1) + "h";
  const d = ms / (24 * 60 * 60 * 1000);
  if (d < 30) return Math.round(d) + "d";
  if (d < 365) return (d / 30).toFixed(1) + "mo";
  return (d / 365).toFixed(1) + "y";
}

function srsPreviewIntervals(card) {
  const cfg = srsGetSettings();
  const now = Date.now();
  const c = card || srsCardDefaults(now);
  const state = c.state || "new";
  const out = { again: "", hard: "", good: "", easy: "" };
  if (state === "new") {
    const s0 = cfg.learnSteps[0] || 1;
    const s1 = cfg.learnSteps[1] || s0 * 10;
    out.again = srsFmtMs(s0 * SRS_MIN);
    out.hard  = srsFmtMs(((s0 + s1) / 2) * SRS_MIN);
    out.good  = srsFmtMs(s1 * SRS_MIN);
    out.easy  = srsFmtMs(cfg.easyInterval * SRS_DAY);
    return out;
  }
  if (state === "learning" || state === "relearning") {
    const steps = state === "relearning" ? cfg.relearnSteps : cfg.learnSteps;
    const cur = steps[c.stepIndex] || steps[steps.length - 1] || 1;
    const nxt = steps[c.stepIndex + 1];
    out.again = srsFmtMs((steps[0] || 1) * SRS_MIN);
    out.hard  = srsFmtMs((nxt ? (cur + nxt) / 2 : cur * 1.5) * SRS_MIN);
    out.good  = nxt ? srsFmtMs(nxt * SRS_MIN) : srsFmtMs(cfg.graduatingInterval * SRS_DAY);
    out.easy  = srsFmtMs(cfg.easyInterval * SRS_DAY);
    return out;
  }
  const iv = Math.max(1, c.interval || 1);
  const ease = c.ease || cfg.startingEase;
  const delayDays = Math.max(0, (now - (c.due || now)) / SRS_DAY);
  out.again = srsFmtMs((cfg.relearnSteps[0] || 10) * SRS_MIN);
  out.hard  = srsFmtMs(Math.max(1, iv * cfg.hardMultiplier) * SRS_DAY);
  const g = iv * ease + (cfg.delayBonus ? delayDays / 2 : 0);
  out.good = srsFmtMs(Math.max(1, g) * SRS_DAY);
  const e = iv * ease * cfg.easyBonus + (cfg.delayBonus ? delayDays : 0);
  out.easy = srsFmtMs(Math.max(1, e) * SRS_DAY);
  return out;
}

function srsApplyRating(hanzi, rating) {
  const db = srsLoad();
  const now = Date.now();
  const cfg = srsGetSettings();
  let c = db[hanzi] ? srsMigrateCard(db[hanzi], now) : srsCardDefaults(now);

  if (c.state === "new") { c.state = "learning"; c.stepIndex = 0; }

  if (c.state === "learning" || c.state === "relearning") {
    const steps = c.state === "relearning" ? cfg.relearnSteps : cfg.learnSteps;
    if (rating === 1) {
      c.stepIndex = 0;
      c.due = now + steps[0] * SRS_MIN;
    } else if (rating === 2) {
      const cur = steps[c.stepIndex] || steps[steps.length - 1];
      const nxt = steps[c.stepIndex + 1];
      c.due = now + (nxt ? (cur + nxt) / 2 : cur * 1.5) * SRS_MIN;
    } else if (rating === 3) {
      const ni = c.stepIndex + 1;
      if (ni < steps.length) {
        c.stepIndex = ni;
        c.due = now + steps[ni] * SRS_MIN;
      } else {
        c.state = "review";
        c.interval = cfg.graduatingInterval;
        c.reps = (c.reps || 0) + 1;
        c.due = now + cfg.graduatingInterval * SRS_DAY;
      }
    } else {
      c.state = "review";
      c.interval = cfg.easyInterval;
      c.reps = (c.reps || 0) + 1;
      c.ease = Math.min(3.5, (c.ease || cfg.startingEase) + 0.15);
      c.due = now + cfg.easyInterval * SRS_DAY;
    }
  } else if (c.state === "review") {
    const delayDays = Math.max(0, (now - (c.due || now)) / SRS_DAY);
    const iv = Math.max(1, c.interval || 1);
    const ease = c.ease || cfg.startingEase;
    if (rating === 1) {
      c.lapses = (c.lapses || 0) + 1;
      c.ease = Math.max(cfg.minEase, ease - 0.2);
      c.interval = Math.max(1, Math.round(iv * cfg.newIntervalAfterLapse));
      c.state = "relearning";
      c.stepIndex = 0;
      c.due = now + (cfg.relearnSteps[0] || 10) * SRS_MIN;
    } else if (rating === 2) {
      c.ease = Math.max(cfg.minEase, ease - 0.15);
      c.interval = Math.min(cfg.maxInterval, Math.max(1, iv * cfg.hardMultiplier));
      c.due = now + c.interval * SRS_DAY;
    } else if (rating === 3) {
      const nx = iv * ease + (cfg.delayBonus ? delayDays / 2 : 0);
      c.interval = Math.min(cfg.maxInterval, Math.max(1, Math.round(nx)));
      c.reps = (c.reps || 0) + 1;
      c.due = now + c.interval * SRS_DAY;
    } else {
      const nx = iv * ease * cfg.easyBonus + (cfg.delayBonus ? delayDays : 0);
      c.ease = Math.min(3.5, ease + 0.15);
      c.interval = Math.min(cfg.maxInterval, Math.max(1, Math.round(nx)));
      c.reps = (c.reps || 0) + 1;
      c.due = now + c.interval * SRS_DAY;
    }
  }
  c.lastRating = rating;
  db[hanzi] = c;
  srsSave(db);
  return c;
}


function srsReview(hanzi, rating) {
  return srsApplyRating(hanzi, rating);
}

function srsDueCards() {
  const db = srsLoad();
  const now = Date.now();
  return Object.entries(db).filter(([_, r]) => (r.due || 0) <= now);
}

async function renderSrs() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">🔁 ${tU("srs_title")}</span></div>
    <div id="content" class="loading">${t("loading")}</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));

  if (!vocabCache) {
    try { vocabCache = await (await fetch("/api/vocab")).json(); }
    catch (e) { vocabCache = []; }
  }

  const db = srsLoad();
  const known = Object.keys(db).length;
  const due = srsDueCards().length;

  const content = document.getElementById("content");
  content.classList.remove("loading");

  if (srsSession) { srsRenderCard(); return; }

  content.innerHTML = `
    <div class="content-card" style="margin-top:14px">
      <div style="display:flex;gap:18px;flex-wrap:wrap;align-items:center;margin-bottom:16px">
        <div>
          <div style="font-size:28px;font-weight:700;color:#66B2FF">${due}</div>
          <div style="font-size:12px;color:#8B9AAB">${tU("srs_due")}</div>
        </div>
        <div>
          <div style="font-size:28px;font-weight:700;color:#8B9AAB">${known}</div>
          <div style="font-size:12px;color:#8B9AAB">${tU("srs_total")}</div>
        </div>
      </div>
      <div id="lessons-pick"></div>
      <div style="font-size:13px;color:#8B9AAB;margin-bottom:8px">${tU("srs_size")}</div>
      <div id="size-btns" style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px"></div>
      <button id="start" style="padding:12px 24px;border-radius:10px;background:#4a9eff;color:#fff;border:0;font-size:16px;cursor:pointer;font-weight:600">
        ${tU("srs_start")}
      </button>
    </div>`;

  let size = lsGet(LS.settings, {}).sessionSize || 20;
  function drawSize() {
    const wrap = document.getElementById("size-btns");
    wrap.innerHTML = "";
    for (const n of [10, 20, 30, 50]) {
      const b = document.createElement("button");
      const active = n === size;
      b.textContent = n;
      b.style.cssText =
        `padding:8px 18px;border-radius:8px;cursor:pointer;font-size:14px;` +
        `border:1px solid ${active ? "#66B2FF" : "#444"};` +
        `background:${active ? "#4a9eff" : "transparent"};color:#fff`;
      b.addEventListener("click", () => {
        size = n;
        const s = lsGet(LS.settings, {}); s.sessionSize = n; lsSet(LS.settings, s);
        drawSize();
  srsDrawLessons();
      });
      wrap.appendChild(b);
    }
  }
  drawSize();

  document.getElementById("start").addEventListener("click", () => {
    srsStartSession(size);
  });
  srsAddHelpButton();
  srsTutorialMaybeShow();
}

function srsStartSession(size) {
  const db = srsLoad();
  const now = Date.now();
  const sel = srsGetLessonSel();
  if (Array.isArray(sel) && sel.length === 0) {
    alert(tU("srs_pick_empty"));
    return;
  }
  const entries = Object.entries(db).map(([h, c]) => [h, srsMigrateCard(c, now)]);

  let learning = entries
    .filter(([h, c]) => (c.state === "learning" || c.state === "relearning") && (c.due || 0) <= now && srsHanziInSel(h, sel))
    .map(([h]) => h);

  let review = entries
    .filter(([h, c]) => c.state === "review" && (c.due || 0) <= now && srsHanziInSel(h, sel))
    .map(([h]) => h);

  const all = (vocabCache || []).map(w => w.hanzi).filter(Boolean);
  let fresh = all.filter(h => {
    const c = db[h];
    if (!c) return srsHanziInSel(h, sel);
    return srsMigrateCard(c, now).state === "new" && srsHanziInSel(h, sel);
  });
  for (let i = fresh.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [fresh[i], fresh[j]] = [fresh[j], fresh[i]];
  }

  let candidates = learning.concat(review).concat(fresh);
  candidates = candidates.slice(0, size);
  if (!candidates.length) { alert(tU("srs_all_done")); return; }
  srsSession = { queue: candidates, done: 0, total: candidates.length, revealed: false };
  srsRenderCard();
}


// ============================================================
// SRS Tutorial: анимированный баннер-онбординг
// ============================================================
(function srsTutInit() {
  if (document.getElementById("srs-tut-style")) return;
  const style = document.createElement("style");
  style.id = "srs-tut-style";
  style.textContent = `
    @keyframes srsTutFadeIn { from { opacity:0 } to { opacity:1 } }
    @keyframes srsTutSlideIn { from { opacity:0; transform:translateY(24px) scale(.96) } to { opacity:1; transform:translateY(0) scale(1) } }
    @keyframes srsTutFloat { 0%,100% { transform:translateY(0) } 50% { transform:translateY(-10px) } }
    @keyframes srsTutPulse { 0%,100% { transform:scale(1); box-shadow:0 0 0 0 rgba(74,158,255,.45) } 50% { transform:scale(1.05); box-shadow:0 0 0 14px rgba(74,158,255,0) } }
    @keyframes srsTutBounce { 0%,100% { transform:translateY(0) scale(1) } 50% { transform:translateY(-8px) scale(1.06) } }
    #srs-tut-card { animation:srsTutSlideIn .4s cubic-bezier(.2,.8,.2,1); }
    .srs-tut-icon { animation:srsTutFloat 2.4s ease-in-out infinite; display:inline-block; }
    .srs-tut-dot { transition:all .25s ease; }
    .srs-tut-btn { transition:transform .15s ease, filter .15s ease; }
    .srs-tut-btn:hover { transform:translateY(-2px); filter:brightness(1.08); }
    .srs-tut-btn:active { transform:translateY(0) scale(.97); }
    #srs-help { animation:srsTutPulse 2.6s ease-in-out infinite; }
  `;
  (document.head || document.documentElement).appendChild(style);
})();

function srsTutorialSlides() {
  const lang = (typeof getLang === "function") ? getLang() : "ru";
  const T = {
    ru: [
      { icon: "🎯", title: "Зачем нужен SRS?", text: "SRS показывает слово в тот момент, когда ты почти его забыл. Так запоминание работает в 3–5 раз эффективнее обычной зубрёжки." },
      { icon: "📚", title: "Выбери уроки", text: "Перед началом сессии отметь уроки, которые хочешь повторить. Например, только 1.1 и 2.3 — система возьмёт слова лишь из них." },
      { icon: "👀", title: "Вспомни перевод", text: "Посмотри на иероглиф. Попробуй вспомнить чтение (pinyin) и перевод — лучше вслух. Не торопись открывать ответ." },
      { icon: "🔄", title: "Открой ответ", text: "Нажми «Показать ответ» и честно проверь себя. Если подглядывал заранее — эффекта не будет." },
      { icon: "🎚️", title: "Оцени себя", text: "Забыл / Трудно / Хорошо / Легко. На кнопках видно, через сколько карточка вернётся — 1m, 10m, 1d или 4d." },
      { icon: "📈", title: "Возвращайся каждый день", text: "5–10 минут в день достаточно. Система сама подберёт расписание — от тебя нужно только заходить и честно отвечать." }
    ],
    en: [
      { icon: "🎯", title: "Why SRS?", text: "SRS shows a word right before you forget it. That makes memorization 3–5× more effective than cramming." },
      { icon: "📚", title: "Pick your lessons", text: "Before starting, tick the lessons you want to review. For example, only 1.1 and 2.3 — the system will pull words only from them." },
      { icon: "👀", title: "Recall the meaning", text: "Look at the character. Try to recall the reading (pinyin) and translation — preferably out loud. Don't rush to reveal." },
      { icon: "🔄", title: "Reveal the answer", text: "Tap 'Show answer' and check yourself honestly. If you peeked early — the effect is lost." },
      { icon: "🎚️", title: "Rate yourself", text: "Again / Hard / Good / Easy. The buttons show when the card will return — 1m, 10m, 1d or 4d." },
      { icon: "📈", title: "Come back daily", text: "5–10 minutes a day is enough. The system handles the schedule — you just show up and answer honestly." }
    ],
    tk: [
      { icon: "🎯", title: "SRS näme üçin?", text: "SRS sözi ýatdan çykmazyndan öň görkezýär. Bu ýatlamany 3–5 esse has täsirli edýär." },
      { icon: "📚", title: "Sapaklary saýla", text: "Sessiýa başlamazdan öň gaýtalamak isleýän sapaklary bellediň. Meselem, diňe 1.1 we 2.3." },
      { icon: "👀", title: "Manysyny ýatla", text: "Iýeroglife serediň. Okaýyşy (pinyin) we terjimesini ýatlamaga synanyşyň — sesli aýtsaňyz gowy." },
      { icon: "🔄", title: "Jogaby aç", text: "\"Jogaby görkez\" düwmesine basyň we özüňizi dogruçyl barlaň. Öňünden seretmäň." },
      { icon: "🎚️", title: "Özüňize baha beriň", text: "Ýatdan çykardym / Kyn / Gowy / Aňsat. Düwmelerde haçan gaýdyp geljekdigi görünýär — 1m, 10m, 1d ýa 4d." },
      { icon: "📈", title: "Her gün gaýdyp geliň", text: "Günde 5–10 minut ýeterlik. Tertibi ulgam özi düzýär." }
    ]
  };
  return T[lang] || T.en;
}

function srsTutorialLabels() {
  const l = (typeof getLang === "function") ? getLang() : "ru";
  if (l === "ru") return { skip: "Пропустить", back: "Назад", next: "Далее →", done: "Понятно!" };
  if (l === "tk") return { skip: "Geç", back: "Yza", next: "Indiki →", done: "Düşündim!" };
  return { skip: "Skip", back: "Back", next: "Next →", done: "Got it!" };
}

function srsShowTutorial(onDone) {
  const slides = srsTutorialSlides();
  const L = srsTutorialLabels();
  let idx = 0;
  const overlay = document.createElement("div");
  overlay.id = "srs-tut-overlay";
  overlay.style.cssText = "position:fixed;inset:0;background:rgba(8,12,20,0.85);backdrop-filter:blur(6px);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px;animation:srsTutFadeIn .3s ease";

  function render() {
    const s = slides[idx];
    const isLast = idx === slides.length - 1;
    overlay.innerHTML = `
      <div id="srs-tut-card" style="max-width:460px;width:100%;background:linear-gradient(160deg,#1b2333 0%,#141a26 100%);border:1px solid #2a3446;border-radius:18px;padding:28px 24px 22px;text-align:center;color:#E6EDF5;box-shadow:0 24px 60px rgba(0,0,0,.55);position:relative">
        <button class="srs-tut-btn" id="srs-tut-x" style="position:absolute;top:10px;right:12px;background:transparent;border:0;color:#6E7A8A;font-size:20px;cursor:pointer;line-height:1;padding:6px">✕</button>
        <div class="srs-tut-icon" style="font-size:64px;line-height:1;margin-bottom:14px">${s.icon}</div>
        <div style="font-size:20px;font-weight:700;margin-bottom:10px">${escapeHtml(s.title)}</div>
        <div style="font-size:14px;color:#A6B4C2;line-height:1.55;min-height:78px">${escapeHtml(s.text)}</div>
        <div style="display:flex;gap:6px;justify-content:center;margin:22px 0 18px">
          ${slides.map((_, i) => `<span class="srs-tut-dot" style="width:8px;height:8px;border-radius:50%;background:${i === idx ? '#4a9eff' : '#2f3a4d'};transform:${i === idx ? 'scale(1.35)' : 'scale(1)'}"></span>`).join("")}
        </div>
        <div style="display:flex;gap:10px;justify-content:space-between;align-items:center">
          <button class="srs-tut-btn" id="srs-tut-skip" style="background:transparent;border:0;color:#8B9AAB;font-size:13px;cursor:pointer;padding:8px 4px">${L.skip}</button>
          <div style="display:flex;gap:8px">
            ${idx > 0 ? `<button class="srs-tut-btn" id="srs-tut-prev" style="padding:10px 18px;border-radius:10px;border:1px solid #333;background:transparent;color:#E6EDF5;font-size:14px;cursor:pointer">${L.back}</button>` : ""}
            <button class="srs-tut-btn" id="srs-tut-next" style="padding:10px 22px;border-radius:10px;border:0;background:#4a9eff;color:#fff;font-size:14px;font-weight:600;cursor:pointer">${isLast ? L.done : L.next}</button>
          </div>
        </div>
      </div>
    `;
    document.getElementById("srs-tut-x").onclick = close;
    document.getElementById("srs-tut-skip").onclick = close;
    document.getElementById("srs-tut-next").onclick = () => { if (isLast) close(); else { idx++; render(); } };
    const pv = document.getElementById("srs-tut-prev");
    if (pv) pv.onclick = () => { if (idx > 0) { idx--; render(); } };
  }
  function close() {
    overlay.remove();
    if (typeof onDone === "function") onDone();
  }
  document.body.appendChild(overlay);
  render();
}

function srsTutorialMaybeShow() {
  if (typeof srsSession !== "undefined" && srsSession) return;
  if (lsGet("hsk5_srs_tutorial_seen", false)) return;
  setTimeout(() => srsShowTutorial(() => lsSet("hsk5_srs_tutorial_seen", true)), 500);
}

function srsAddHelpButton() {
  if (document.getElementById("srs-help")) return;
  const btn = document.createElement("button");
  btn.id = "srs-help";
  btn.title = "How to use SRS / Как пользоваться";
  btn.textContent = "?";
  btn.style.cssText = "position:fixed;right:20px;bottom:20px;width:50px;height:50px;border-radius:50%;border:0;background:#4a9eff;color:#fff;font-size:22px;font-weight:700;cursor:pointer;box-shadow:0 8px 24px rgba(74,158,255,.45);z-index:900;transition:transform .15s";
  btn.addEventListener("mouseenter", () => btn.style.transform = "scale(1.1)");
  btn.addEventListener("mouseleave", () => btn.style.transform = "scale(1)");
  btn.addEventListener("click", () => srsShowTutorial());
  document.body.appendChild(btn);
}

window.addEventListener("hashchange", () => {
  const b = document.getElementById("srs-help");
  if (b) b.remove();
});

function srsDrawLessons() {
  const wrap = document.getElementById("lessons-pick");
  if (!wrap) return;
  const sel = srsGetLessonSel();
  const byUnit = {};
  for (const w of (vocabCache || [])) {
    if (!w || !w.hanzi || !w.unit) continue;
    if (!byUnit[w.unit]) byUnit[w.unit] = new Set();
    byUnit[w.unit].add(w.lesson);
  }
  const units = Object.keys(byUnit).map(Number).sort((a, b) => a - b);
  if (!units.length) { wrap.innerHTML = ""; return; }

  let total = 0;
  for (const u of units) total += byUnit[u].size;

  let html = `<div style="background:rgba(255,255,255,0.03);border:1px solid #2a3446;border-radius:10px;padding:12px;margin-bottom:16px">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <div style="font-size:13px;color:#8B9AAB">${tU("srs_pick_lessons")}</div>
      <div style="display:flex;gap:6px">
        <button id="sel-all" type="button" style="padding:4px 10px;border-radius:6px;border:1px solid #444;background:transparent;color:#fff;font-size:12px;cursor:pointer">${tU("srs_pick_all")}</button>
        <button id="sel-none" type="button" style="padding:4px 10px;border-radius:6px;border:1px solid #444;background:transparent;color:#fff;font-size:12px;cursor:pointer">${tU("srs_pick_none")}</button>
      </div>
    </div>`;
  for (const u of units) {
    html += `<div style="margin-bottom:6px"><div style="font-size:12px;color:#8B9AAB;margin-bottom:4px">Unit ${u}</div><div style="display:flex;flex-wrap:wrap;gap:6px">`;
    for (const l of Array.from(byUnit[u]).sort((a, b) => a - b)) {
      const key = "u" + u + "_l" + l;
      const active = sel === "all" || (Array.isArray(sel) && sel.indexOf(key) >= 0);
      html += `<button type="button" class="srs-lesson-chip" data-key="${key}" style="padding:5px 12px;border-radius:8px;font-size:13px;cursor:pointer;border:1px solid ${active ? "#4a9eff" : "#444"};background:${active ? "rgba(74,158,255,0.2)" : "transparent"};color:${active ? "#8EC8FF" : "#ccc"}">${u}.${l}</button>`;
    }
    html += `</div></div>`;
  }
  html += `</div>`;
  wrap.innerHTML = html;

  wrap.querySelectorAll(".srs-lesson-chip").forEach(btn => {
    btn.addEventListener("click", () => {
      const key = btn.dataset.key;
      let cur = srsGetLessonSel();
      if (cur === "all") {
        cur = [];
        for (const u of units) for (const l of byUnit[u]) cur.push("u" + u + "_l" + l);
      } else {
        cur = cur.slice();
      }
      const i = cur.indexOf(key);
      if (i >= 0) cur.splice(i, 1); else cur.push(key);
      if (cur.length === total) srsSetLessonSel("all");
      else srsSetLessonSel(cur);
      srsDrawLessons();
    });
  });
  const a = document.getElementById("sel-all");
  const n = document.getElementById("sel-none");
  if (a) a.addEventListener("click", () => { srsSetLessonSel("all"); srsDrawLessons(); });
  if (n) n.addEventListener("click", () => { srsSetLessonSel([]); srsDrawLessons(); });
}


function srsRenderCard() {
  if (!srsSession || !srsSession.queue.length) {
    const total = srsSession ? srsSession.total : 0;
    srsSession = null;
    markActivity(1);
    app.innerHTML = `
      <button class="back-btn" id="back">‹ ${t("back")}</button>
      <div class="header"><span class="app-name">🔁 ${tU("srs_title")}</span></div>
      <div class="content-card" style="margin-top:30px;text-align:center;padding:40px">
        <div style="font-size:48px">🎉</div>
        <div style="font-size:20px;margin-top:12px">${tU("srs_finish")}</div>
        <div style="color:#8B9AAB;margin-top:8px">${total}</div>
        <button id="ok" style="margin-top:24px;padding:12px 24px;border-radius:10px;background:#4a9eff;color:#fff;border:0;font-size:16px;cursor:pointer">OK</button>
      </div>`;
    document.getElementById("back").addEventListener("click", () => navigate("menu"));
    document.getElementById("ok").addEventListener("click", () => navigate("menu"));
    return;
  }
  const hanzi = srsSession.queue[0];
  const word = vocabCache.find(w => w.hanzi === hanzi) || { hanzi, pinyin: "", pos: "", meaning: {} };
  const lang = getLang();
  const meaning = (word.meaning && (word.meaning[lang] || word.meaning.en)) || "";
  const revealed = srsSession.revealed;
  const cardRec = srsLoad()[hanzi] || { state: "new" };
  const stateLabel = srsStateLabel(cardRec);
  const stateColor = ({ new: "#5CD68E", learning: "#FFB84D", review: "#66B2FF", relearning: "#FF6B6B" }[cardRec.state || "new"]) || "#8B9AAB";
  const previews = srsPreviewIntervals(cardRec);

  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">🔁 ${tU("srs_title")}</span></div>
    <div style="color:#8B9AAB;font-size:13px;margin-top:8px;text-align:center;display:flex;justify-content:center;gap:12px;align-items:center">
      <span>${srsSession.done} / ${srsSession.total}</span>
      <span style="padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;background:${stateColor}22;color:${stateColor};border:1px solid ${stateColor}">${stateLabel}</span>
    </div>
    <div class="content-card" style="margin-top:20px;text-align:center;padding:40px 20px;min-height:280px">
      <div style="font-size:64px;font-weight:700;letter-spacing:4px">${escapeHtml(word.hanzi)}</div>
      ${revealed ? `
        <div style="font-size:22px;color:#8B9AAB;margin-top:12px">${escapeHtml(word.pinyin)}</div>
        <div style="font-size:14px;color:#8B9AAB;margin-top:4px">${escapeHtml(word.pos)}</div>
        <div style="font-size:22px;color:#66B2FF;margin-top:16px">${escapeHtml(meaning)}</div>
      ` : ""}
    </div>
    <div id="actions" style="margin-top:20px"></div>`;

  document.getElementById("back").addEventListener("click", () => {
    srsSession = null;
    navigate("menu");
  });

  const actions = document.getElementById("actions");
  if (!revealed) {
    const b = document.createElement("button");
    b.textContent = tU("srs_reveal");
    b.style.cssText = "width:100%;padding:16px;border-radius:12px;background:#4a9eff;color:#fff;border:0;font-size:16px;cursor:pointer;font-weight:600";
    b.addEventListener("click", () => { srsSession.revealed = true; srsRenderCard(); });
    actions.appendChild(b);
  } else {
    const row = document.createElement("div");
    row.style.cssText = "display:grid;grid-template-columns:repeat(4,1fr);gap:8px";
    const btnData = [
      { label: tU("srs_again"), color: "#FF6B6B", r: 1, prev: previews.again },
      { label: tU("srs_hard"),  color: "#FFB84D", r: 2, prev: previews.hard  },
      { label: tU("srs_good"),  color: "#5CD68E", r: 3, prev: previews.good  },
      { label: tU("srs_easy"),  color: "#4a9eff", r: 4, prev: previews.easy  },
    ];
    for (const { label, color, r, prev } of btnData) {
      const b = document.createElement("button");
      b.innerHTML = `<div style="font-size:14px;font-weight:600">${label}</div><div style="font-size:11px;color:${color}88;margin-top:2px">${prev}</div>`;
      b.style.cssText =
        `padding:14px 8px;border-radius:10px;border:1px solid ${color};` +
        `background:${color}22;color:${color};cursor:pointer;font-weight:600`;
      b.addEventListener("click", () => {
        const updated = srsApplyRating(hanzi, r);
        markActivity(1);
        const stillLearning = updated.state === "learning" || updated.state === "relearning";
        if (stillLearning) {
          const pos = Math.min(3, srsSession.queue.length - 1);
          srsSession.queue.splice(pos + 1, 0, hanzi);
        } else {
          srsSession.done++;
        }
        srsSession.queue.shift();
        srsSession.revealed = false;
        srsRenderCard();
      });
      row.appendChild(b);
    }
    actions.appendChild(row);
  }
}

// ============================================================
// Экран урока
// ============================================================
const TABS = [
  { key: "tab_text", id: "text" }, { key: "tab_vocab", id: "vocab" },
  { key: "tab_grammar", id: "grammar" }, { key: "tab_phrases", id: "phrases" },
  { key: "tab_compare", id: "compare" }, { key: "tab_exercise", id: "exercise" },
  { key: "tab_extend", id: "extend" }, { key: "tab_apply", id: "apply" },
];
let currentLesson = null, currentTab = "text";

async function renderLesson(unit, index) {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div id="lesson-content" class="loading">${t("loading")}</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("lessons"));
  try {
    const r = await fetch(`/api/lessons/${unit}/${index}`);
    if (!r.ok) throw new Error("Урок не найден");
    currentLesson = await r.json();
    currentLesson.unit = unit;
    currentLesson.index = index;
    currentTab = "text";
    markLessonOpened(unit, index);
    drawLesson();
  } catch (e) {
    document.getElementById("lesson-content").innerHTML =
      `<div style="color:#FF6B6B">Ошибка: ${e.message}</div>`;
  }
}

function drawLesson() {
  const L = currentLesson;
  const color = UNIT_COLORS[L.unit] || "#3A6088";
  const zh = (L.title && L.title.zh) || "";
  const tr = (L.title && (L.title[getLang()] || L.title.en)) || "";
  const cont = document.getElementById("lesson-content");
  cont.classList.remove("loading");
  cont.innerHTML = `
    <div class="lesson-header">
      <div class="lesson-badge" style="background:${color}">${L.unit}.${L.index}</div>
      <div class="lesson-titles-block">
        <div class="lesson-zh-big">${zh}</div>
        <div class="lesson-tr-big">${tr}</div>
      </div>
    </div>
    <div class="tabs-bar" id="tabs-bar"></div>
    <div class="tab-content" id="tab-content"></div>`;
  const tb = document.getElementById("tabs-bar");
  for (const tab of TABS) {
    const b = document.createElement("button");
    b.className = "tab-btn" + (tab.id === currentTab ? " active" : "");
    b.textContent = t(tab.key);
    b.addEventListener("click", () => { currentTab = tab.id; drawLesson(); });
    tb.appendChild(b);
  }
  const c = document.getElementById("tab-content");
  const fn = { text: tabText, vocab: tabVocab, grammar: tabGrammar, phrases: tabPhrases,
    compare: tabCompare, exercise: tabExercise, extend: tabExtend, apply: tabApply }[currentTab];
  if (fn) fn(c);
}

let currentAudio = null;

function tabText(c) {
  const L = currentLesson, lang = getLang();
  const tr = (L.text_translation && L.text_translation[lang]) || "";
  const w = document.createElement("div");
  w.className = "content-card";
  w.innerHTML = `
    <div class="audio-controls" style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:18px">
      <button id="btn-play"
              style="padding:10px 20px;border-radius:10px;background:#4a9eff;color:#fff;border:0;cursor:pointer;font-size:16px;font-weight:600;display:flex;align-items:center;gap:8px">
        <span id="play-icon" style="font-size:18px">▶</span>
        <span id="play-label">Play</span>
      </button>

      <button id="btn-back"
              style="padding:10px 16px;border-radius:10px;background:#2a3f5a;color:#fff;border:0;cursor:pointer;font-size:14px;font-weight:600">
        ⟲ 5s
      </button>
      <button id="btn-fwd"
              style="padding:10px 16px;border-radius:10px;background:#2a3f5a;color:#fff;border:0;cursor:pointer;font-size:14px;font-weight:600">
        5s ⟳
      </button>

      <div style="margin-left:auto;display:flex;gap:6px;align-items:center">
        <span style="font-size:13px;color:#8B9AAB;margin-right:4px">Speed:</span>
        <span id="speed-btns" style="display:flex;gap:4px"></span>
      </div>
    </div>

    <div class="text-zh">${escapeHtml(L.text_zh || "")}</div>
    <div class="text-tr">${escapeHtml(tr)}</div>`;
  c.appendChild(w);

  const audioUrl = `/audio/unit${L.unit}/lesson${String(L.index).padStart(2, "0")}/textbook_1.mp3`;
  const btnPlay = document.getElementById("btn-play");
  const icon = document.getElementById("play-icon");
  const label = document.getElementById("play-label");
  const btnBack = document.getElementById("btn-back");
  const btnFwd = document.getElementById("btn-fwd");
  const speedWrap = document.getElementById("speed-btns");

  // останавливаем предыдущий
  if (currentAudio) {
    currentAudio.pause();
    currentAudio = null;
  }
  icon.textContent = "▶";
  label.textContent = "Play";

  // скорость — из localStorage
  let speed = parseFloat(localStorage.getItem("hsk5_audio_speed") || "1.0");
  if (![0.5, 1.0, 1.5, 2.0].includes(speed)) speed = 1.0;

  function drawSpeeds() {
    speedWrap.innerHTML = "";
    for (const s of [0.5, 1.0, 1.5, 2.0]) {
      const b = document.createElement("button");
      b.textContent = s.toFixed(1) + "x";
      const active = Math.abs(s - speed) < 0.001;
      b.style.cssText =
        `padding:6px 10px;border-radius:8px;font-size:13px;cursor:pointer;` +
        `border:1px solid ${active ? "#66B2FF" : "#444"};` +
        `background:${active ? "#4a9eff" : "transparent"};color:#fff`;
      b.addEventListener("click", () => {
        speed = s;
        localStorage.setItem("hsk5_audio_speed", String(speed));
        if (currentAudio) currentAudio.playbackRate = speed;
        drawSpeeds();
      });
      speedWrap.appendChild(b);
    }
  }
  drawSpeeds();

  btnPlay.addEventListener("click", () => {
    if (currentAudio && !currentAudio.paused) {
      currentAudio.pause();
      icon.textContent = "▶";
      label.textContent = "Play";
      return;
    }
    if (!currentAudio) {
      currentAudio = new Audio(audioUrl);
      currentAudio.playbackRate = speed;
      currentAudio.addEventListener("ended", () => {
        icon.textContent = "▶";
        label.textContent = "Play";
      });
      currentAudio.addEventListener("error", () => {
        icon.textContent = "⚠";
        label.textContent = "Audio not available";
      });
    }
    currentAudio.play().then(() => {
      icon.textContent = "⏸";
      label.textContent = "Pause";
    }).catch(err => {
      icon.textContent = "⚠";
      label.textContent = "Cannot play audio";
      console.error("audio error:", err);
    });
  });

  btnBack.addEventListener("click", () => {
    if (!currentAudio) return;
    currentAudio.currentTime = Math.max(0, currentAudio.currentTime - 5);
  });

  btnFwd.addEventListener("click", () => {
    if (!currentAudio) return;
    const dur = currentAudio.duration || 1e9;
    currentAudio.currentTime = Math.min(dur, currentAudio.currentTime + 5);
  });
}
function tabVocab(c) {
  const L = currentLesson, lang = getLang(), words = L.vocabulary || [];
  const w = document.createElement("div");
  w.className = "content-card";
  w.innerHTML = `
    <div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:14px">
      <div class="content-card-title" style="margin:0">生词 · ${words.length} ${t("vocab_words")}</div>
      <button id="vocab-play-all"
              style="margin-left:auto;padding:10px 18px;border-radius:10px;background:#4a9eff;color:#fff;
                     border:0;cursor:pointer;font-size:14px;font-weight:600;display:flex;align-items:center;gap:6px">
        <span id="vpa-icon" style="font-size:16px">▶</span>
        <span id="vpa-label">Play all words</span>
      </button>
    </div>
    <table class="vocab-table"><thead><tr>
      <th style="width:40px"></th>
      <th style="width:90px">${t("vocab_col_hanzi")}</th>
      <th style="width:130px">${t("vocab_col_pinyin")}</th>
      <th style="width:70px">${t("vocab_col_pos")}</th>
      <th>${t("vocab_col_trans")}</th></tr></thead><tbody></tbody></table>`;
  const tbody = w.querySelector("tbody");

  for (const v of words) {
    const tr = (v.meaning && (v.meaning[lang] || v.meaning.en)) || "";
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>
        <button class="word-audio-btn" data-hanzi="${escapeHtml(v.hanzi || "")}"
                style="padding:4px 8px;border-radius:6px;background:transparent;color:#66B2FF;
                       border:1px solid #4a6a8a;cursor:pointer;font-size:14px">🔊</button>
      </td>
      <td class="cell-hanzi">${escapeHtml(v.hanzi || "")}</td>
      <td class="cell-pinyin">${escapeHtml(v.pinyin || "")}</td>
      <td class="cell-pos">${escapeHtml(v.pos || "")}</td>
      <td>${escapeHtml(tr)}</td>`;
    tbody.appendChild(row);
  }
  c.appendChild(w);

  // === Аудиоплеер ===
  const audioUrl = `/audio/unit${L.unit}/lesson${String(L.index).padStart(2, "0")}/vocab.mp3`;
  const btn = document.getElementById("vocab-play-all");
  const icon = document.getElementById("vpa-icon");
  const label = document.getElementById("vpa-label");

  if (currentAudio) { currentAudio.pause(); currentAudio = null; }
  icon.textContent = "▶"; label.textContent = "Play all words";

  btn.addEventListener("click", () => {
    if (currentAudio && !currentAudio.paused) {
      currentAudio.pause();
      icon.textContent = "▶"; label.textContent = "Play all words";
      return;
    }
    if (!currentAudio) {
      currentAudio = new Audio(audioUrl);
      currentAudio.addEventListener("ended", () => {
        icon.textContent = "▶"; label.textContent = "Play all words";
      });
      currentAudio.addEventListener("error", () => {
        icon.textContent = "⚠"; label.textContent = "Audio not available";
      });
    }
    currentAudio.play().then(() => {
      icon.textContent = "⏸"; label.textContent = "Pause";
    }).catch(err => {
      icon.textContent = "⚠"; label.textContent = "Cannot play";
      console.error(err);
    });
  });

  // кнопки 🔊 на каждой строке — играют mp3 только этого слова
  w.querySelectorAll(".word-audio-btn").forEach(b => {
    b.addEventListener("click", (ev) => {
      ev.stopPropagation();
      const hanzi = b.dataset.hanzi || "";
      if (!hanzi) return;
      const wordUrl = "/audio/words/" + encodeURIComponent(hanzi) + ".mp3";

      // лёгкая подсветка кнопки
      const oldBg = b.style.background;
      b.style.background = "rgba(74,158,255,0.4)";
      setTimeout(() => { b.style.background = oldBg; }, 400);

      const a = new Audio(wordUrl);
      a.addEventListener("error", () => {
        console.warn("no audio for word:", hanzi);
      });
      a.play().catch(err => console.warn("play error:", err));
    });
  });
}

function renderGrammarCard(g, lang, ex, exs) {
  let html = `<div class="grammar-head">
      <span class="grammar-word">${escapeHtml(g.word || "")}</span>
      <span class="grammar-pos">${escapeHtml(g.pos || "")}</span></div>
    <div class="grammar-expl">${escapeHtml(ex)}</div>${exs}`;

  const fm = (g.formula || {})[lang] || (g.formula || {}).ru || (g.formula || {}).en || "";
  if (fm) {
    html += `<div class="grammar-block" style="margin-top:12px;padding:10px 12px;background:rgba(80,180,220,0.07);border-left:3px solid #4CB8DC;border-radius:6px"><div style="font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:#7EE0FF;margin-bottom:6px">\u{1F4D0} \u0424\u043E\u0440\u043C\u0443\u043B\u0430</div><div style="font-family:Menlo,Consolas,monospace;font-size:14px;color:#D9E6F2;white-space:pre-wrap">${escapeHtml(fm)}</div></div>`;
  }

  const wtu = (g.when_to_use || {})[lang] || (g.when_to_use || {}).ru || (g.when_to_use || {}).en || [];
  if (wtu && wtu.length) {
    const items = wtu.map(s => `<li style="margin:3px 0">${escapeHtml(s)}</li>`).join("");
    html += `<div class="grammar-block" style="margin-top:10px;padding:10px 12px;background:rgba(140,220,140,0.06);border-left:3px solid #56C271;border-radius:6px"><div style="font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:#7EE39A;margin-bottom:6px">\u{1F4CD} \u041A\u043E\u0433\u0434\u0430 \u0438\u0441\u043F\u043E\u043B\u044C\u0437\u043E\u0432\u0430\u0442\u044C</div><ul style="margin:0;padding-left:18px;color:#D9E6F2;font-size:14px">${items}</ul></div>`;
  }

  if (g.common_mistakes && g.common_mistakes.length) {
    const items = g.common_mistakes.map(m => {
      const why = (m.why || {})[lang] || (m.why || {}).ru || (m.why || {}).en || "";
      return `<li style="margin:6px 0"><div style="color:#FF8080">\u274C ${escapeHtml(m.wrong || "")}</div><div style="color:#8AE38A">\u2705 ${escapeHtml(m.right || "")}</div>${why ? `<div style="color:#A6B4C2;font-size:13px;margin-top:2px">${escapeHtml(why)}</div>` : ""}</li>`;
    }).join("");
    html += `<div class="grammar-block" style="margin-top:10px;padding:10px 12px;background:rgba(220,90,90,0.06);border-left:3px solid #E06A6A;border-radius:6px"><div style="font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:#FF9090;margin-bottom:6px">\u26A0\uFE0F \u0422\u0438\u043F\u0438\u0447\u043D\u044B\u0435 \u043E\u0448\u0438\u0431\u043A\u0438</div><ul style="margin:0;padding-left:18px">${items}</ul></div>`;
  }

  if (g.comparison_with && g.comparison_with.length) {
    const items = g.comparison_with.map(c => {
      const d = (c.difference || {})[lang] || (c.difference || {}).ru || (c.difference || {}).en || "";
      return `<li style="margin:6px 0"><div style="color:#F0C674;font-weight:600">\u2194\uFE0F ${escapeHtml(c.word || "")}</div><div style="color:#D9E6F2;font-size:13px;margin-top:2px">${escapeHtml(d)}</div></li>`;
    }).join("");
    html += `<div class="grammar-block" style="margin-top:10px;padding:10px 12px;background:rgba(240,200,100,0.06);border-left:3px solid #E0B85A;border-radius:6px"><div style="font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:#F0C674;margin-bottom:6px">\u2696\uFE0F \u0421\u0440\u0430\u0432\u043D\u0435\u043D\u0438\u0435</div><ul style="margin:0;padding-left:18px">${items}</ul></div>`;
  }

  if (g.exercises && g.exercises.length) {
    const items = g.exercises.map((x, i) => {
      const q = x.question || "";
      const a = x.answer || "";
      return `<li style="margin:8px 0;list-style:none;padding-left:0"><div style="color:#D9E6F2">${i+1}. ${escapeHtml(q)}</div><details style="margin-top:4px"><summary style="cursor:pointer;color:#7EE0FF;font-size:13px">\u041F\u043E\u043A\u0430\u0437\u0430\u0442\u044C \u043E\u0442\u0432\u0435\u0442</summary><div style="color:#8AE38A;margin-top:4px">\u2192 ${escapeHtml(a)}</div></details></li>`;
    }).join("");
    html += `<div class="grammar-block" style="margin-top:10px;padding:10px 12px;background:rgba(80,140,220,0.06);border-left:3px solid #5A96D6;border-radius:6px"><div style="font-size:12px;text-transform:uppercase;letter-spacing:0.5px;color:#8EC8FF;margin-bottom:6px">\u270F\uFE0F \u0423\u043F\u0440\u0430\u0436\u043D\u0435\u043D\u0438\u044F</div><ul style="margin:0;padding-left:0">${items}</ul></div>`;
  }

  return html;
}

function tabGrammar(c) {
  const L = currentLesson, lang = getLang();
  for (const g of (L.grammar || [])) {
    const card = document.createElement("div");
    card.className = "grammar-card";
    const ex = (g.explanation && (g.explanation[lang] || g.explanation.en)) || "";
    let exs = "";
    for (let i = 0; i < (g.examples || []).length; i++) {
      const e = g.examples[i], eTr = e[lang] || e.en || "";
      exs += `<div class="grammar-example">
        <div class="ex-zh">${i + 1}. ${escapeHtml(e.zh || "")}</div>
        <div class="ex-tr">${escapeHtml(eTr)}</div></div>`;
    }
    card.innerHTML = renderGrammarCard(g, lang, ex, exs);
    c.appendChild(card);
  }
}
function tabPhrases(c) {
  const L = currentLesson;
  for (const col of (L.collocations || [])) {
    const w = document.createElement("div");
    w.className = "phrases-card";
    let it = "";
    for (const i of (col.items || [])) it += `<div class="phrase-item">${escapeHtml(i)}</div>`;
    w.innerHTML = `<div class="phrases-pattern">${escapeHtml(col.pattern || "")}</div>${it}`;
    c.appendChild(w);
  }
}
function tabCompare(c) {
  const L = currentLesson, lang = getLang();
  for (const cp of (L.comparisons || [])) {
    const w = document.createElement("div");
    w.className = "compare-card";
    const cm = (cp.common && (cp.common[lang] || cp.common.en)) || "";
    let d = "";
    for (const x of (cp.differences || [])) {
      d += `<div class="compare-diff-item">${escapeHtml(x[lang] || x.en || "")}</div>`;
    }
    w.innerHTML = `<div class="compare-head">${escapeHtml(cp.word_a || "")} vs ${escapeHtml(cp.word_b || "")}</div>
      <div class="compare-common">≈ ${t("common")}</div>
      <div class="compare-common-text">${escapeHtml(cm)}</div>
      <div class="compare-diff-title">≠ ${t("differences")}</div>${d}`;
    c.appendChild(w);
  }
}
function tabExercise(c) {
  const L = currentLesson;
  const items = [
    { i: "🎧", t: t("listen"), s: `${(L.workbook && L.workbook.listening || []).length} ${t("questions")}` },
    { i: "📖", t: t("reading"), s: `${(L.workbook && L.workbook.reading || []).length} ${t("questions")}` },
    { i: "✍", t: t("writing"), s: `${(L.workbook && L.workbook.writing || []).length} ${t("tasks")}` },
  ];
  for (const x of items) {
    const e = document.createElement("div");
    e.className = "exercise-item";
    e.innerHTML = `<div class="exercise-icon">${x.i}</div>
      <div><div class="exercise-title">${x.t}</div>
      <div class="exercise-sub">${x.s}</div></div>
      <div class="card-chevron" style="margin-left:auto">›</div>`;
    e.addEventListener("click", () => alert("Появится в следующих итерациях"));
    c.appendChild(e);
  }
}
function tabExtend(c) {
  const L = currentLesson, lang = getLang();
  const exp = L.expansion || {};
  if (!exp.words || !exp.words.length) {
    c.innerHTML = `<div class="loading">—</div>`; return;
  }
  const w = document.createElement("div");
  w.className = "content-card";
  const topic = (exp.topic && (exp.topic[lang] || exp.topic.en)) || "";
  let h = topic ? `<div class="extend-topic">${escapeHtml(topic)}</div>` : "";
  for (const x of exp.words) {
    const m = (x.meaning && (x.meaning[lang] || x.meaning.en)) || "";
    h += `<div class="extend-word">
      <div class="extend-hanzi">${escapeHtml(x.hanzi || "")}</div>
      <div class="extend-pinyin">${escapeHtml(x.pinyin || "")}</div>
      <div class="extend-meaning">${escapeHtml(m)}</div></div>`;
  }
  w.innerHTML = h;
  c.appendChild(w);
}
function tabApply(c) {
  const L = currentLesson, lang = getLang();
  const a = L.application || {};
  const d = (a.discussion && (a.discussion[lang] || a.discussion.en)) || "";
  const w = document.createElement("div");
  w.className = "content-card";
  w.innerHTML = `<div class="content-card-title">🎓 ${t("tab_apply").replace(/^[^\s]+\s*/, "")}</div>
    <div class="apply-question">${escapeHtml(d)}</div>`;
  c.appendChild(w);
}

// ============================================================
// Обратная связь
// ============================================================
function renderFeedback() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">✉ ${tFb("page_title")}</span></div>
    <div class="version">${tFb("hint")}</div>
    <div class="content-card" style="max-width:640px;margin:20px auto">
      <div class="content-card-title">${tFb("name")}</div>
      <input id="fb-name" type="text" placeholder="${tFb("name_ph")}"
             style="width:100%;padding:10px;border-radius:8px;border:1px solid #444;background:#0e1620;color:#fff;font-size:15px;margin-bottom:14px;box-sizing:border-box">
      <div class="content-card-title">${tFb("message")}</div>
      <textarea id="fb-message" rows="6" placeholder="${tFb("message_ph")}"
                style="width:100%;padding:10px;border-radius:8px;border:1px solid #444;background:#0e1620;color:#fff;font-size:15px;resize:vertical;box-sizing:border-box"></textarea>
      <button id="fb-send"
              style="margin-top:14px;padding:12px 24px;border-radius:10px;background:#4a9eff;color:#fff;border:0;font-size:16px;cursor:pointer;font-weight:600">
        ${tFb("send")}</button>
      <div id="fb-status" style="margin-top:12px;font-size:14px"></div>
    </div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  document.getElementById("fb-send").addEventListener("click", async () => {
    const n = document.getElementById("fb-name").value;
    const m = document.getElementById("fb-message").value;
    const s = document.getElementById("fb-status");
    if (!m.trim()) { s.style.color = "#FF6B6B"; s.textContent = tFb("empty"); return; }
    s.style.color = "#8B9AAB"; s.textContent = tFb("sending");
    try {
      const r = await fetch("/api/feedback", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: n, message: m }),
      });
      if (r.ok) {
        s.style.color = "#5CD68E"; s.textContent = tFb("sent");
        document.getElementById("fb-message").value = "";
      } else {
        s.style.color = "#FF6B6B"; s.textContent = tFb("error");
      }
    } catch (e) {
      s.style.color = "#FF6B6B"; s.textContent = tFb("error");
    }
  });
}


// ============================================================
// ПРОФИЛЬ
// ============================================================
function renderProfile() {
  const u = window.HSK_USER || {};
  const s = lsGet(LS.settings, {});
  const act = lsGet(LS.activity, {});
  const lessons = lsGet(LS.lessons, []);
  const srs = lsGet(LS.srs, {});

  let actions = 0;
  for (const c of Object.values(act)) actions += c;
  let streak = 0;
  const d = new Date();
  while (true) {
    const s2 = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;
    if (act[s2]) { streak++; d.setDate(d.getDate()-1); } else break;
  }

  const created = u.created_at ? u.created_at.slice(0, 10) : "—";

  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">👤 Профиль</span></div>
    <div class="content-card" style="max-width:600px;margin:20px auto;padding:30px">
      <div style="display:flex;align-items:center;gap:20px;margin-bottom:26px">
        <div style="width:76px;height:76px;border-radius:50%;background:linear-gradient(135deg,#4a9eff,#66B2FF);display:flex;align-items:center;justify-content:center;font-size:40px">
          ${u.avatar || "👤"}
        </div>
        <div>
          <div style="font-size:24px;font-weight:700">${escapeHtml(u.name || "")}</div>
          <div style="color:#8B9AAB;font-size:14px;margin-top:4px">${escapeHtml(u.email || "")}</div>
          ${u.is_admin ? '<div style="color:#FFB84D;font-size:12px;margin-top:4px">👑 Администратор</div>' : ''}
        </div>
      </div>

      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:14px">
        <div>
          <div style="font-size:22px;font-weight:700;color:#66B2FF">${lessons.length} / 18</div>
          <div style="font-size:12px;color:#8B9AAB">Уроков открыто</div>
        </div>
        <div>
          <div style="font-size:22px;font-weight:700;color:#66B2FF">${Object.keys(srs).length}</div>
          <div style="font-size:12px;color:#8B9AAB">Слов в SRS</div>
        </div>
        <div>
          <div style="font-size:22px;font-weight:700;color:#FFB84D">${streak} 🔥</div>
          <div style="font-size:12px;color:#8B9AAB">Стрик</div>
        </div>
        <div>
          <div style="font-size:22px;font-weight:700;color:#5CD68E">${actions}</div>
          <div style="font-size:12px;color:#8B9AAB">Всего действий</div>
        </div>
      </div>

      <div style="margin-top:26px;font-size:13px;color:#8B9AAB">
        Зарегистрирован: ${created}
      </div>

      <button id="p-edit" style="margin-top:20px;padding:10px 20px;border-radius:8px;background:transparent;color:#66B2FF;border:1px solid #66B2FF;cursor:pointer;font-size:14px">
        Редактировать профиль
      </button>

      <button id="p-out" style="margin-top:12px;margin-left:8px;padding:10px 20px;border-radius:8px;background:transparent;color:#FF6B6B;border:1px solid #FF6B6B;cursor:pointer;font-size:14px">
        Выйти
      </button>
    </div>`;

  document.getElementById("back").addEventListener("click", () => navigate("menu"));
  document.getElementById("p-out").addEventListener("click", () => {
    if (confirm("Выйти из аккаунта?")) HSKAuth.logout();
  });
  document.getElementById("p-edit").addEventListener("click", () => {
    if (typeof showEditProfile === "function") showEditProfile();
  });
}


// ============================================================
// АДМИН-ПАНЕЛЬ
// ============================================================
async function renderAdmin() {
  const u = window.HSK_USER || {};
  if (!u.is_admin) {
    app.innerHTML = `<div class="content-card" style="margin:40px auto;max-width:500px;text-align:center">
      <div style="font-size:48px">🔒</div>
      <div style="margin-top:14px">Доступ только для администратора</div></div>`;
    return;
  }
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">👑 Пользователи</span></div>
    <div id="content" class="loading">${t("loading")}</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));

  const r = await fetch("/api/admin/users", { credentials: "same-origin" });
  if (!r.ok) {
    document.getElementById("content").innerHTML =
      `<div style="color:#FF6B6B;padding:20px">Не удалось загрузить</div>`;
    return;
  }
  const j = await r.json();
  const users = j.users || [];
  const content = document.getElementById("content");
  content.classList.remove("loading");

  const totalUsers = users.length;
  const activeUsers = users.filter(x => x.activated).length;
  const admins = users.filter(x => x.is_admin).length;

  content.innerHTML = `
    <div class="content-card" style="margin-top:14px">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:14px;margin-bottom:20px">
        <div><div style="font-size:26px;font-weight:700;color:#66B2FF">${totalUsers}</div>
             <div style="font-size:12px;color:#8B9AAB">Всего</div></div>
        <div><div style="font-size:26px;font-weight:700;color:#5CD68E">${activeUsers}</div>
             <div style="font-size:12px;color:#8B9AAB">Активировано</div></div>
        <div><div style="font-size:26px;font-weight:700;color:#FFB84D">${admins}</div>
             <div style="font-size:12px;color:#8B9AAB">Админов</div></div>
      </div>
      <table class="vocab-table" id="users-table">
        <thead><tr>
          <th>Пользователь</th>
          <th>Email</th>
          <th style="width:100px">Дата</th>
          <th style="width:70px">Ключей</th>
          <th style="width:90px">Статус</th>
          <th style="width:70px"></th>
        </tr></thead><tbody></tbody>
      </table>
    </div>`;

  const tbody = content.querySelector("tbody");
  for (const x of users) {
    const tr = document.createElement("tr");
    const created = (x.created_at || "").slice(0, 10);
    const seen = x.last_seen ? x.last_seen.slice(0, 10) : "—";
    tr.innerHTML = `
      <td>
        <span style="font-size:20px;margin-right:6px">${x.avatar || "👤"}</span>
        <b>${escapeHtml(x.name)}</b>
        ${x.is_admin ? '<span style="color:#FFB84D;font-size:11px;margin-left:6px">👑</span>' : ''}
      </td>
      <td style="font-size:13px;color:#8B9AAB">${escapeHtml(x.email)}</td>
      <td style="font-size:12px;color:#8B9AAB">${created}</td>
      <td style="font-size:12px;color:#8B9AAB">${x.progress_keys || 0}</td>
      <td style="font-size:12px;color:${x.activated ? "#5CD68E" : "#FFB84D"}">
        ${x.activated ? "✓ активен" : "⏳ не активирован"}</td>
      <td>
        ${!x.is_admin ? `<button class="del-user" data-id="${x.id}" data-name="${escapeHtml(x.name)}"
          style="padding:4px 10px;border-radius:6px;background:transparent;color:#FF6B6B;
                 border:1px solid #FF6B6B;cursor:pointer;font-size:12px">Удалить</button>` : ""}
      </td>`;
    tbody.appendChild(tr);
  }

  content.querySelectorAll(".del-user").forEach(btn => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      const nm = btn.dataset.name;
      if (!confirm(`Удалить пользователя "${nm}" и весь его прогресс?`)) return;
      const r = await fetch(`/api/admin/users/${id}`, {
        method: "DELETE", credentials: "same-origin",
      });
      if (r.ok) {
        btn.closest("tr").remove();
      } else {
        const j = await r.json();
        alert(j.error || "Не удалось");
      }
    });
  });
}

// ============================================================
// ЗАБЫЛИ ПАРОЛЬ
// ============================================================
function renderForgot() {
  app.innerHTML = `
    <div class="auth-wrap">
      <div class="auth-logo">Сброс пароля</div>
      <div class="auth-sub">Введи email — пришлём ссылку для сброса</div>
      <label class="auth-label">Email</label>
      <input id="fp-email" class="auth-input" type="email">
      <button id="fp-btn" class="auth-btn">Отправить ссылку</button>
      <button id="fp-back" class="auth-btn" style="background:transparent;color:#8B9AAB;font-weight:400;font-size:14px;padding:10px">
        ← Ко входу
      </button>
      <div id="fp-msg" class="auth-msg"></div>
    </div>`;
  const msg = document.getElementById("fp-msg");
  const email = document.getElementById("fp-email");
  const btn = document.getElementById("fp-btn");
  document.getElementById("fp-back").onclick = () => {
    window.location.hash = "";
    if (window.HSKAuth) window.HSKAuth.showAuthScreen("login");
  };
  btn.onclick = async () => {
    const e = email.value.trim();
    if (!e) return setAuthMsg(msg, "Введите email", "error");
    btn.disabled = true;
    setAuthMsg(msg, "Отправляю...", "info");
    const r = await fetch("/api/auth/forgot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: e }),
    });
    btn.disabled = false;
    const j = await r.json().catch(() => ({}));
    if (r.ok) setAuthMsg(msg, "Письмо отправлено. Проверьте почту.", "ok");
    else setAuthMsg(msg, j.error || "Ошибка", "error");
  };
}

function setAuthMsg(el, text, kind) {
  if (!el) return;
  el.className = "auth-msg " + (kind || "");
  el.textContent = text || "";
}

// ============================================================
// НОВЫЙ ПАРОЛЬ ПО ТОКЕНУ
// ============================================================
async function renderReset(token) {
  app.innerHTML = `
    <div class="auth-wrap">
      <div class="auth-logo">Новый пароль</div>
      <div class="auth-sub">Введи новый пароль для своего аккаунта</div>
      <label class="auth-label">Новый пароль (минимум 6 символов)</label>
      <input id="rs-pass" class="auth-input" type="password">
      <label class="auth-label">Повторите</label>
      <input id="rs-pass2" class="auth-input" type="password">
      <button id="rs-btn" class="auth-btn">Установить пароль</button>
      <div id="rs-msg" class="auth-msg"></div>
    </div>`;
  const msg = document.getElementById("rs-msg");
  const p1 = document.getElementById("rs-pass");
  const p2 = document.getElementById("rs-pass2");
  const btn = document.getElementById("rs-btn");
  btn.onclick = async () => {
    if (p1.value.length < 6) return setAuthMsg(msg, "Минимум 6 символов", "error");
    if (p1.value !== p2.value) return setAuthMsg(msg, "Пароли не совпадают", "error");
    btn.disabled = true;
    setAuthMsg(msg, "Сохраняю...", "info");
    const r = await fetch(`/api/auth/reset/${encodeURIComponent(token)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: p1.value }),
    });
    btn.disabled = false;
    const j = await r.json().catch(() => ({}));
    if (r.ok) {
      setAuthMsg(msg, "Пароль обновлён. Открываю...", "ok");
      window.HSK_USER = j.user;
      setTimeout(() => {
        window.location.hash = "menu";
        window.location.reload();
      }, 900);
    } else {
      setAuthMsg(msg, j.error || "Ошибка", "error");
    }
  };
}

// ============================================================
// РЕДАКТИРОВАНИЕ ПРОФИЛЯ
// ============================================================
const AVATAR_CHOICES = ["👤","🐱","🐼","🦊","🐯","🦁","🐸","🐧","🦉","🦄","🐲","👩","👨","🧑","👧","👦","🧠","📚","🎓","⭐"];
let editAvatar = null;

function showEditProfile() {
  const u = window.HSK_USER || {};
  editAvatar = u.avatar || "👤";
  const html = `
    <div id="edit-modal" style="position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:9999;display:flex;align-items:center;justify-content:center;padding:20px">
      <div style="background:#0e1620;border-radius:16px;padding:26px;max-width:440px;width:100%;max-height:90vh;overflow-y:auto;color:#F0F4F8">
        <h3 style="margin:0 0 20px;color:#66B2FF">Редактировать профиль</h3>
        <label class="auth-label">Имя</label>
        <input id="ep-name" class="auth-input" type="text" value="${escapeHtml(u.name || "")}" maxlength="60">
        <label class="auth-label" style="margin-top:14px;display:block">Аватар</label>
        <div id="ep-avatars" style="display:flex;flex-wrap:wrap;gap:6px;margin-top:8px"></div>
        <div id="ep-msg" class="auth-msg"></div>
        <div style="display:flex;gap:10px;margin-top:22px">
          <button id="ep-save" class="auth-btn" style="margin-top:0">Сохранить</button>
          <button id="ep-cancel" class="auth-btn" style="margin-top:0;background:#2a3f5a">Отмена</button>
        </div>
      </div>
    </div>`;
  document.body.insertAdjacentHTML("beforeend", html);

  const avatarWrap = document.getElementById("ep-avatars");
  function drawAvatars() {
    avatarWrap.innerHTML = "";
    for (const a of AVATAR_CHOICES) {
      const b = document.createElement("button");
      b.textContent = a;
      const active = a === editAvatar;
      b.style.cssText = `font-size:24px;padding:6px;width:44px;height:44px;cursor:pointer;` +
        `border-radius:10px;border:1px solid ${active ? "#66B2FF" : "#333"};` +
        `background:${active ? "rgba(74,158,255,0.2)" : "transparent"};color:#fff`;
      b.onclick = () => { editAvatar = a; drawAvatars(); };
      avatarWrap.appendChild(b);
    }
  }
  drawAvatars();

  const msg = document.getElementById("ep-msg");
  document.getElementById("ep-cancel").onclick = () => {
    document.getElementById("edit-modal").remove();
  };
  document.getElementById("ep-save").onclick = async () => {
    const nm = document.getElementById("ep-name").value.trim();
    if (!nm) return setAuthMsg(msg, "Имя не может быть пустым", "error");
    const btn = document.getElementById("ep-save");
    btn.disabled = true;
    setAuthMsg(msg, "Сохраняю...", "info");
    const r = await fetch("/api/auth/profile", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ name: nm, avatar: editAvatar }),
    });
    const j = await r.json().catch(() => ({}));
    btn.disabled = false;
    if (r.ok) {
      window.HSK_USER = j.user;
      document.getElementById("edit-modal").remove();
      navigate("profile");
    } else {
      setAuthMsg(msg, j.error || "Ошибка", "error");
    }
  };
}

// ============================================================
// Заглушка
// ============================================================
function renderPlaceholder(title) {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">${title}</span></div>
    <div class="loading" style="font-size:18px; padding-top:80px;">
      🚧 Этот раздел появится в следующих итерациях</div>`;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
}

// ============================================================
// Роутер
// ============================================================
function navigate(path) {
  const p = path.split("/");
  if (path === "menu" || path === "") renderMainMenu();
  else if (p[0] === "lessons") renderLessons();
  else if (p[0] === "lesson" && p.length === 3) {
    const u = parseInt(p[1], 10), i = parseInt(p[2], 10);
    if (Number.isFinite(u) && Number.isFinite(i)) renderLesson(u, i);
    else { renderLessons(); window.location.hash = "lessons"; return; }
  }
  else if (p[0] === "vocab") renderVocab();
  else if (p[0] === "grammar") renderGrammar();
  else if (p[0] === "compare") renderCompare();
  else if (p[0] === "analyzer") renderAnalyzer();
  else if (p[0] === "activity") renderActivity();
  else if (p[0] === "progress") renderProgress();
  else if (p[0] === "srs") renderSrs();
  else if (p[0] === "feedback") renderFeedback();
  else if (p[0] === "profile") renderProfile();
  else if (p[0] === "admin") renderAdmin();
  else if (p[0] === "forgot") renderForgot();
  else if (p[0] === "achievements") renderAchievements();
  else if (p[0] === "settings") renderSettings();
  else renderPlaceholder("? " + path);
  window.location.hash = path;
}

// ============================================================
// Хелпер
// ============================================================
function escapeHtml(s) {
  if (!s) return "";
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
    .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

// ============================================================
// Баннер об обновлениях (туркменский, красивое оформление)
// ============================================================
const HSK_BANNER_VERSION = "2026-09-24-audio";
const HSK_BANNER_KEY = "hsk5_banner_seen_" + HSK_BANNER_VERSION;

function ensureUpdateBannerStyles() {
  if (document.getElementById("hsk-update-styles")) return;
  const st = document.createElement("style");
  st.id = "hsk-update-styles";
  st.textContent = `
    #hsk-update-banner {
      position: fixed;
      top: 22px;
      left: 50%;
      transform: translate(-50%, -180%);
      z-index: 99999;
      transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.5s ease;
      opacity: 0;
      pointer-events: none;
    }
    #hsk-update-banner.show {
      transform: translate(-50%, 0);
      opacity: 1;
      pointer-events: auto;
    }
    #hsk-update-banner .ub-inner {
      position: relative;
      display: flex;
      gap: 16px;
      align-items: flex-start;
      padding: 20px 44px 20px 22px;
      border-radius: 16px;
      background: rgba(18, 28, 42, 0.96);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      box-shadow:
        0 14px 48px rgba(74, 158, 255, 0.4),
        0 0 0 1px rgba(102, 178, 255, 0.22) inset,
        0 1px 0 rgba(255, 255, 255, 0.08) inset;
      max-width: min(620px, calc(100vw - 32px));
      color: #F0F4F8;
      box-sizing: border-box;
      overflow: hidden;
    }
    #hsk-update-banner .ub-inner::before {
      content: "";
      position: absolute;
      inset: -1.5px;
      border-radius: 18px;
      padding: 1.5px;
      background: linear-gradient(135deg, #66B2FF, #5CD68E, #A56BFF, #FFB84D, #66B2FF);
      background-size: 400% 400%;
      -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      pointer-events: none;
      animation: hsk-ub-flow 5s linear infinite;
    }
    @keyframes hsk-ub-flow {
      0%   { background-position:   0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position:   0% 50%; }
    }
    #hsk-update-banner .ub-icon {
      font-size: 40px;
      line-height: 1;
      flex-shrink: 0;
      animation: hsk-ub-wiggle 1.8s ease-in-out infinite;
      filter: drop-shadow(0 0 12px rgba(102, 178, 255, 0.7));
    }
    @keyframes hsk-ub-wiggle {
      0%, 100% { transform: scale(1) rotate(-8deg); }
      50%      { transform: scale(1.15) rotate(8deg); }
    }
    #hsk-update-banner .ub-content {
      flex: 1;
      min-width: 0;
    }
    #hsk-update-banner .ub-title {
      font-weight: 800;
      font-size: 17px;
      letter-spacing: 0.3px;
      margin-bottom: 6px;
      background: linear-gradient(90deg, #66B2FF 0%, #5CD68E 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: #66B2FF;
    }
    #hsk-update-banner .ub-body {
      font-size: 14.5px;
      line-height: 1.55;
      color: #E4EDF5;
    }
    #hsk-update-banner .ub-body b { color: #66B2FF; }
    #hsk-update-banner .ub-close {
      position: absolute;
      top: 8px;
      right: 10px;
      background: transparent;
      border: 0;
      color: #8B9AAB;
      font-size: 18px;
      line-height: 1;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 6px;
      font-family: inherit;
    }
    #hsk-update-banner .ub-close:hover {
      background: rgba(255,255,255,0.08);
      color: #fff;
    }
    #hsk-update-banner .ub-progress {
      position: absolute;
      left: 0;
      bottom: 0;
      height: 3px;
      background: linear-gradient(90deg, #66B2FF, #5CD68E);
      border-radius: 0 0 0 16px;
      animation: hsk-ub-progress 14s linear forwards;
    }
    @keyframes hsk-ub-progress {
      from { width: 100%; opacity: 0.85; }
      to   { width: 0%;   opacity: 0.2; }
    }
    @media (max-width: 520px) {
      #hsk-update-banner { top: 12px; }
      #hsk-update-banner .ub-inner { padding: 16px 40px 16px 16px; gap: 12px; }
      #hsk-update-banner .ub-icon { font-size: 32px; }
      #hsk-update-banner .ub-title { font-size: 15px; }
      #hsk-update-banner .ub-body { font-size: 13.5px; }
    }
  `;
  document.head.appendChild(st);
}

function showUpdateBanner() {
  ensureUpdateBannerStyles();
  const el = document.createElement("div");
  el.id = "hsk-update-banner";
  el.innerHTML = `
    <div class="ub-inner">
      <div class="ub-icon">✨</div>
      <div class="ub-content">
        <div class="ub-title">Täze täzelikler!</div>
        <div class="ub-body">
          Indi <b>her sözi aýratyn</b> diňläp bilersiňiz — haýsy sözi bassaňyz, şol söz aýdylýar.<br>
          Hasaba girip, ösüşiňizi <b>ähli enjamlarda</b> saklaň!
        </div>
      </div>
      <button class="ub-close" aria-label="Close">✕</button>
      <div class="ub-progress"></div>
    </div>`;
  document.body.appendChild(el);

  requestAnimationFrame(() => {
    requestAnimationFrame(() => el.classList.add("show"));
  });

  let hideTimer = setTimeout(hide, 14000);

  function hide() {
    clearTimeout(hideTimer);
    el.classList.remove("show");
    setTimeout(() => el.remove(), 700);
    try { localStorage.setItem(HSK_BANNER_KEY, "1"); } catch (e) {}
  }

  el.querySelector(".ub-close").addEventListener("click", hide);
}

function maybeShowUpdateBanner() {
  try {
    if (localStorage.getItem(HSK_BANNER_KEY) === "1") return;
  } catch (e) { /* localStorage недоступен */ }
  setTimeout(showUpdateBanner, 500);
}

// ============================================================
// Старт
// ============================================================
window.addEventListener("lang_changed", () => {
  navigate(window.location.hash.slice(1) || "menu");
});
window.addEventListener("resize", () => {
  const c = document.getElementById("bg-pattern");
  if (c) { c.innerHTML = ""; c.dataset.drawn = "0"; }
  drawBackgroundPattern();
});
async function bootApp() {
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
    window.HSK_MODE = {
      guest_mode: !!j.guest_mode,
      registration_enabled: j.registration_enabled !== false,
    };
    if (!j.user) {
      if (typeof HSKAuth !== "undefined") HSKAuth.showAuthScreen("login");
      return;
    }
    window.HSK_USER = j.user;
    if (typeof HSKAuth !== "undefined" && !j.user.guest) {
      try { await HSKAuth.loadProgress(); } catch (e) {}
    }
    drawBackgroundPattern();
    navigate(window.location.hash.slice(1) || "menu");
    setTimeout(maybeShowUpdateBanner, 500);
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
