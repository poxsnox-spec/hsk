# -*- coding: utf-8 -*-
"""HSK6 routes. Регистрируется из web/server.py:  import hsk6; hsk6.register(app)"""
import json
import sqlite3
import threading
import time
from pathlib import Path

from flask import jsonify, request, send_from_directory

from deepseek_client import chat_json

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "hsk6_data" / "hsk6.sqlite"
STATIC = ROOT / "web" / "static"

LANGS = ["ru", "en", "tk", "uz", "tg", "id"]

_db_lock = threading.Lock()

SYSTEM_PROMPT = (
    "Ты — старший преподаватель китайского HSK6. Пишешь естественно, "
    "в книжно-публицистическом регистре HSK6 (CEFR B2-C1). "
    "Никогда не выдумываешь грамматику — только реальный HSK6+."
)

USER_PROMPT = """Слово: {hanzi} ({pinyin}) — {translation}
Язык объяснения: {lang_name}

Сгенерируй РОВНО 3 предложения на китайском:
- Уровень лексики и грамматики HSK6 (B2-C1). Никаких простых HSK3-4 конструкций.
- В КАЖДОМ предложении присутствует "{hanzi}".
- Разные контексты: 1) бытовой, 2) публицистический/новостной, 3) книжно-абстрактный.

И глубокое объяснение:
- meaning — что значит на самом деле, включая подтекст.
- when_used — где ИСПОЛЬЗУЮТ (регистр, жанр).
- when_not_used — где УПОТРЕБЛЯТЬ НЕЛЬЗЯ и чем заменить (2-3 синонима с разницей).
- collocations — 4-6 устойчивых сочетаний (китайский + перевод).
- nuance — отличие от ближайших синонимов, коннотации.
- register — разговорный / нейтральный / книжный / официальный.

Верни СТРОГО JSON:
{{
  "sentences": [
    {{"zh":"...","pinyin":"...","translation":"..."}},
    {{"zh":"...","pinyin":"...","translation":"..."}},
    {{"zh":"...","pinyin":"...","translation":"..."}}
  ],
  "explanation": {{
    "meaning":"...", "when_used":"...", "when_not_used":"...",
    "collocations":[{{"zh":"...","translation":"..."}}],
    "nuance":"...", "register":"..."
  }}
}}"""

LANG_NAMES = {
    "ru": "русский", "en": "English", "tk": "türkmen dili",
    "uz": "o'zbek tili", "tg": "тоҷикӣ", "id": "Bahasa Indonesia",
}


def _db():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db


def _get_meta(word_id):
    with _db_lock:
        db = _db()
        row = db.execute(
            "SELECT word_id, hanzi, pinyin, translations FROM word_meta WHERE word_id=?",
            (word_id,),
        ).fetchone()
        db.close()
    return dict(row) if row else None


def _get_content(word_id, lang):
    with _db_lock:
        db = _db()
        row = db.execute(
            "SELECT sentences, explanation FROM word_content WHERE word_id=? AND lang=?",
            (word_id, lang),
        ).fetchone()
        db.close()
    if not row:
        return None
    return {"sentences": json.loads(row["sentences"]),
            "explanation": json.loads(row["explanation"])}


def _put_content(word_id, lang, sentences, explanation):
    with _db_lock:
        db = _db()
        db.execute(
            "INSERT OR REPLACE INTO word_content VALUES(?,?,?,?,?,?)",
            (word_id, lang,
             json.dumps(sentences, ensure_ascii=False),
             json.dumps(explanation, ensure_ascii=False),
             "deepseek-chat", int(time.time())),
        )
        db.commit()
        db.close()


def _generate(word_id, lang):
    meta = _get_meta(word_id)
    if not meta:
        return None
    tr = json.loads(meta.get("translations") or "{}").get(lang, "")
    prompt = USER_PROMPT.format(
        hanzi=meta["hanzi"], pinyin=meta.get("pinyin", ""),
        translation=tr, lang_name=LANG_NAMES.get(lang, "English"),
    )
    data = chat_json(
        [{"role": "system", "content": SYSTEM_PROMPT},
         {"role": "user", "content": prompt}],
        temperature=0.7,
    )
    _put_content(word_id, lang, data["sentences"], data["explanation"])
    return data


def register(app):
    @app.route("/hsk6")
    def hsk6_page():
        return send_from_directory(str(STATIC), "hsk6.html")

    @app.route("/api/hsk6/words")
    def hsk6_words():
        with _db_lock:
            db = _db()
            rows = db.execute(
                "SELECT word_id, hanzi, pinyin, translations FROM word_meta ORDER BY order_index"
            ).fetchall()
            db.close()
        return jsonify([{
            "id": r["word_id"], "hanzi": r["hanzi"], "pinyin": r["pinyin"],
            "translations": json.loads(r["translations"] or "{}"),
        } for r in rows])

    @app.route("/api/hsk6/word/<int:word_id>")
    def hsk6_word(word_id):
        lang = request.args.get("lang", "ru")
        if lang not in LANGS:
            lang = "ru"
        meta = _get_meta(word_id)
        if not meta:
            return jsonify({"error": "not found"}), 404
        content = _get_content(word_id, lang)
        return jsonify({
            "id": meta["word_id"],
            "hanzi": meta["hanzi"],
            "pinyin": meta["pinyin"],
            "translation": json.loads(meta["translations"] or "{}").get(lang, ""),
            "content": content,
        })

    @app.route("/api/hsk6/generate/<int:word_id>", methods=["POST"])
    def hsk6_generate(word_id):
        lang = (request.get_json(silent=True) or {}).get("lang", "ru")
        if lang not in LANGS:
            return jsonify({"error": "bad lang"}), 400
        cached = _get_content(word_id, lang)
        if cached:
            return jsonify(cached)
        try:
            data = _generate(word_id, lang)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify(data)