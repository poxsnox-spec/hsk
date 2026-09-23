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
    <button class="side-btn" id="btn-profile">
      <span style="font-size:18px">${(window.HSK_USER && window.HSK_USER.avatar) || "👤"}</span>
      <span>${(window.HSK_USER && window.HSK_USER.name) || "Профиль"}</span>
    </button>
    <button class="side-btn" id="btn-logout" style="color:#FF6B6B">
      <span style="font-size:18px">⎋</span>
      <span>Выйти</span>
    </button>
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

function srsLoad() { return lsGet(LS.srs, {}); }
function srsSave(data) { lsSet(LS.srs, data); }

function srsReview(hanzi, rating) {
  const db = srsLoad();
  let r = db[hanzi] || { ease: 2.5, interval: 0, reps: 0, lapses: 0, due: 0 };
  // rating: 1=again 2=hard 3=good 4=easy
  if (rating === 1) {
    r.interval = 0;
    r.reps = 0;
    r.lapses = (r.lapses || 0) + 1;
    r.ease = Math.max(1.3, r.ease - 0.2);
  } else {
    if (rating === 2) {
      r.interval = r.reps === 0 ? 1 : Math.max(1, Math.round(r.interval * 1.2));
      r.ease = Math.max(1.3, r.ease - 0.15);
    } else if (rating === 3) {
      r.interval = r.reps === 0 ? 1 : (r.reps === 1 ? 3 : Math.round(r.interval * r.ease));
      r.reps += 1;
    } else if (rating === 4) {
      r.interval = r.reps === 0 ? 2 : (r.reps === 1 ? 5 : Math.round(r.interval * r.ease * 1.3));
      r.ease = Math.min(3.0, r.ease + 0.15);
      r.reps += 1;
    }
    r.reps = r.reps || 1;
  }
  const now = Date.now();
  r.due = now + r.interval * 24 * 60 * 60 * 1000;
  db[hanzi] = r;
  srsSave(db);
  return r;
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
      });
      wrap.appendChild(b);
    }
  }
  drawSize();

  document.getElementById("start").addEventListener("click", () => {
    srsStartSession(size);
  });
}

function srsStartSession(size) {
  const db = srsLoad();
  const now = Date.now();
  // 1) сначала due-карточки
  let candidates = Object.entries(db)
    .filter(([_, r]) => (r.due || 0) <= now)
    .map(([h]) => h);
  // 2) если мало — добавляем новые слова
  const need = size - candidates.length;
  if (need > 0) {
    const all = vocabCache.map(w => w.hanzi).filter(Boolean);
    const fresh = all.filter(h => !db[h]);
    // перемешаем
    for (let i = fresh.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [fresh[i], fresh[j]] = [fresh[j], fresh[i]];
    }
    candidates = candidates.concat(fresh.slice(0, need));
  }
  candidates = candidates.slice(0, size);
  if (!candidates.length) {
    alert(tU("srs_all_done"));
    return;
  }
  srsSession = { queue: candidates, done: 0, total: candidates.length, revealed: false };
  srsRenderCard();
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
        <button id="ok" style="margin-top:24px;padding:12px 24px;border-radius:10px;background:#4a9eff;color:#fff;border:0;font-size:16px;cursor:pointer">
          OK</button>
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

  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header"><span class="app-name">🔁 ${tU("srs_title")}</span></div>
    <div style="color:#8B9AAB;font-size:13px;margin-top:8px;text-align:center">
      ${srsSession.done} / ${srsSession.total}
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
      { label: tU("srs_again"), color: "#FF6B6B", r: 1 },
      { label: tU("srs_hard"),  color: "#FFB84D", r: 2 },
      { label: tU("srs_good"),  color: "#5CD68E", r: 3 },
      { label: tU("srs_easy"),  color: "#4a9eff", r: 4 },
    ];
    for (const { label, color, r } of btnData) {
      const b = document.createElement("button");
      b.textContent = label;
      b.style.cssText =
        `padding:14px 8px;border-radius:10px;border:1px solid ${color};` +
        `background:${color}22;color:${color};font-size:14px;cursor:pointer;font-weight:600`;
      b.addEventListener("click", () => {
        srsReview(hanzi, r);
        markActivity(1);
        if (r === 1) {
          // опять — в конец очереди
          srsSession.queue.push(hanzi);
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
  w.innerHTML = `<div class="content-card-title">生词 · ${words.length} ${t("vocab_words")}</div>
    <table class="vocab-table"><thead><tr>
      <th style="width:90px">${t("vocab_col_hanzi")}</th>
      <th style="width:130px">${t("vocab_col_pinyin")}</th>
      <th style="width:70px">${t("vocab_col_pos")}</th>
      <th>${t("vocab_col_trans")}</th></tr></thead><tbody></tbody></table>`;
  const tbody = w.querySelector("tbody");
  for (const v of words) {
    const tr = (v.meaning && (v.meaning[lang] || v.meaning.en)) || "";
    const row = document.createElement("tr");
    row.innerHTML = `<td class="cell-hanzi">${escapeHtml(v.hanzi)}</td>
      <td class="cell-pinyin">${escapeHtml(v.pinyin)}</td>
      <td class="cell-pos">${escapeHtml(v.pos)}</td>
      <td>${escapeHtml(tr)}</td>`;
    tbody.appendChild(row);
  }
  c.appendChild(w);
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
    card.innerHTML = `<div class="grammar-head">
        <span class="grammar-word">${escapeHtml(g.word || "")}</span>
        <span class="grammar-pos">${escapeHtml(g.pos || "")}</span></div>
      <div class="grammar-expl">${escapeHtml(ex)}</div>${exs}`;
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
    alert("Редактирование появится позже");
  });
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
// Объявление при входе (туркменский, 5 сек, лимит 30 часов)
// ============================================================
function ensureAnnouncementStyles() {
  if (document.getElementById("hsk-announce-styles")) return;
  const st = document.createElement("style");
  st.id = "hsk-announce-styles";
  st.textContent = `
    #hsk-announcement {
      position: fixed;
      top: 24px;
      left: 50%;
      transform: translate(-50%, -160%);
      z-index: 9999;
      transition: transform 0.55s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.45s ease;
      opacity: 0;
      pointer-events: none;
    }
    #hsk-announcement.show {
      transform: translate(-50%, 0);
      opacity: 1;
    }
    #hsk-announcement .announce-inner {
      position: relative;
      display: flex;
      gap: 16px;
      align-items: center;
      padding: 18px 26px;
      border-radius: 16px;
      background: rgba(20, 32, 48, 0.94);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      box-shadow:
        0 12px 40px rgba(74, 158, 255, 0.35),
        0 0 0 1px rgba(102, 178, 255, 0.18) inset,
        0 1px 0 rgba(255, 255, 255, 0.06) inset;
      max-width: min(600px, calc(100vw - 40px));
      color: #F0F4F8;
      font-family: inherit;
      box-sizing: border-box;
    }
    #hsk-announcement .announce-inner::before {
      content: "";
      position: absolute;
      inset: -1px;
      border-radius: 17px;
      padding: 1.5px;
      background: linear-gradient(135deg, #66B2FF, #5CD68E, #A56BFF, #66B2FF);
      background-size: 300% 300%;
      -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      pointer-events: none;
      animation: hsk-border-flow 4s linear infinite;
    }
    @keyframes hsk-border-flow {
      0%   { background-position:   0% 50%; }
      50%  { background-position: 100% 50%; }
      100% { background-position:   0% 50%; }
    }
    #hsk-announcement .announce-icon {
      font-size: 38px;
      line-height: 1;
      flex-shrink: 0;
      animation: hsk-bounce 1.3s ease-in-out infinite;
      filter: drop-shadow(0 0 10px rgba(102, 178, 255, 0.6));
    }
    @keyframes hsk-bounce {
      0%, 100% { transform: scale(1) rotate(0); }
      50%      { transform: scale(1.18) rotate(-10deg); }
    }
    #hsk-announcement .announce-text {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    #hsk-announcement .announce-title {
      font-weight: 700;
      font-size: 16px;
      letter-spacing: 0.3px;
      background: linear-gradient(90deg, #66B2FF 0%, #5CD68E 100%);
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      color: #66B2FF;
    }
    #hsk-announcement .announce-body {
      font-size: 14.5px;
      line-height: 1.5;
      color: #E4EDF5;
    }
    @media (max-width: 500px) {
      #hsk-announcement { top: 14px; }
      #hsk-announcement .announce-inner { padding: 14px 18px; gap: 12px; }
      #hsk-announcement .announce-icon { font-size: 30px; }
      #hsk-announcement .announce-title { font-size: 15px; }
      #hsk-announcement .announce-body { font-size: 13.5px; }
    }
  `;
  document.head.appendChild(st);
}

function showAnnouncement() {
  ensureAnnouncementStyles();
  const el = document.createElement("div");
  el.id = "hsk-announcement";
  el.innerHTML = `
    <div class="announce-inner">
      <div class="announce-icon">🎉</div>
      <div class="announce-text">
        <div class="announce-title">Täze mümkinçilikler!</div>
        <div class="announce-body">
          Ähli bölümler işleýär — islendik dersiň tekstini diňläp bilersiňiz!
        </div>
      </div>
    </div>`;
  document.body.appendChild(el);
  // плавное появление
  requestAnimationFrame(() => {
    requestAnimationFrame(() => el.classList.add("show"));
  });
  // автоскрытие через 5 секунд
  setTimeout(() => {
    el.classList.remove("show");
    setTimeout(() => el.remove(), 700);
  }, 5000);
}

function maybeShowAnnouncement() {
  const KEY = "hsk5_announcement_start";
  const LIMIT_MS = 30 * 60 * 60 * 1000;  // 30 часов
  const now = Date.now();
  let start = parseInt(localStorage.getItem(KEY) || "0", 10);
  if (!start || start <= 0) {
    start = now;
    try { localStorage.setItem(KEY, String(start)); } catch (e) {}
  }
  if (now - start > LIMIT_MS) return;  // лимит истёк — больше не показываем
  showAnnouncement();
}

// ============================================================
// Старт
// ============================================================
drawBackgroundPattern();
navigate(window.location.hash.slice(1) || "menu");
setTimeout(maybeShowAnnouncement, 350);

window.addEventListener("lang_changed", () => {
  navigate(window.location.hash.slice(1) || "menu");
});
window.addEventListener("resize", () => {
  const c = document.getElementById("bg-pattern");
  if (c) { c.innerHTML = ""; c.dataset.drawn = "0"; }
  drawBackgroundPattern();
});
window.addEventListener("hashchange", () => {
async function bootApp() {
  const h = window.location.hash || "";
  if (h.startsWith("#activate/")) {
    const token = h.slice("#activate/".length);
    if (typeof HSKAuth !== "undefined") {
      await HSKAuth.doActivate(token);
      return;
    }
  }
  try {
    const r = await fetch("/api/auth/me", { credentials: "same-origin" });
    const j = await r.json();
    if (!j.user) {
      if (typeof HSKAuth !== "undefined") HSKAuth.showAuthScreen("login");
      return;
    }
    window.HSK_USER = j.user;
    if (typeof HSKAuth !== "undefined") await HSKAuth.loadProgress();
    navigate(window.location.hash.slice(1) || "menu");
  } catch (e) {
    document.getElementById("app").innerHTML =
      `<div style="padding:40px;color:#FF6B6B;font-size:14px">Ошибка соединения: ${e.message}</div>`;
  }
}
bootApp();
});