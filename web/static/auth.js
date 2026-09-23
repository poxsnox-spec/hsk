// HSK 5 Learner — авторизация
(function () {
  "use strict";

  const app = () => document.getElementById("app");
  let currentUser = null;

  // ============================================================
  // Стили
  // ============================================================
  function ensureStyles() {
    if (document.getElementById("hsk-auth-styles")) return;
    const s = document.createElement("style");
    s.id = "hsk-auth-styles";
    s.textContent = `
      .auth-wrap {
        max-width: 420px;
        margin: 40px auto 20px;
        padding: 32px 28px;
        border-radius: 18px;
        background: rgba(20, 32, 48, 0.9);
        box-shadow:
          0 20px 60px rgba(0,0,0,0.5),
          0 0 0 1px rgba(102,178,255,0.15) inset;
        color: #F0F4F8;
      }
      .auth-logo {
        text-align: center;
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 6px;
        background: linear-gradient(90deg,#66B2FF,#5CD68E);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: #66B2FF;
      }
      .auth-sub {
        text-align: center;
        color: #8B9AAB;
        font-size: 13px;
        margin-bottom: 22px;
      }
      .auth-tabs {
        display: flex;
        gap: 6px;
        margin-bottom: 22px;
        background: rgba(0,0,0,0.25);
        padding: 4px;
        border-radius: 10px;
      }
      .auth-tab {
        flex: 1;
        padding: 10px;
        text-align: center;
        border: 0;
        background: transparent;
        color: #8B9AAB;
        cursor: pointer;
        font-size: 14px;
        border-radius: 8px;
        font-weight: 600;
      }
      .auth-tab.active {
        background: #4a9eff;
        color: #fff;
      }
      .auth-label {
        display: block;
        font-size: 13px;
        color: #8B9AAB;
        margin-bottom: 6px;
        margin-top: 14px;
      }
      .auth-input {
        width: 100%;
        padding: 12px 14px;
        border-radius: 10px;
        border: 1px solid #2c3e50;
        background: #0e1620;
        color: #fff;
        font-size: 15px;
        box-sizing: border-box;
        outline: none;
      }
      .auth-input:focus { border-color: #4a9eff; }
      .auth-btn {
        width: 100%;
        padding: 14px;
        border-radius: 12px;
        background: linear-gradient(135deg,#4a9eff,#66B2FF);
        color: #fff;
        border: 0;
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        margin-top: 22px;
      }
      .auth-btn:hover { opacity: 0.92; }
      .auth-btn:disabled { opacity: 0.5; cursor: wait; }
      .auth-msg {
        margin-top: 14px;
        font-size: 14px;
        text-align: center;
        min-height: 20px;
      }
      .auth-msg.error { color: #FF6B6B; }
      .auth-msg.ok    { color: #5CD68E; }
      .auth-msg.info  { color: #8B9AAB; }
      .auth-footer {
        text-align: center;
        font-size: 12px;
        color: #5a6b7a;
        margin-top: 26px;
      }
      .auth-icon-big {
        text-align: center;
        font-size: 60px;
        margin: 8px 0 18px;
      }
    `;
    document.head.appendChild(s);
  }

  // ============================================================
  // Утилиты
  // ============================================================
  function setMsg(el, text, kind) {
    if (!el) return;
    el.className = "auth-msg " + (kind || "");
    el.textContent = text || "";
  }

  function esc(s) {
    if (!s) return "";
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  async function api(url, opts) {
    const r = await fetch(url, Object.assign({
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
    }, opts || {}));
    let data = {};
    try { data = await r.json(); } catch (e) {}
    return { status: r.status, ok: r.ok, data };
  }

  // ============================================================
  // ЭКРАН: ВХОД / РЕГИСТРАЦИЯ
  // ============================================================
  function showAuthScreen(tab) {
    ensureStyles();
    tab = tab || "login";

    app().innerHTML = `
      <div class="auth-wrap">
        <div class="auth-logo">HSK 5 Learner</div>
        <div class="auth-sub">HSK 标准教程 5 上 · веб-версия</div>
        <div class="auth-tabs">
          <button class="auth-tab ${tab === "login" ? "active" : ""}" id="tab-login">Вход</button>
          <button class="auth-tab ${tab === "register" ? "active" : ""}" id="tab-register">Регистрация</button>
        </div>
        <div id="auth-form-slot"></div>
        <div id="auth-msg" class="auth-msg"></div>
        <div class="auth-footer">RU · TK · EN · UZ · TG</div>
      </div>`;

    document.getElementById("tab-login").onclick = () => showAuthScreen("login");
    document.getElementById("tab-register").onclick = () => showAuthScreen("register");

    if (tab === "login") renderLoginForm();
    else renderRegisterForm();
  }

  function renderLoginForm() {
    const slot = document.getElementById("auth-form-slot");
    slot.innerHTML = `
      <label class="auth-label">Email</label>
      <input id="li-email" class="auth-input" type="email" autocomplete="email">
      <label class="auth-label">Пароль</label>
      <input id="li-pass" class="auth-input" type="password" autocomplete="current-password">
      <button id="li-btn" class="auth-btn">Войти</button>
      <div style="text-align:center;margin-top:14px">
        <a href="#forgot" id="li-forgot" style="color:#8B9AAB;font-size:13px;text-decoration:none">
          Забыли пароль?
        </a>
      </div>`;

    const msg = document.getElementById("auth-msg");
    const email = document.getElementById("li-email");
    const pass = document.getElementById("li-pass");
    const btn = document.getElementById("li-btn");

    async function doLogin() {
      setMsg(msg, "");
      const e = email.value.trim();
      const p = pass.value;
      if (!e || !p) return setMsg(msg, "Заполните все поля", "error");
      btn.disabled = true;
      setMsg(msg, "Проверяю...", "info");
      const r = await api("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email: e, password: p }),
      });
      btn.disabled = false;
      if (r.ok) {
        currentUser = r.data.user;
        window.HSK_USER = currentUser;
        await loadProgress();
        setMsg(msg, "Успех", "ok");
        // перезагружаем приложение
        window.location.hash = "menu";
        window.location.reload();
      } else {
        setMsg(msg, r.data.error || "Ошибка входа", "error");
        if (r.data.need_activation) {
          setTimeout(() => showPendingScreen(r.data.email), 600);
        }
      }
    }

    btn.onclick = doLogin;
    pass.addEventListener("keydown", ev => { if (ev.key === "Enter") doLogin(); });
  }

  function renderRegisterForm() {
    const slot = document.getElementById("auth-form-slot");
    slot.innerHTML = `
      <label class="auth-label">Имя</label>
      <input id="rg-name" class="auth-input" type="text" autocomplete="name">
      <label class="auth-label">Email</label>
      <input id="rg-email" class="auth-input" type="email" autocomplete="email">
      <label class="auth-label">Пароль (минимум 6 символов)</label>
      <input id="rg-pass" class="auth-input" type="password" autocomplete="new-password">
      <button id="rg-btn" class="auth-btn">Создать аккаунт</button>`;

    const msg = document.getElementById("auth-msg");
    const name = document.getElementById("rg-name");
    const email = document.getElementById("rg-email");
    const pass = document.getElementById("rg-pass");
    const btn = document.getElementById("rg-btn");

    async function doRegister() {
      setMsg(msg, "");
      const n = name.value.trim();
      const e = email.value.trim();
      const p = pass.value;
      if (!n || !e || !p) return setMsg(msg, "Заполните все поля", "error");
      if (p.length < 6) return setMsg(msg, "Пароль минимум 6 символов", "error");
      btn.disabled = true;
      setMsg(msg, "Создаю аккаунт...", "info");
      const r = await api("/api/auth/register", {
        method: "POST",
        body: JSON.stringify({ name: n, email: e, password: p }),
      });
      btn.disabled = false;
      if (!r.ok) return setMsg(msg, r.data.error || "Ошибка", "error");
      if (r.data.is_admin) {
        setMsg(msg, "Админ — входим...", "ok");
        setTimeout(() => window.location.reload(), 500);
        return;
      }
      showPendingScreen(r.data.email);
    }

    btn.onclick = doRegister;
    pass.addEventListener("keydown", ev => { if (ev.key === "Enter") doRegister(); });
  }

  // ============================================================
  // ЭКРАН: письмо отправлено
  // ============================================================
  function showPendingScreen(email) {
    app().innerHTML = `
      <div class="auth-wrap">
        <div class="auth-icon-big">📬</div>
        <div class="auth-logo" style="font-size:22px">Проверьте почту</div>
        <div class="auth-sub" style="font-size:14px;line-height:1.6;margin-top:14px">
          Мы отправили письмо с ссылкой для активации на<br>
          <b style="color:#66B2FF">${esc(email)}</b>
        </div>
        <div class="auth-sub" style="font-size:13px;margin-top:14px">
          Перейдите по ссылке в письме, чтобы активировать аккаунт.
          Если не пришло — проверьте «Спам».
        </div>
        <button id="resend-btn" class="auth-btn" style="background:#2a3f5a">
          Отправить письмо ещё раз
        </button>
        <button id="back-btn" class="auth-btn" style="background:transparent;color:#8B9AAB;font-weight:400;font-size:14px;padding:10px">
          ← Назад ко входу
        </button>
        <div id="resend-msg" class="auth-msg"></div>
      </div>`;

    document.getElementById("back-btn").onclick = () => showAuthScreen("login");
    const btn = document.getElementById("resend-btn");
    const msg = document.getElementById("resend-msg");
    btn.onclick = async () => {
      btn.disabled = true;
      setMsg(msg, "Отправляю...", "info");
      const r = await api("/api/auth/resend", {
        method: "POST", body: JSON.stringify({ email }),
      });
      btn.disabled = false;
      if (r.ok) setMsg(msg, "Письмо отправлено ещё раз", "ok");
      else setMsg(msg, r.data.error || "Ошибка", "error");
    };
  }

  // ============================================================
  // АКТИВАЦИЯ (по ссылке #activate/TOKEN)
  // ============================================================
  async function doActivate(token) {
    ensureStyles();
    app().innerHTML = `
      <div class="auth-wrap">
        <div class="auth-icon-big" id="act-icon">⏳</div>
        <div class="auth-logo" style="font-size:22px" id="act-title">Активация...</div>
        <div id="act-msg" class="auth-msg info">Подождите секунду</div>
      </div>`;

    const r = await api("/api/auth/activate/" + encodeURIComponent(token));
    const icon = document.getElementById("act-icon");
    const title = document.getElementById("act-title");
    const msg = document.getElementById("act-msg");
    if (r.ok) {
      icon.textContent = "🎉";
      title.textContent = "Аккаунт активирован!";
      setMsg(msg, "Сейчас откроем приложение...", "ok");
      currentUser = r.data.user;
      window.HSK_USER = currentUser;
      await loadProgress();
      setTimeout(() => {
        window.location.hash = "menu";
        window.location.reload();
      }, 1200);
    } else {
      icon.textContent = "⚠";
      title.textContent = "Не удалось активировать";
      setMsg(msg, r.data.error || "Ошибка", "error");
      const b = document.createElement("button");
      b.className = "auth-btn";
      b.textContent = "Перейти ко входу";
      b.onclick = () => { window.location.hash = ""; showAuthScreen("login"); };
      msg.parentNode.appendChild(b);
    }
  }

  // ============================================================
  // PROGRESS SYNC
  // ============================================================
  const SYNC_KEYS = ["hsk5_activity", "hsk5_lessons_opened",
                     "hsk5_srs", "hsk5_settings"];

  async function loadProgress() {
    try {
      const r = await api("/api/progress", { method: "GET" });
      if (!r.ok) return;
      const serverData = r.data || {};
      for (const k of SYNC_KEYS) {
        if (k in serverData) {
          try {
            localStorage.setItem(k, JSON.stringify(serverData[k]));
          } catch (e) {}
        }
      }
    } catch (e) { /* offline — работаем на локальном */ }
  }

  let syncTimers = {};
  function syncKey(key, value) {
    if (!SYNC_KEYS.includes(key)) return;
    if (!currentUser) return;
    clearTimeout(syncTimers[key]);
    syncTimers[key] = setTimeout(() => {
      fetch("/api/progress/" + encodeURIComponent(key), {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({ value }),
      }).catch(() => {});
    }, 400);  // debounce 400 мс
  }

  async function logout() {
    try { await api("/api/auth/logout", { method: "POST" }); } catch (e) {}
    // чистим localStorage — данные пользователя
    for (const k of SYNC_KEYS) {
      try { localStorage.removeItem(k); } catch (e) {}
    }
    currentUser = null;
    window.HSK_USER = null;
    window.location.hash = "";
    window.location.reload();
  }

  // ============================================================
  // Экспорт
  // ============================================================
  window.HSKAuth = {
    showAuthScreen,
    doActivate,
    loadProgress,
    syncKey,
    logout,
    getUser: () => currentUser,
  };

  // Подхватываем пользователя, если уже залогинен
  fetch("/api/auth/me", { credentials: "same-origin" })
    .then(r => r.json())
    .then(j => {
      if (j && j.user) {
        currentUser = j.user;
        window.HSK_USER = j.user;
      }
    })
    .catch(() => {});
})();