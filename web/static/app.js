// HSK 5 Learner — веб-версия
const app = document.getElementById("app");

// ============================================================
// Фоновый паттерн
// ============================================================
function drawBackgroundPattern() {
  const container = document.getElementById("bg-pattern");
  if (!container || container.dataset.drawn === "1") return;
  container.dataset.drawn = "1";

  const BG_CHARS = "汉字学习研究书道文心画意诗词歌赋";
  const MATH = "xyabfπ√∞θαβΔ";
  const w = window.innerWidth;
  const h = window.innerHeight;

  let seed = 42;
  const rnd = () => {
    seed = (seed * 16807) % 2147483647;
    return seed / 2147483647;
  };

  for (let i = 0; i < 30; i++) {
    const span = document.createElement("span");
    span.textContent = BG_CHARS[Math.floor(rnd() * BG_CHARS.length)];
    span.style.left = (rnd() * (w + 100) - 50) + "px";
    span.style.top = (rnd() * (h + 100) - 50) + "px";
    span.style.fontSize = (40 + rnd() * 90) + "px";
    container.appendChild(span);
  }
  for (let i = 0; i < 22; i++) {
    const span = document.createElement("span");
    span.className = "math";
    span.textContent = MATH[Math.floor(rnd() * MATH.length)];
    span.style.left = (rnd() * w) + "px";
    span.style.top = (rnd() * h) + "px";
    span.style.fontSize = (14 + rnd() * 16) + "px";
    container.appendChild(span);
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
    </div>
  `;

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
      <div class="card-chevron">›</div>
    `;
    card.addEventListener("click", () => navigate(item.route));
    list.appendChild(card);
  }

  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = `
    <div class="continue-card" id="btn-continue">
      <div class="continue-icon">▶</div>
      <div>
        <div class="continue-title">${t("continue")}</div>
        <div class="continue-sub">Урок 1.1</div>
      </div>
    </div>
    <button class="side-btn" id="btn-lang">
      <span style="font-size:18px">🌐</span>
      <span>${langName()}</span>
    </button>
    <button class="side-btn" id="btn-about">
      <span style="font-size:18px">ℹ</span>
      <span>О программе</span>
    </button>
    <div class="streak-card">
      <div style="font-size:28px">🔥</div>
      <div>
        <div class="streak-num">0</div>
        <div class="streak-label">${t("streak")}</div>
      </div>
    </div>
    <div class="progress-bar-container">
      <div class="progress-header">
        <span>${t("course_progress")}</span>
        <span>0/18</span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill" style="width: 0%"></div>
      </div>
    </div>
  `;

  document.getElementById("btn-continue").addEventListener("click",
    () => navigate("lessons"));
  document.getElementById("btn-lang").addEventListener("click",
    () => cycleLang());
  document.getElementById("btn-about").addEventListener("click",
    () => alert("HSK 5 Learner · web\nHSK 5 上 · тренажёр"));
}

function langName() {
  return { ru: "Сменить язык", tk: "Dili çalyş", en: "Change language" }[getLang()];
}

function cycleLang() {
  const order = ["ru", "tk", "en"];
  const cur = getLang();
  const nxt = order[(order.indexOf(cur) + 1) % order.length];
  setLang(nxt);
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

const UNIT_COLORS = {
  1: "#3A6088", 2: "#3A7060", 3: "#7A6030",
  4: "#5A4A88", 5: "#3A7080", 6: "#7A3A60",
};

async function renderLessons() {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header">
      <span class="app-name">📚 ${t("menu_lessons").replace(/^[^\s]+\s*/, "")}</span>
    </div>
    <div class="version">${t("lessons_sub")}</div>
    <div id="lessons-content" class="loading">${t("loading")}</div>
  `;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));

  try {
    const r = await fetch("/api/lessons");
    const lessons = await r.json();

    const byUnit = {};
    for (const l of lessons) {
      const u = l.unit;
      if (!byUnit[u]) byUnit[u] = [];
      byUnit[u].push(l);
    }

    const cont = document.getElementById("lessons-content");
    cont.classList.remove("loading");
    cont.innerHTML = "";

    for (const unit of Object.keys(byUnit).sort()) {
      const unitBlock = document.createElement("div");
      unitBlock.className = "unit-block";

      const title = UNIT_TITLES[unit] || {};
      const tr = title[getLang()] || title.en || "";

      unitBlock.innerHTML = `
        <div class="unit-header">
          <span class="unit-label">UNIT ${unit}</span>
          <span class="unit-name">${title.zh || ""} · ${tr}</span>
        </div>
      `;

      for (const l of byUnit[unit]) {
        const row = document.createElement("div");
        row.className = "lesson-row";
        const color = UNIT_COLORS[l.unit] || "#3A6088";
        // FIX: сервер отдаёт "lesson", а не "index"
        const lessonNum = l.lesson;
        const zh = (l.title && l.title.zh) || `Урок ${l.unit}.${lessonNum}`;
        const trTitle = (l.title && (l.title[getLang()] || l.title.en)) || "";

        row.innerHTML = `
          <div class="lesson-num" style="background:${color}">${l.unit}.${lessonNum}</div>
          <div class="lesson-titles">
            <div class="lesson-zh">${zh}</div>
            <div class="lesson-tr">${trTitle}</div>
          </div>
          <div class="card-chevron">›</div>
        `;
        // FIX: используем l.lesson
        row.addEventListener("click", () => navigate(`lesson/${l.unit}/${lessonNum}`));
        unitBlock.appendChild(row);
      }

      cont.appendChild(unitBlock);
    }
  } catch (e) {
    document.getElementById("lessons-content").innerHTML =
      `<div style="color:#FF6B6B">Ошибка загрузки: ${e.message}</div>`;
  }
}

// ============================================================
// ЭКРАН УРОКА
// ============================================================
const TABS = [
  { key: "tab_text",     id: "text" },
  { key: "tab_vocab",    id: "vocab" },
  { key: "tab_grammar",  id: "grammar" },
  { key: "tab_phrases",  id: "phrases" },
  { key: "tab_compare",  id: "compare" },
  { key: "tab_exercise", id: "exercise" },
  { key: "tab_extend",   id: "extend" },
  { key: "tab_apply",    id: "apply" },
];

let currentLesson = null;
let currentTab = "text";

async function renderLesson(unit, index) {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div id="lesson-content" class="loading">${t("loading")}</div>
  `;
  document.getElementById("back").addEventListener("click", () => navigate("lessons"));

  try {
    const r = await fetch(`/api/lessons/${unit}/${index}`);
    if (!r.ok) throw new Error("Урок не найден");
    currentLesson = await r.json();
    currentTab = "text";
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
      <div class="lesson-badge" style="background:${color}">${L.unit}.${L.index || L.lesson || ""}</div>
      <div class="lesson-titles-block">
        <div class="lesson-zh-big">${zh}</div>
        <div class="lesson-tr-big">${tr}</div>
      </div>
    </div>

    <div class="tabs-bar" id="tabs-bar"></div>
    <div class="tab-content" id="tab-content"></div>
  `;

  const tabsBar = document.getElementById("tabs-bar");
  for (const tab of TABS) {
    const btn = document.createElement("button");
    btn.className = "tab-btn" + (tab.id === currentTab ? " active" : "");
    btn.textContent = t(tab.key);
    btn.addEventListener("click", () => {
      currentTab = tab.id;
      drawLesson();
    });
    tabsBar.appendChild(btn);
  }

  const content = document.getElementById("tab-content");
  content.innerHTML = "";

  const renderer = {
    text: renderTabText,
    vocab: renderTabVocab,
    grammar: renderTabGrammar,
    phrases: renderTabPhrases,
    compare: renderTabCompare,
    exercise: renderTabExercise,
    extend: renderTabExtend,
    apply: renderTabApply,
  }[currentTab];

  if (renderer) renderer(content);
}

function renderTabText(cont) {
  const L = currentLesson;
  const lang = getLang();
  const tr = (L.text_translation && L.text_translation[lang]) || "";

  const wrapper = document.createElement("div");
  wrapper.className = "content-card";
  wrapper.innerHTML = `
    <button class="audio-btn" disabled>${t("translate_audio")}</button>
    <div class="text-zh">${escapeHtml(L.text_zh || "")}</div>
    <div class="text-tr">${escapeHtml(tr)}</div>
  `;
  cont.appendChild(wrapper);
}

function renderTabVocab(cont) {
  const L = currentLesson;
  const lang = getLang();
  const words = L.vocabulary || [];

  const card = document.createElement("div");
  card.className = "content-card";
  card.innerHTML = `
    <div class="content-card-title">生词 · ${words.length} ${t("vocab_words")}</div>
    <table class="vocab-table">
      <thead>
        <tr>
          <th style="width:90px">${t("vocab_col_hanzi")}</th>
          <th style="width:130px">${t("vocab_col_pinyin")}</th>
          <th style="width:70px">${t("vocab_col_pos")}</th>
          <th>${t("vocab_col_trans")}</th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
  `;
  const tbody = card.querySelector("tbody");

  for (const w of words) {
    const tr = (w.meaning && (w.meaning[lang] || w.meaning.en)) || "";
    const row = document.createElement("tr");
    row.innerHTML = `
      <td class="cell-hanzi">${escapeHtml(w.hanzi || "")}</td>
      <td class="cell-pinyin">${escapeHtml(w.pinyin || "")}</td>
      <td class="cell-pos">${escapeHtml(w.pos || "")}</td>
      <td>${escapeHtml(tr)}</td>
    `;
    tbody.appendChild(row);
  }
  cont.appendChild(card);
}

function renderTabGrammar(cont) {
  const L = currentLesson;
  const lang = getLang();
  const grammars = L.grammar || [];

  for (const g of grammars) {
    const card = document.createElement("div");
    card.className = "grammar-card";
    const expl = (g.explanation && (g.explanation[lang] || g.explanation.en)) || "";

    let examplesHtml = "";
    for (let i = 0; i < (g.examples || []).length; i++) {
      const ex = g.examples[i];
      const exTr = ex[lang] || ex.en || "";
      examplesHtml += `
        <div class="grammar-example">
          <div class="ex-zh">${i + 1}. ${escapeHtml(ex.zh || "")}</div>
          <div class="ex-tr">${escapeHtml(exTr)}</div>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="grammar-head">
        <span class="grammar-word">${escapeHtml(g.word || "")}</span>
        <span class="grammar-pos">${escapeHtml(g.pos || "")}</span>
      </div>
      <div class="grammar-expl">${escapeHtml(expl)}</div>
      ${examplesHtml}
    `;
    cont.appendChild(card);
  }
}

function renderTabPhrases(cont) {
  const L = currentLesson;
  for (const col of (L.collocations || [])) {
    const card = document.createElement("div");
    card.className = "phrases-card";
    let itemsHtml = "";
    for (const item of (col.items || [])) {
      itemsHtml += `<div class="phrase-item">${escapeHtml(item)}</div>`;
    }
    card.innerHTML = `
      <div class="phrases-pattern">${escapeHtml(col.pattern || "")}</div>
      ${itemsHtml}
    `;
    cont.appendChild(card);
  }
}

function renderTabCompare(cont) {
  const L = currentLesson;
  const lang = getLang();
  for (const cp of (L.comparisons || [])) {
    const card = document.createElement("div");
    card.className = "compare-card";
    const common = (cp.common && (cp.common[lang] || cp.common.en)) || "";

    let diffsHtml = "";
    for (const d of (cp.differences || [])) {
      const dText = d[lang] || d.en || "";
      diffsHtml += `<div class="compare-diff-item">${escapeHtml(dText)}</div>`;
    }

    card.innerHTML = `
      <div class="compare-head">${escapeHtml(cp.word_a || "")} vs ${escapeHtml(cp.word_b || "")}</div>
      <div class="compare-common">≈ ${t("common")}</div>
      <div class="compare-common-text">${escapeHtml(common)}</div>
      <div class="compare-diff-title">≠ ${t("differences")}</div>
      ${diffsHtml}
    `;
    cont.appendChild(card);
  }
}

function renderTabExercise(cont) {
  const L = currentLesson;
  const items = [
    { icon: "🎧", title: t("listen"),
      sub: `${(L.workbook && L.workbook.listening || []).length} ${t("questions")}` },
    { icon: "📖", title: t("reading"),
      sub: `${(L.workbook && L.workbook.reading || []).length} ${t("questions")}` },
    { icon: "✍", title: t("writing"),
      sub: `${(L.workbook && L.workbook.writing || []).length} ${t("tasks")}` },
  ];

  for (const item of items) {
    const el = document.createElement("div");
    el.className = "exercise-item";
    el.innerHTML = `
      <div class="exercise-icon">${item.icon}</div>
      <div>
        <div class="exercise-title">${item.title}</div>
        <div class="exercise-sub">${item.sub}</div>
      </div>
      <div class="card-chevron" style="margin-left:auto">›</div>
    `;
    el.addEventListener("click", () => alert("Появится в Итерации 3"));
    cont.appendChild(el);
  }
}

function renderTabExtend(cont) {
  const L = currentLesson;
  const lang = getLang();
  const exp = L.expansion || {};
  if (!exp.words || !exp.words.length) {
    cont.innerHTML = `<div class="loading">—</div>`;
    return;
  }

  const card = document.createElement("div");
  card.className = "content-card";
  const topic = (exp.topic && (exp.topic[lang] || exp.topic.en)) || "";
  let html = topic ? `<div class="extend-topic">${escapeHtml(topic)}</div>` : "";

  for (const w of exp.words) {
    const m = (w.meaning && (w.meaning[lang] || w.meaning.en)) || "";
    html += `
      <div class="extend-word">
        <div class="extend-hanzi">${escapeHtml(w.hanzi || "")}</div>
        <div class="extend-pinyin">${escapeHtml(w.pinyin || "")}</div>
        <div class="extend-meaning">${escapeHtml(m)}</div>
      </div>
    `;
  }
  card.innerHTML = html;
  cont.appendChild(card);
}

function renderTabApply(cont) {
  const L = currentLesson;
  const lang = getLang();
  const app_ = L.application || {};
  const disc = (app_.discussion && (app_.discussion[lang] || app_.discussion.en)) || "";

  const card = document.createElement("div");
  card.className = "content-card";
  card.innerHTML = `
    <div class="content-card-title">🎓 ${t("tab_apply").replace(/^[^\s]+\s*/, "")}</div>
    <div class="apply-question">${escapeHtml(disc)}</div>
  `;
  cont.appendChild(card);
}

// ============================================================
// Заглушка
// ============================================================
function renderPlaceholder(title) {
  app.innerHTML = `
    <button class="back-btn" id="back">‹ ${t("back")}</button>
    <div class="header">
      <span class="app-name">${title}</span>
    </div>
    <div class="loading" style="font-size:18px; padding-top:80px;">
      🚧 Этот раздел появится в следующих итерациях
    </div>
  `;
  document.getElementById("back").addEventListener("click", () => navigate("menu"));
}

// ============================================================
// Роутер
// ============================================================
function navigate(path) {
  const parts = path.split("/");
  if (path === "menu" || path === "") {
    renderMainMenu();
  } else if (parts[0] === "lessons") {
    renderLessons();
  } else if (parts[0] === "lesson" && parts.length === 3) {
    // FIX: защита от NaN / undefined
    const u = parseInt(parts[1], 10);
    const i = parseInt(parts[2], 10);
    if (Number.isFinite(u) && Number.isFinite(i)) {
      renderLesson(u, i);
    } else {
      // если пришли по битой ссылке #lesson/1/undefined — уводим к списку
      renderLessons();
      window.location.hash = "lessons";
      return;
    }
  } else if (parts[0] === "vocab") {
    renderPlaceholder("📓 " + t("menu_vocab").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "srs") {
    renderPlaceholder("🔁 " + t("menu_srs").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "activity") {
    renderPlaceholder("📊 " + t("menu_activity").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "progress") {
    renderPlaceholder("📈 " + t("menu_progress").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "analyzer") {
    renderPlaceholder("🔍 " + t("menu_analyzer").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "grammar") {
    renderPlaceholder("📚 " + t("menu_grammar").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "compare") {
    renderPlaceholder("⚖ " + t("menu_compare").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "achievements") {
    renderPlaceholder("🏆 " + t("menu_achievements").replace(/^[^\s]+\s*/, ""));
  } else if (parts[0] === "settings") {
    renderPlaceholder("⚙ " + t("menu_settings").replace(/^[^\s]+\s*/, ""));
  } else {
    renderPlaceholder("? " + path);
  }
  window.location.hash = path;
}

// ============================================================
// Хелперы
// ============================================================
function escapeHtml(s) {
  if (!s) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ============================================================
// Старт
// ============================================================
drawBackgroundPattern();

const initial = window.location.hash.slice(1) || "menu";
navigate(initial);

window.addEventListener("lang_changed", () => {
  const route = window.location.hash.slice(1) || "menu";
  navigate(route);
});

window.addEventListener("resize", () => {
  const c = document.getElementById("bg-pattern");
  if (c) { c.innerHTML = ""; c.dataset.drawn = "0"; }
  drawBackgroundPattern();
});

window.addEventListener("hashchange", () => {
  const route = window.location.hash.slice(1) || "menu";
  navigate(route);
});