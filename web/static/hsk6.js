// HSK6 · SRS + генерация через DeepSeek + авточитатель (одна кнопка)
(function(){
"use strict";

const LS = {
  srs:      "hsk6_srs",
  settings: "hsk6_srs_settings",
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

// ---------- i18n ----------
const T6 = {
  tr: {
    subtitle: "2460 kelime · C1 Seviyesi",
    meta: "DeepSeek · 3 örnek · derin açıklama",
    loaded: "Yüklendi",
    words: "kelime",
    in_srs: "SRS'de",
    due: "Vadesi gelen",
    explain_title: "Derin açıklama",
    examples_title: "Örnekler",
    meaning: "Anlam",
    when_used: "Nerede kullanılır",
    when_not_used: "Nerede kullanılmaz",
    collocations: "Tipik eşdizimler",
    nuance: "Eş anlamlılarla nüans farkı",
    register: "Dil düzeyi",
    generating: "Oluşturuluyor…",
    loading: "Yükleniyor…",
    loading_list: "Liste yükleniyor…",
    error: "Hata",
    error_loading: "Yükleme hatası",
    added_to_srs: "Kelime SRS'ye eklendi",
    review_done: "Tekrar tamamlandı",
    deck_done: "Deste tamamlandı",
    no_due: "Vadesi gelen kart yok",
    srs_again: "Tekrar",
    srs_hard: "Zor",
    srs_good: "İyi",
    srs_easy: "Kolay",
    tts_no_voice: "Bu dil için yüklü ses yok",
    tts_not_supported: "Tarayıcı konuşmayı desteklemiyor",
    tts_nothing: "Henüz okunacak bir şey yok — oluşturmayı bekleyin",
  },

  ru: {
    subtitle: "2460 слов · Уровень C1",
    meta: "DeepSeek · 3 примера · глубокое объяснение",
    loaded: "Загружено", words: "слов",
    in_srs: "В SRS", due: "К повторению",
    explain_title: "Глубокое объяснение",
    examples_title: "Примеры",
    meaning: "Что значит",
    when_used: "Где используется",
    when_not_used: "Где НЕ используется",
    collocations: "Типичные сочетания",
    nuance: "Нюанс vs синонимы",
    register: "Регистр",
    generating: "Генерация…",
    loading: "Загрузка…",
    loading_list: "Загрузка списка…",
    error: "Ошибка",
    error_loading: "Ошибка загрузки",
    added_to_srs: "Слово добавлено в SRS",
    review_done: "Review завершён",
    deck_done: "Колода завершена",
    no_due: "Нет карточек к повторению",
    srs_again: "Забыл",
    srs_hard: "Трудно",
    srs_good: "Хорошо",
    srs_easy: "Легко",
    tts_no_voice: "Голос для этого языка не установлен",
    tts_not_supported: "Браузер не поддерживает озвучку",
    tts_nothing: "Нечего читать — дождитесь генерации",
  },
  en: {
    subtitle: "2460 words · Level C1",
    meta: "DeepSeek · 3 examples · deep explanation",
    loaded: "Loaded", words: "words",
    in_srs: "In SRS", due: "Due",
    explain_title: "Deep explanation",
    examples_title: "Examples",
    meaning: "Meaning",
    when_used: "Where it's used",
    when_not_used: "Where NOT to use",
    collocations: "Typical collocations",
    nuance: "Nuance vs synonyms",
    register: "Register",
    generating: "Generating…",
    loading: "Loading…",
    loading_list: "Loading list…",
    error: "Error",
    error_loading: "Loading error",
    added_to_srs: "Word added to SRS",
    review_done: "Review finished",
    deck_done: "Deck finished",
    no_due: "No cards due",
    srs_again: "Again",
    srs_hard: "Hard",
    srs_good: "Good",
    srs_easy: "Easy",
    tts_no_voice: "No voice for this language installed",
    tts_not_supported: "Browser doesn't support speech",
    tts_nothing: "Nothing to read yet — wait for generation",
  },
  tk: {
    subtitle: "2460 söz · Dereje C1",
    meta: "DeepSeek · 3 mysal · çuň düşündiriş",
    loaded: "Ýüklenen", words: "söz",
    in_srs: "SRS-de", due: "Gaýtalamaga",
    explain_title: "Çuň düşündiriş",
    examples_title: "Mysallar",
    meaning: "Manysy",
    when_used: "Nirede ulanylýar",
    when_not_used: "Nirede ULANYLMAÝAR",
    collocations: "Adaty söz düzümleri",
    nuance: "Sinonimlerden tapawudy",
    register: "Stil",
    generating: "Döredilýär…",
    loading: "Ýüklenýär…",
    loading_list: "Sanaw ýüklenýär…",
    error: "Ýalňyşlyk",
    error_loading: "Ýüklemek säwligi",
    added_to_srs: "Söz SRS-e goşuldy",
    review_done: "Gaýtalama gutardy",
    deck_done: "Kartlar gutardy",
    no_due: "Gaýtalamaga karta ýok",
    srs_again: "Ýatdan çykardym",
    srs_hard: "Kyn",
    srs_good: "Gowy",
    srs_easy: "Aňsat",
    tts_no_voice: "Bu dil üçin ses ýok",
    tts_not_supported: "Brauzer sesini goldamaýar",
    tts_nothing: "Okajak zat ýok — garaşyň",
  },
  uz: {
    subtitle: "2460 so'z · C1 daraja",
    meta: "DeepSeek · 3 misol · chuqur tushuntirish",
    loaded: "Yuklandi", words: "so'z",
    in_srs: "SRS'da", due: "Takrorlashga",
    explain_title: "Chuqur tushuntirish",
    examples_title: "Misollar",
    meaning: "Ma'nosi",
    when_used: "Qayerda ishlatiladi",
    when_not_used: "Qayerda ISHLATILMAYDI",
    collocations: "Odatiy birikmalar",
    nuance: "Sinonimlardan farqi",
    register: "Uslub",
    generating: "Yaratilmoqda…",
    loading: "Yuklanmoqda…",
    loading_list: "Ro'yxat yuklanmoqda…",
    error: "Xatolik",
    error_loading: "Yuklashda xatolik",
    added_to_srs: "So'z SRS'ga qo'shildi",
    review_done: "Takrorlash tugadi",
    deck_done: "Kartalar tugadi",
    no_due: "Takrorlash uchun karta yo'q",
    srs_again: "Yana",
    srs_hard: "Qiyin",
    srs_good: "Yaxshi",
    srs_easy: "Oson",
    tts_no_voice: "Bu til uchun ovoz yo'q",
    tts_not_supported: "Brauzer ovozni qo'llamaydi",
    tts_nothing: "O'qish uchun hech narsa yo'q",
  },
  tg: {
    subtitle: "2460 калима · Сатҳи C1",
    meta: "DeepSeek · 3 мисол · шарҳи амиқ",
    loaded: "Бор карда шуд", words: "калима",
    in_srs: "Дар SRS", due: "Барои такрор",
    explain_title: "Шарҳи амиқ",
    examples_title: "Мисолҳо",
    meaning: "Маъно",
    when_used: "Куҷо истифода мешавад",
    when_not_used: "Куҷо ИСТИФОДА НАМЕШАВАД",
    collocations: "Таркибҳои маъмул",
    nuance: "Фарқ аз синонимҳо",
    register: "Услуб",
    generating: "Сохта мешавад…",
    loading: "Боргирӣ…",
    loading_list: "Рӯйхат боргирӣ мешавад…",
    error: "Хато",
    error_loading: "Хатои боргирӣ",
    added_to_srs: "Калима ба SRS илова шуд",
    review_done: "Такрор анҷом ёфт",
    deck_done: "Кортҳо анҷом ёфтанд",
    no_due: "Барои такрор корт нест",
    srs_again: "Боз",
    srs_hard: "Душвор",
    srs_good: "Хуб",
    srs_easy: "Осон",
    tts_no_voice: "Барои ин забон овоз нест",
    tts_not_supported: "Браузер овозро дастгирӣ намекунад",
    tts_nothing: "Барои хондан чизе нест",
  },
  id: {
    subtitle: "2460 kata · Level C1",
    meta: "DeepSeek · 3 contoh · penjelasan mendalam",
    loaded: "Dimuat", words: "kata",
    in_srs: "Di SRS", due: "Untuk diulang",
    explain_title: "Penjelasan mendalam",
    examples_title: "Contoh",
    meaning: "Arti",
    when_used: "Di mana digunakan",
    when_not_used: "Di mana TIDAK digunakan",
    collocations: "Kolokasi umum",
    nuance: "Nuansa vs sinonim",
    register: "Register",
    generating: "Menghasilkan…",
    loading: "Memuat…",
    loading_list: "Memuat daftar…",
    error: "Kesalahan",
    error_loading: "Gagal memuat",
    added_to_srs: "Kata ditambahkan ke SRS",
    review_done: "Ulasan selesai",
    deck_done: "Dek selesai",
    no_due: "Tidak ada kartu untuk diulang",
    srs_again: "Lagi",
    srs_hard: "Sulit",
    srs_good: "Bagus",
    srs_easy: "Mudah",
    tts_no_voice: "Tidak ada suara untuk bahasa ini",
    tts_not_supported: "Browser tidak mendukung suara",
    tts_nothing: "Belum ada yang dibaca",
  },
};

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
  currentContent: null,
};

function currentLang() {
  if (typeof getLang === "function") {
    try { const l = getLang(); if (l) return l; } catch(e) {}
  }
  try { const raw = localStorage.getItem("hsk5_lang"); if (raw) return raw; } catch(e) {}
  return "ru";
}

function t6(key) {
  const l = state.lang || "ru";
  return (T6[l] && T6[l][key]) || (T6.en && T6.en[key]) || key;
}

function updateUiTexts() {
  const map = {
    "t-subtitle": "subtitle",
    "t-meta": "meta",
    "t-explain-title": "explain_title",
    "t-examples-title": "examples_title",
    "t-srs-again": "srs_again",
    "t-srs-hard": "srs_hard",
    "t-srs-good": "srs_good",
    "t-srs-easy": "srs_easy",
  };
  for (const [id, key] of Object.entries(map)) {
    const el = document.getElementById(id);
    if (el) el.textContent = t6(key);
  }
}

// ============================================================
// TTS — одна кнопка читает всё
// ============================================================
const TTS = (function(){
  const synth = window.speechSynthesis;
  const supported = !!synth;
  let voices = [];
  let isPlaying = false;
  let stopFlag = false;
  let voicesReady = false;

  const LANG_MAP = {
    ru: ["ru-RU", "ru"],
    en: ["en-US", "en-GB", "en"],
    tk: ["tk-TM", "tr-TR", "tr", "en-US"],
    uz: ["uz-UZ", "uz", "tr-TR", "en-US"],
    tg: ["tg-TJ", "fa-IR", "fa", "ru-RU", "en-US"],
    id: ["id-ID", "id", "en-US"],
    tr: ["tr-TR", "tr", "en-US"],
    zh: ["zh-CN", "zh-Hans", "zh"],
  };

  function refreshVoices() {
    if (!supported) return;
    voices = synth.getVoices() || [];
    if (voices.length) voicesReady = true;
  }
  if (supported) {
    refreshVoices();
    try { synth.addEventListener("voiceschanged", refreshVoices); } catch(e){}
    setTimeout(refreshVoices, 500);
    setTimeout(refreshVoices, 1500);
  }

  function pickVoice(langKey) {
    const candidates = LANG_MAP[langKey] || [langKey];
    for (const code of candidates) {
      const base = code.split("-")[0].toLowerCase();
      const v = voices.find(x => (x.lang || "").toLowerCase() === code.toLowerCase())
             || voices.find(x => (x.lang || "").toLowerCase().startsWith(base + "-"))
             || voices.find(x => (x.lang || "").toLowerCase() === base);
      if (v) return v;
    }
    return null;
  }

  function hasNativeVoice(langKey) {
    const candidates = LANG_MAP[langKey] || [langKey];
    const nativeCode = candidates[0];
    const base = nativeCode.split("-")[0].toLowerCase();
    return voices.some(x => (x.lang || "").toLowerCase().startsWith(base));
  }

  function updateBtn() {
    const b = document.getElementById("tts-btn");
    if (!b) return;
    if (isPlaying) {
      b.classList.add("playing");
      b.textContent = "⏹";
      b.title = "Стоп";
    } else {
      b.classList.remove("playing");
      b.textContent = "🔊";
      b.title = "Слушать карточку";
    }
  }

  function stop() {
    if (!supported) return;
    stopFlag = true;
    try { synth.cancel(); } catch(e) {}
    isPlaying = false;
    updateBtn();
  }

  function speakOne(text, langKey) {
    return new Promise((resolve) => {
      if (stopFlag) { resolve(); return; }
      if (!supported || !text) { resolve(); return; }
      const u = new SpeechSynthesisUtterance(text);
      const v = pickVoice(langKey);
      if (v) u.voice = v;
      else if (voices[0]) u.voice = voices[0];
      u.lang = (v && v.lang) || (LANG_MAP[langKey] || [langKey])[0];
      u.rate = 0.95;
      u.pitch = 1.0;
      u.onend = () => resolve();
      u.onerror = () => resolve();
      try { synth.speak(u); } catch(e) { resolve(); }
    });
  }

  // items: [{text, lang}, ...]
  async function playQueue(items, onFallback) {
    if (!supported) { onFallback && onFallback("unsupported"); return; }
    stop();
    stopFlag = false;
    isPlaying = true;
    updateBtn();

    const anyFallback = items.some(it => !hasNativeVoice(it.lang));
    if (anyFallback && onFallback) onFallback("no_voice");

    for (const item of items) {
      if (stopFlag) break;
      await speakOne(item.text, item.lang);
    }

    isPlaying = false;
    stopFlag = false;
    updateBtn();
  }

  return {
    supported,
    stop,
    playQueue,
    isPlaying: () => isPlaying,
  };
})();

// ============================================================
// localStorage
// ============================================================
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

// ---------- Tracking ----------
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
  if (Date.now() - viewStartAt < AUTO_ADD_AFTER_MS) return false;
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
  clearTimeout(t._timer);
  t._timer = setTimeout(() => t.classList.remove("show"), 2400);
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
  TTS.stop();
  $("intro").style.display = "flex";
  $("card").style.display = "none";
  $("srs-bar").style.display = "none";
  $("progress-fill").style.width = "0%";
  const srsTotal = countSrsCards();
  const due = countDueCards();
  $("deck-info").innerHTML =
    `${t6("loaded")}: ${state.words.length} ${t6("words")}<br>
     <span style="font-size:12px">${t6("in_srs")}: <b>${srsTotal}</b> · ${t6("due")}: <b>${due}</b></span>`;
  injectReviewButton();
  updateReviewBadge();
}

function renderCard() {
  $("intro").style.display = "none";
  $("card").style.display = "block";
  $("srs-bar").style.display = "flex";
  renderCurrent();
}

async function renderCurrent() {
  TTS.stop();
  if (state.viewHanzi && state.viewStartAt) {
    const added = autoAddIfLong(state.viewHanzi, state.viewStartAt);
    if (added) toast(t6("added_to_srs"));
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

  $("explain-body").innerHTML = `<span class="explain-loading">${t6("generating")}</span>`;
  $("examples-body").innerHTML = `<span class="explain-loading">${t6("generating")}</span>`;

  if (state.contentCache.has(w.id)) {
    state.currentContent = state.contentCache.get(w.id);
    renderContent(state.currentContent);
    updateSrsPreviews();
    return;
  }
  try {
    const data = await fetchWord(w.id);
    if (data.content) {
      state.contentCache.set(w.id, data.content);
      state.currentContent = data.content;
      renderContent(data.content);
    } else {
      const gen = await generateContent(w.id);
      state.contentCache.set(w.id, gen);
      state.currentContent = gen;
      renderContent(gen);
    }
  } catch (e) {
    $("explain-body").innerHTML = `<span style="color:var(--cinnabar)">${t6("error")}: ${e.message}</span>`;
  }
  prefetchNext(1);
  updateSrsPreviews();
}

function renderContent(data) {
  const exp = data.explanation || {};
  const sections = [];
  if (exp.meaning)       sections.push([t6("meaning"), exp.meaning]);
  if (exp.when_used)     sections.push([t6("when_used"), exp.when_used]);
  if (exp.when_not_used) sections.push([t6("when_not_used"), exp.when_not_used]);
  if (exp.nuance)        sections.push([t6("nuance"), exp.nuance]);
  if (exp.register)      sections.push([t6("register"), exp.register]);

  let html = "";
  for (const [label, text] of sections) {
    html += `<div class="explain-section">
      <div class="explain-label">${label}</div>
      <div class="explain-text">${escapeHtml(text)}</div>
    </div>`;
  }
  if (exp.collocations && exp.collocations.length) {
    html += `<div class="explain-section">
      <div class="explain-label">${t6("collocations")}</div>
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
  TTS.stop();
  const w = currentWord();
  if (!w) return;
  autoAddIfLong(w.hanzi, state.viewStartAt);
  srsApplyRating(w.hanzi, rating);

  if (state.isReview) {
    state.reviewPos += 1;
    if (state.reviewPos >= state.reviewQueue.length) {
      toast(t6("review_done"));
      state.isReview = false;
      renderIntro();
      return;
    }
  } else {
    state.index = Math.min(state.index + 1, state.words.length - 1);
    lsSet(LS.pos, state.index);
    if (state.index >= state.words.length - 1 && w === state.words[state.words.length - 1]) {
      toast(t6("deck_done"));
      renderIntro();
      return;
    }
  }
  await renderCurrent();
}

async function startReview() {
  const db = srsLoad();
  const now = Date.now();
  let due = Object.entries(db).filter(([h, c]) => (c.due || 0) <= now).map(([h]) => h);
  if (!due.length) { toast(t6("no_due")); return; }
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

// ============================================================
// ЕДИНАЯ ФУНКЦИЯ ЧТЕНИЯ: кнопка читает всё подряд
// ============================================================
function buildReadQueue() {
  const w = currentWord();
  if (!w) return [];
  const data = state.currentContent;
  const lang = state.lang;
  const tr = (w.translations && w.translations[lang]) || (w.translations && w.translations.en) || "";

  const q = [];
  // 1) сам иероглиф
  q.push({ text: w.hanzi, lang: "zh" });
  // 2) pinyin (читаем китайским голосом — ближе к произношению)
  if (w.pinyin) q.push({ text: w.pinyin, lang: "zh" });
  // 3) перевод
  if (tr) q.push({ text: tr, lang: lang });

  // 4) глубокое объяснение
  if (data && data.explanation) {
    const exp = data.explanation;
    const parts = [];
    if (exp.meaning)       parts.push(exp.meaning);
    if (exp.when_used)     parts.push(exp.when_used);
    if (exp.when_not_used) parts.push(exp.when_not_used);
    if (exp.nuance)        parts.push(exp.nuance);
    if (exp.register)      parts.push(exp.register);
    if (parts.length) q.push({ text: parts.join(". "), lang: lang });
  }

  // 5) примеры: сначала китайский, потом перевод
  if (data && data.sentences && data.sentences.length) {
    for (const s of data.sentences) {
      if (s.zh) q.push({ text: s.zh, lang: "zh" });
      if (s.translation) q.push({ text: s.translation, lang: lang });
    }
  }
  return q;
}

function readAll() {
  const w = currentWord();
  if (!w) return;
  if (!state.currentContent) { toast(t6("tts_nothing")); return; }
  const queue = buildReadQueue();
  if (!queue.length) { toast(t6("tts_nothing")); return; }
  if (!TTS.supported) { toast(t6("tts_not_supported")); return; }

  TTS.playQueue(queue, (reason) => {
    if (reason === "no_voice") toast(t6("tts_no_voice"));
    if (reason === "unsupported") toast(t6("tts_not_supported"));
  });
}

function onTtsClick() {
  if (TTS.isPlaying()) {
    TTS.stop();
  } else {
    readAll();
  }
}

async function init() {
  state.lang = currentLang();
  state.index = lsGet(LS.pos, 0);

  updateUiTexts();

  $("start-btn").onclick = async () => {
    try {
      if (!state.words.length) {
        $("deck-info").textContent = t6("loading_list");
        await loadWords();
      }
      state.isReview = false;
      renderCard();
    } catch (e) { toast(t6("error_loading") + ": " + e.message); }
  };

  $("back-btn").onclick = () => {
    TTS.stop();
    if (state.viewHanzi && state.viewStartAt) autoAddIfLong(state.viewHanzi, state.viewStartAt);
    state.isReview = false;
    renderIntro();
  };

  // Единая TTS-кнопка
  const ttsBtn = $("tts-btn");
  if (ttsBtn) ttsBtn.onclick = onTtsClick;

  document.querySelectorAll("#rate-wrap .srs-btn").forEach(b => {
    b.onclick = () => rateAndNext(parseInt(b.dataset.rate, 10));
  });

  try { await loadWords(); renderIntro(); }
  catch (e) { $("deck-info").textContent = t6("error_loading") + ": " + e.message; }

  window.addEventListener("beforeunload", () => {
    if (state.viewHanzi && state.viewStartAt) autoAddIfLong(state.viewHanzi, state.viewStartAt);
  });

  window.addEventListener("lang_changed", () => {
    const nl = currentLang();
    if (nl !== state.lang) {
      state.lang = nl;
      state.contentCache.clear();
      _sortedWords = null;
      updateUiTexts();
      if ($("card").style.display !== "none") renderCurrent();
      else renderIntro();
    }
  });

  window.addEventListener("storage", (e) => {
    if (e.key === "hsk5_lang") {
      const nl = e.newValue || "ru";
      if (nl !== state.lang) {
        state.lang = nl;
        state.contentCache.clear();
        _sortedWords = null;
        updateUiTexts();
        if ($("card").style.display !== "none") renderCurrent();
        else renderIntro();
      }
    }
  });

  document.addEventListener("keydown", e => {
    // TTS по пробелу — работает и на intro, и на карточке
    if (e.code === "Space" && !$("card").style.display.match(/none/i)) {
      // если фокус не в input
      const tag = (e.target && e.target.tagName) || "";
      if (tag === "INPUT" || tag === "TEXTAREA") return;
    }
    if ($("card").style.display === "none") return;

    if (e.code === "Space") {
      e.preventDefault();
      rateAndNext(3);
    }
    if (e.key >= "1" && e.key <= "4") {
      rateAndNext(parseInt(e.key, 10));
    }
    if (e.key === "r" || e.key === "R") {
      onTtsClick();
    }
  });
}

document.addEventListener("DOMContentLoaded", init);
})();