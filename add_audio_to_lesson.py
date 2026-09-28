#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_audio_to_lesson.py:
  1. Обновляет lesson01.json — ссылки на реальные mp3
  2. Патчит business_lesson.html — добавляет плеер в диалоги и словарь
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
JSON_FILE = ROOT / "data" / "business" / "lesson01.json"
HTML_FILE = ROOT / "web" / "static" / "business_lesson.html"

# ───── 1. Обновить JSON ─────
def update_json():
    d = json.loads(JSON_FILE.read_text(encoding="utf-8"))
    dlg = d.get("dialogs") or []
    if len(dlg) >= 2:
        dlg[0]["audio"] = "dialog_airport.mp3"
        dlg[1]["audio"] = "dialog_hotel.mp3"
    # Убираем старую ссылку на textbook_1, ставим vocab
    if "audio" not in d:
        d["audio"] = {}
    d["audio"]["dialog_airport"] = "dialog_airport.mp3"
    d["audio"]["dialog_hotel"]   = "dialog_hotel.mp3"
    d["audio"]["vocab"]          = "vocab.mp3"
    d["audio"]["base"] = f"/audio/business/lesson{d['lesson']:02d}/"
    bak = JSON_FILE.with_suffix(JSON_FILE.suffix + ".pre_audio.bak")
    if not bak.exists():
        shutil.copy2(JSON_FILE, bak)
    JSON_FILE.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
    print(f"OK: JSON — audio ссылки обновлены ({len(dlg)} диалога)")


# ───── 2. Патч HTML ─────
AUDIO_HELPERS = '''
// ═══════════════════════════════════════════════════════════
// Audio player helpers
// ═══════════════════════════════════════════════════════════
var _audioEls = {};

function renderAudioPlayer(audioId, src, label) {
  if (!src) return '';
  return '<div class="audio-player" style="display:flex;align-items:center;gap:8px;' +
    'padding:10px 14px;background:#e0f4f9;border-radius:10px;margin:12px 0;flex-wrap:wrap">' +
    '<button class="ap-btn ap-play" data-audio="' + audioId + '" ' +
      'style="width:38px;height:38px;border-radius:50%;border:0;background:#1a365d;color:#fff;' +
      'cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px">' +
      '<i class="fa-solid fa-play"></i></button>' +
    '<button class="ap-btn ap-rew" data-audio="' + audioId + '" ' +
      'style="padding:6px 12px;border-radius:8px;border:1px solid #1a365d;background:transparent;' +
      'color:#1a365d;cursor:pointer;font-size:12px">-5s</button>' +
    '<button class="ap-btn ap-fwd" data-audio="' + audioId + '" ' +
      'style="padding:6px 12px;border-radius:8px;border:1px solid #1a365d;background:transparent;' +
      'color:#1a365d;cursor:pointer;font-size:12px">+5s</button>' +
    '<select class="ap-speed" data-audio="' + audioId + '" ' +
      'style="padding:6px 8px;border-radius:8px;border:1px solid #cbd5e1;background:#fff;font-size:12px">' +
      '<option value="0.5">0.5×</option><option value="0.75">0.75×</option>' +
      '<option value="1.0" selected>1.0×</option><option value="1.25">1.25×</option>' +
      '<option value="1.5">1.5×</option><option value="2.0">2.0×</option></select>' +
    '<span style="font-size:12px;color:#64748b;margin-left:4px">' + (label || '') + '</span>' +
    '<audio id="' + audioId + '" preload="none" src="' + src + '"></audio>' +
    '</div>';
}

function bindAudioPlayers() {
  document.querySelectorAll(".ap-play").forEach(function(b) {
    b.addEventListener("click", function() {
      var id = b.dataset.audio;
      var a = document.getElementById(id);
      if (!a) return;
      if (a.paused) {
        // pause others
        Object.keys(_audioEls).forEach(function(k) {
          if (k !== id && !_audioEls[k].paused) _audioEls[k].pause();
        });
        a.play();
      } else a.pause();
    });
  });
  document.querySelectorAll(".ap-rew").forEach(function(b) {
    b.addEventListener("click", function() {
      var a = document.getElementById(b.dataset.audio);
      if (a) a.currentTime = Math.max(0, a.currentTime - 5);
    });
  });
  document.querySelectorAll(".ap-fwd").forEach(function(b) {
    b.addEventListener("click", function() {
      var a = document.getElementById(b.dataset.audio);
      if (a) a.currentTime = Math.min(a.duration || 1e9, a.currentTime + 5);
    });
  });
  document.querySelectorAll(".ap-speed").forEach(function(s) {
    s.addEventListener("change", function() {
      var a = document.getElementById(s.dataset.audio);
      if (a) a.playbackRate = parseFloat(s.value);
    });
  });
  // обновляем иконки play/pause
  document.querySelectorAll("audio").forEach(function(a) {
    _audioEls[a.id] = a;
    a.addEventListener("play", function() {
      var btn = document.querySelector('.ap-play[data-audio="' + a.id + '"] i');
      if (btn) btn.className = "fa-solid fa-pause";
    });
    a.addEventListener("pause", function() {
      var btn = document.querySelector('.ap-play[data-audio="' + a.id + '"] i');
      if (btn) btn.className = "fa-solid fa-play";
    });
    a.addEventListener("ended", function() {
      var btn = document.querySelector('.ap-play[data-audio="' + a.id + '"] i');
      if (btn) btn.className = "fa-solid fa-play";
    });
  });
}
'''

# Старый блок renderText — заменить, добавив плеер перед строками диалога
OLD_RENDER_TEXT = '''function renderText() {
  var dlg = data.dialogs || [];
  if (!dlg.length) return '<div class="text-slate-400 text-center py-20">' + t("no_dialogs") + '</div>';
  var html = "";
  dlg.forEach(function(d, i) {
    var sc = d.scene || {};
    html += '<div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">';
    html += '<div class="flex items-center justify-between mb-4">' +
      '<div><span class="text-xs text-slate-400 uppercase tracking-wide">' + t("dialog") + ' ' + (i+1) + '</span>' +
      '<div class="text-lg font-bold text-brand-navy">' + esc(sc.zh || "") + ' · ' + esc(pick(sc)) + '</div></div>' +
      '<button class="text-xs text-brand-cyan hover:text-brand-navy" onclick="toggleTranslations()">' +
      '<i class="fa-solid fa-eye mr-1"></i>' + t("translation_btn") + '</button></div>';
    (d.lines || []).forEach(function(ln) {
      html += '<div class="dialog-line">' +
        '<div class="text-xs text-slate-400 mb-1">' + esc(ln.speaker || "") + '</div>' +
        '<div class="text-base font-medium text-slate-800">' + esc(ln.zh || "") + '</div>' +
        (has(ln.pinyin) ? '<div class="text-xs text-slate-400 mt-1 font-mono">' + esc(ln.pinyin) + '</div>' : '') +
        (pick(ln) ? '<div class="trans-block mt-1"><div class="text-sm text-slate-600">' + esc(pick(ln)) + '</div></div>' : '') +
        '</div>';
    });
    html += '</div>';
  });
  return html;
}'''

NEW_RENDER_TEXT = '''function renderText() {
  var dlg = data.dialogs || [];
  if (!dlg.length) return '<div class="text-slate-400 text-center py-20">' + t("no_dialogs") + '</div>';
  var base = (data.audio && data.audio.base) ? data.audio.base : "/audio/business/lesson01/";
  var html = "";
  dlg.forEach(function(d, i) {
    var sc = d.scene || {};
    html += '<div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 mb-6">';
    html += '<div class="flex items-center justify-between mb-4">' +
      '<div><span class="text-xs text-slate-400 uppercase tracking-wide">' + t("dialog") + ' ' + (i+1) + '</span>' +
      '<div class="text-lg font-bold text-brand-navy">' + esc(sc.zh || "") + ' · ' + esc(pick(sc)) + '</div></div>' +
      '<button class="text-xs text-brand-cyan hover:text-brand-navy" onclick="toggleTranslations()">' +
      '<i class="fa-solid fa-eye mr-1"></i>' + t("translation_btn") + '</button></div>';
    // ── AUDIO PLAYER ──
    if (d.audio) {
      var audioId = "aud-dialog-" + i;
      var src = base + d.audio;
      html += renderAudioPlayer(audioId, src, "");
    }
    (d.lines || []).forEach(function(ln) {
      html += '<div class="dialog-line">' +
        '<div class="text-xs text-slate-400 mb-1">' + esc(ln.speaker || "") + '</div>' +
        '<div class="text-base font-medium text-slate-800">' + esc(ln.zh || "") + '</div>' +
        (has(ln.pinyin) ? '<div class="text-xs text-slate-400 mt-1 font-mono">' + esc(ln.pinyin) + '</div>' : '') +
        (pick(ln) ? '<div class="trans-block mt-1"><div class="text-sm text-slate-600">' + esc(pick(ln)) + '</div></div>' : '') +
        '</div>';
    });
    html += '</div>';
  });
  return html;
}'''

# Обновить renderVocab — добавить плеер вверху
OLD_RENDER_VOCAB = '''function renderVocab() {
  var v = data.vocabulary || [];
  if (!v.length) return '<div class="text-slate-400 text-center py-20">' + t("no_vocab") + '</div>';
  var html = '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';'''

NEW_RENDER_VOCAB = '''function renderVocab() {
  var v = data.vocabulary || [];
  if (!v.length) return '<div class="text-slate-400 text-center py-20">' + t("no_vocab") + '</div>';
  var base = (data.audio && data.audio.base) ? data.audio.base : "/audio/business/lesson01/";
  var html = '';
  if (data.audio && data.audio.vocab) {
    html += renderAudioPlayer("aud-vocab", base + data.audio.vocab, "");
  }
  html += '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">';'''

# renderTab — вызвать bindAudioPlayers() после вставки HTML
OLD_RENDER_TAB = '''function renderTab() {
  var c = document.getElementById("biz-content");
  var fns = { text: renderText, vocab: renderVocab, expr: renderExpr, grammar: renderGrammar, exercises: renderExercises, workbook: renderWorkbook };
  var fn = fns[currentTab] || renderText;
  c.innerHTML = fn();
}'''

NEW_RENDER_TAB = '''function renderTab() {
  var c = document.getElementById("biz-content");
  var fns = { text: renderText, vocab: renderVocab, expr: renderExpr, grammar: renderGrammar, exercises: renderExercises, workbook: renderWorkbook };
  var fn = fns[currentTab] || renderText;
  c.innerHTML = fn();
  if (typeof bindAudioPlayers === "function") bindAudioPlayers();
}'''


def check_braces(src, name):
    o, c = src.count("{"), src.count("}")
    return o == c, f"{name}: {{ }} {o}/{c}"


def patch_html():
    src = HTML_FILE.read_text(encoding="utf-8")

    if "renderAudioPlayer" in src:
        print("HTML уже пропатчен")
        return

    # 1. Добавляем хелперы после getTABS()
    # Ищем конец функции getTABS
    m = re.search(r'function\s+getTABS\s*\([^)]*\)\s*\{', src)
    if not m:
        print("!! не нашёл function getTABS")
        return
    # найти парную }
    i = src.find("{", m.end() - 1)
    depth = 0
    j = i
    in_str = None
    esc = False
    while j < len(src):
        ch = src[j]
        if esc: esc = False
        elif ch == "\\": esc = True
        elif in_str:
            if ch == in_str: in_str = None
        elif ch in ('"', "'", "`"): in_str = ch
        elif ch == "{": depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                src = src[:j+1] + "\n" + AUDIO_HELPERS + src[j+1:]
                break
        j += 1

    # 2. renderText
    if OLD_RENDER_TEXT in src:
        src = src.replace(OLD_RENDER_TEXT, NEW_RENDER_TEXT, 1)
        print("  ✓ renderText — добавлен плеер")
    else:
        print("  !! не нашёл старый renderText")

    # 3. renderVocab
    if OLD_RENDER_VOCAB in src:
        src = src.replace(OLD_RENDER_VOCAB, NEW_RENDER_VOCAB, 1)
        print("  ✓ renderVocab — добавлен плеер")
    else:
        print("  !! не нашёл старый renderVocab")

    # 4. renderTab
    if OLD_RENDER_TAB in src:
        src = src.replace(OLD_RENDER_TAB, NEW_RENDER_TAB, 1)
        print("  ✓ renderTab — вызывает bindAudioPlayers()")
    else:
        print("  !! не нашёл старый renderTab")

    ok, msg = check_braces(src, "HTML")
    print(msg)
    if not ok:
        print("!! НЕ пишу HTML")
        return

    bak = HTML_FILE.with_suffix(HTML_FILE.suffix + ".pre_audio.bak")
    shutil.copy2(HTML_FILE, bak)
    HTML_FILE.write_text(src, encoding="utf-8")
    print(f"OK: {HTML_FILE.name} обновлён")
    print(f"Бэкап: {bak.name}")


def main():
    print("=" * 60)
    print("ПОДКЛЮЧЕНИЕ АУДИО К УРОКУ 1")
    print("=" * 60)
    update_json()
    print()
    patch_html()
    print()
    print("Дальше: Ctrl+Shift+R в браузере")
    print("Проверь: /business/lesson/1 → вкладки Text и Words")


if __name__ == "__main__":
    main()