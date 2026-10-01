// HSK6 · SRS + генерация через DeepSeek
(function(){
"use strict";

const LS = {
  srs:      "hsk6_srs",
  settings: "hsk6_srs_settings",
  lang:     "hsk6_lang",
  pos:      "hsk6_last_index",
  viewed:   "hsk6_viewed",
};

const SRS_SETTINGS_DEFAULT = {
  learnSteps: [1, 10], relearnSteps: [10],
  graduatingInterval: 1, easyInterval: 4,
  startingEase: 2.5, minEase: 1.3, easyBonus: 1.3,
  hardMultiplier: 1.2, maxInterval: 365 * 5,
  newIntervalAfterLapse: 0, delayBonus: true,
};
const SRS_MIN = 60 * 1000;
const SRS_DAY = 24 * 60 * SRS_MIN;
const AUTO_ADD_AFTER_MS = 60 * 1000;

let state = {
  words: [],
  index: 0,
  lang: "ru",
  contentCache: new Map(),
  prefetchQueue: new Set(),
  viewStartAt: 0,
  viewHanzi: null,
  isReview: false,
  reviewQueue: [],
  reviewPos: 0,
};

// ---------- localStorage ----------
function lsGet(k, def) {
  try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : def; }
  catch(e){ return def; }
}
function lsSet(k, v) {
  try { localStorage.setItem(k, JSON.stringify(v)); } catch(e){}
  if (typeof HSKAuth !== "undefined" && HSKAuth.syncKey) HSKAuth.syncKey(k, v);
}

// ---------- SRS ----------
function srsLoad() { return lsGet(LS.srs, {}); }
function srsSave(d) { lsSet(LS.srs, d); }
function srsGetSettings() {
  return Object.assign({}, SRS_SETTINGS_DEFAULT, lsGet(LS.settings, {}) || {});
}
function srsCardDefaults(now) {
  const cfg = srsGetSettings();
  return { state:"new", stepIndex:0, due:now, interval:0,
           ease:cfg.startingEase, reps:0, lapses:0 };
}
function srsMigrate(c, now) {
  if (!c || typeof c !== "object") return srsCardDefaults(now);
  if (c.state) return c;
  const cfg = srsGetSettings();
  c.state = (c.reps || 0) >= 1 ? "review" : "new";
  c.stepIndex = c.stepIndex || 0;
  if (!c.ease) c.ease = cfg.startingEase;
  return c;
}
function srsFmtMs(ms) {
  if (ms < 60000) return Math.round(ms/1000) + "s";
  if (ms < 3600000) return Math.round(ms/60000) + "m";
  if (ms < 86400000) return (ms/3600000).toFixed(1) + "h";
  const d = ms / 86400000;
  if (d < 30) return Math.round(d) + "d";
  if (d < 365) return (d/30).toFixed(1) + "mo";
  return (d/365).toFixed(1) + "y";
}
function srsPreview(card) {
  const cfg = srsGetSettings();
  const now = Date.now();
  const c = card || srsCardDefaults(now);
  const st = c.state || "new";
  const out = { again:"", hard:"", good:"", easy:"" };
  if (st === "new") {
    const s0 = cfg.learnSteps[0] || 1;
    const s1 = cfg.learnSteps[1] || s0 * 10;
    out.again = srsFmtMs(s0 * SRS_MIN);
    out.hard  = srsFmtMs(((s0 + s1) / 2) * SRS_MIN);
    out.good  = srsFmtMs(s1 * SRS_MIN);
    out.easy  = srsFmtMs(cfg.easyInterval * SRS_DAY);
    return out;
  }
  if (st === "learning" || st === "relearning") {
    const steps = st === "relearning" ? cfg.relearnSteps : cfg.learnSteps;
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
function srsApplyRating(key, rating) {
  const db = srsLoad();
  const now = Date.now();
  const cfg = srsGetSettings();
  let c = db[key] ? srsMigrate(db[key], now) : srsCardDefaults(now);
  if (c.state === "new") { c.state = "learning"; c.stepIndex = 0; }
  if (c.state === "learning" || c.state === "relearning") {
    const steps = c.state === "relearning" ? cfg.relearnSteps : cfg.learnSteps;
    if (rating === 1) { c.stepIndex = 0; c.due = now + steps[0] * SRS_MIN; }
    else if (rating === 2) {
      const cur = steps[c.stepIndex] || steps[steps.length - 1];
      const nxt = steps[c.stepIndex + 1];
      c.due = now + (nxt ? (cur + nxt) / 2 : cur * 1.5) * SRS_MIN;
    } else if (rating === 3) {
      const ni = c.stepIndex + 1;
      if (ni < steps.length) { c.stepIndex = ni; c.due = now + steps[ni] * SRS_MIN; }
      else {
        c.state = "review"; c.interval = cfg.graduatingInterval;
        c.reps = (c.reps || 0) + 1;
        c.due = now + cfg.graduatingInterval * SRS_DAY;
      }
    } else {
      c.state = "review"; c.interval = cfg.easyInterval;
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
      c.state = "relearning"; c.stepIndex = 0;
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
  db[key] = c;
  srsSave(db);
  return c;
}

// ---------- Tracking просмотров ----------
function loadViewed() { return lsGet(LS.viewed, {}); }
function saveViewed(v) { lsSet(LS.viewed, v); }
function markViewed(hanzi) {
  if (!hanzi) return;
  const v = loadViewed();
  v[hanzi] = Date.now();
  saveViewed(v);
}
function autoAddIfLong(hanzi, viewStartAt) {
  if (!hanzi || !viewStartAt) return false;
  const elapsed = Date.now() - viewStartAt;
  if (elapsed < AUTO_ADD_AFTER_MS) return false;
  const db = srsLoad();
  if (db[hanzi]) return false;
  db[hanzi] = srsCardDefaults(Date.now());
  srsSave(db);
  return true;
}
function countSrsCards() { return Object.keys(srsLoad()).length; }
function countDueCards() {
  const db = srsLoad();
  const now = Date.now();
  return Object.values(db).filter(c => (c.due || 0) <= now).length;
}

// ---------- Highlighter ----------
let _sortedWords = null;
function buildMatcher() {
  if (_sortedWords) return _sortedWords;
  _sortedWords = state.words.map(w => w.hanzi).sort((a,b) => b.length - a.length);
  return _sortedWords;
}
function highlight(text) {
  const words = buildMatcher();
  const out = [];
  let i = 0;
  while (i < text.length) {
    let matched = null;
    for (const w of words) if (text.startsWith(w, i)) { matched = w; break; }
    if (matched) { out.push(["m", matched]); i += matched.length; }
    else { out.push(["t", text[i]]); i += 1; }
  }
  const merged = [];
  for (const [k, chunk] of out) {
    if (merged.length && merged[merged.length-1][0] === "t" && k === "t")
      merged[merged.length-1][1] += chunk;
    else merged.push([k, chunk]);
  }
  return merged.map(([k, c]) => {
    const esc = c.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
    return k === "m" ? `<mark>${esc}</mark>` : esc;
  }).join("");
}

// ---------- API ----------
async function loadWords() {
  const r = await fetch("/api/hsk6/words");
  state.words = await r.json();
}
async function fetchWord(id) {
  const r = await fetch(`/api/hsk6/word/${id}?lang=${state.lang}`);
  return r.json();
}
async function generateContent(id) {
  const r = await fetch(`/api/hsk6/generate/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ lang: state.lang }),
  });
  if (!r.ok) throw new Error("generate failed");
  return r.json();
}
async function prefetchNext(n = 1) {
  for (let i = 1; i <= n; i++) {
    const idx = state.index + i;
    if (idx >= state.words.length) break;
    const w = state.words[idx];
    if (state.contentCache.has(w.id) || state.prefetchQueue.has(w.id)) continue;
    state.prefetchQueue.add(w.id);
    try {
      const data = await fetchWord(w.id);
      if (data.content) state.contentCache.set(w.id, data.content);
      else {
        const gen = await generateContent(w.id);
        state.contentCache.set(w.id, gen);
      }
    } catch (e) {}
    finally { state.prefetchQueue.delete(w.id); }
  }
}

// ---------- UI ----------
const $ = id => document.getElementById(id);
function toast(msg) {
  const t = $("toast");
  t.textContent = msg; t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 1800);
}
function escapeHtml(s) {
  return String(s || "").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

function currentWord() {
  if (state.isReview) {
    const hanzi = state.reviewQueue[state.reviewPos];
    if (!hanzi) return null;
    return state.words.find(w => w.hanzi === hanzi) || null;
  }
  return state.words[state.index];
}
function currentPosition() {
  return state.isReview ? state.reviewPos : state.index;
}
function currentTotal() {
  return state.isReview ? state.reviewQueue.length : state.words.length;
}

function injectReviewButton() {
  if ($("review-btn")) return;
  const start = $("start-btn");
  if (!start) return;
  const btn = document.createElement("button");
  btn.id = "review-btn";
  btn.textContent = "REVIEW";
  btn.style.cssText = `
    margin-top: 12px; padding: 14px 42px;
    background: transparent; color: var(--cinnabar);
    border: 1px solid var(--cinnabar); border-radius: 4px;
    font-family: var(--font-body); font-size: 15px; font-weight: 600;
    letter-spacing: 0.12em; cursor: pointer;
    transition: background .15s, color .15s;
  `;
  btn.onmouseenter = () => { btn.style.background = "var(--cinnabar)"; btn.style.color = "var(--paper)"; };
  btn.onmouseleave = () => { btn.style.background = "transparent"; btn.style.color = "var(--cinnabar)"; };
  btn.onclick = startReview;
  start.parentNode.insertBefore(btn, start.nextSibling);
}

function updateReviewBadge() {
  const btn = $("review-btn");
  if (!btn) return;
  const due = countDueCards();
  const total = countSrsCards();
  if (due > 0) {
    btn.textContent = `REVIEW (${due})`;
    btn.style.fontWeight = "700";
  } else {
    btn.textContent = total > 0 ? "REVIEW (0)" : "REVIEW";
    btn.style.fontWeight = "600";
  }
}

function renderIntro() {
  $("intro").style.display = "flex";
  $("card").style.display = "none";
  $("srs-bar").style.display = "none";
  $("progress-fill").style.width = "0%";
  const srsTotal = countSrsCards();
  const due = countDueCards();
  $("deck-info").innerHTML = `Загружено: ${state.words.length} слов<br>
    <span style="font-size:12px">В SRS: <b>${srsTotal}</b> · К повторению: <b>${due}</b></span>`;
  renderLangPicker();
  injectReviewButton();
  updateReviewBadge();
}

function renderLangPicker() {
  const host = $("lang-picker");
  host.innerHTML = "";
  const langs = [["ru","Рус"],["en","En"],["tk","Tk"],["uz","Uz"],["tg","Tg"],["id","Id"]];
  for (const [code, label] of langs) {
    const b = document.createElement("span");
    b.className = "lang-chip" + (code === state.lang ? " active" : "");
    b.textContent = label;
    b.onclick = () => {
      state.lang = code;
      lsSet(LS.lang, code);
      state.contentCache.clear();
      _sortedWords = null;
      renderLangPicker();
      if ($("card").style.display !== "none") renderCurrent();
    };
    host.appendChild(b);
  }
}

function renderCard() {
  $("intro").style.display = "none";
  $("card").style.display = "block";
  $("srs-bar").style.display = "flex";
  renderCurrent();
}

async function renderCurrent() {
  // авто-добавить предыдущее слово, если долго смотрел
  if (state.viewHanzi && state.viewStartAt) {
    const added = autoAddIfLong(state.viewHanzi, state.viewStartAt);
    if (added) toast("Слово добавлено в SRS");
  }

  const w = currentWord();
  if (!w) return;

  state.viewHanzi = w.hanzi;
  state.viewStartAt = Date.now();
  markViewed(w.hanzi);

  $("hanzi").textContent = w.hanzi;
  $("pinyin").textContent = w.pinyin || "";
  $("translation").textContent = (w.translations && w.translations[state.lang]) || (w.translations && w.translations.en) || "";
  $("counter").textContent = `${currentPosition() + 1} / ${currentTotal()}${state.isReview ? " · REVIEW" : ""}`;
  $("progress-fill").style.width = `${((currentPosition() + 1) / currentTotal()) * 100}%`;

  $("explain-body").innerHTML = `<span class="explain-loading">Генерация…</span>`;
  $("examples-body").innerHTML = `<span class="explain-loading">Генерация…</span>`;

  if (state.contentCache.has(w.id)) {
    renderContent(state.contentCache.get(w.id));
    updateSrsPreviews();
    return;
  }
  try {
    const data = await fetchWord(w.id);
    if (data.content) {
      state.contentCache.set(w.id, data.content);
      renderContent(data.content);
    } else {
      const gen = await generateContent(w.id);
      state.contentCache.set(w.id, gen);
      renderContent(gen);
    }
  } catch (e) {
    $("explain-body").innerHTML = `<span style="color:var(--cinnabar)">Ошибка: ${e.message}</span>`;
  }
  prefetchNext(1);
  updateSrsPreviews();
}

function renderContent(data) {
  const exp = data.explanation || {};
  const sections = [];
  if (exp.meaning)       sections.push(["Что значит", exp.meaning]);
  if (exp.when_used)     sections.push(["Где используется", exp.when_used]);
  if (exp.when_not_used) sections.push(["Где НЕ используется", exp.when_not_used]);
  if (exp.nuance)        sections.push(["Нюанс vs синонимы", exp.nuance]);
  if (exp.register)      sections.push(["Регистр", exp.register]);

  let html = "";
  for (const [label, text] of sections) {
    html += `<div class="explain-section">
      <div class="explain-label">${label}</div>
      <div class="explain-text">${escapeHtml(text)}</div>
    </div>`;
  }
  if (exp.collocations && exp.collocations.length) {
    html += `<div class="explain-section">
      <div class="explain-label">Типичные сочетания</div>
      <div class="collocations">${exp.collocations.map(c =>
        `<span class="colloc">${escapeHtml(c.zh)}</span>`).join("")}</div>
    </div>`;
  }
  $("explain-body").innerHTML = html || `<span class="explain-loading">—</span>`;

  const sents = data.sentences || [];
  $("examples-body").innerHTML = sents.map((s, i) => `
    <div class="example">
      <div class="example-num">${i+1} / ${sents.length}</div>
      <div class="example-zh">${highlight(s.zh)}</div>
      <div class="example-py">${escapeHtml(s.pinyin || "")}</div>
      <div class="example-ru">${escapeHtml(s.translation || "")}</div>
    </div>
  `).join("");
}

function updateSrsPreviews() {
  const w = currentWord();
  if (!w) return;
  const card = srsLoad()[w.hanzi] || srsCardDefaults(Date.now());
  const p = srsPreview(srsMigrate(card, Date.now()));
  $("p1").textContent = p.again;
  $("p2").textContent = p.hard;
  $("p3").textContent = p.good;
  $("p4").textContent = p.easy;
}

async function rateAndNext(rating) {
  const w = currentWord();
  if (!w) return;

  autoAddIfLong(w.hanzi, state.viewStartAt);
  srsApplyRating(w.hanzi, rating);

  if (state.isReview) {
    state.reviewPos += 1;
    if (state.reviewPos >= state.reviewQueue.length) {
      toast("Review завершён");
      state.isReview = false;
      renderIntro();
      return;
    }
  } else {
    state.index = Math.min(state.index + 1, state.words.length - 1);
    lsSet(LS.pos, state.index);
    if (state.index >= state.words.length - 1 && w === state.words[state.words.length - 1]) {
      toast("Колода завершена");
      renderIntro();
      return;
    }
  }
  await renderCurrent();
}

async function startReview() {
  const db = srsLoad();
  const now = Date.now();
  let due = Object.entries(db)
    .filter(([h, c]) => (c.due || 0) <= now)
    .map(([h]) => h);
  if (!due.length) { toast("Нет карточек к повторению"); return; }
  for (let i = due.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [due[i], due[j]] = [due[j], due[i]];
  }
  if (!state.words.length) await loadWords();
  state.isReview = true;
  state.reviewQueue = due;
  state.reviewPos = 0;
  renderCard();
}

async function init() {
  state.lang = lsGet(LS.lang, "ru");
  state.index = lsGet(LS.pos, 0);

  $("start-btn").onclick = async () => {
    try {
      if (!state.words.length) {
        $("deck-info").textContent = "Загрузка списка…";
        await loadWords();
      }
      state.isReview = false;
      renderCard();
    } catch (e) { toast("Ошибка загрузки: " + e.message); }
  };

  $("back-btn").onclick = () => {
    if (state.viewHanzi && state.viewStartAt) autoAddIfLong(state.viewHanzi, state.viewStartAt);
    state.isReview = false;
    renderIntro();
  };

  document.querySelectorAll("#rate-wrap .srs-btn").forEach(b => {
    b.onclick = () => rateAndNext(parseInt(b.dataset.rate, 10));
  });

  try { await loadWords(); renderIntro(); }
  catch (e) { $("deck-info").textContent = "Ошибка: " + e.message; }

  window.addEventListener("beforeunload", () => {
    if (state.viewHanzi && state.viewStartAt) autoAddIfLong(state.viewHanzi, state.viewStartAt);
  });

  document.addEventListener("keydown", e => {
    if ($("card").style.display === "none") return;
    if (e.code === "Space") {
      e.preventDefault();
      rateAndNext(3);
    }
    if (e.key >= "1" && e.key <= "4") {
      rateAndNext(parseInt(e.key, 10));
    }
  });
}

document.addEventListener("DOMContentLoaded", init);
})();