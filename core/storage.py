# -*- coding: utf-8 -*-
"""Хранилище прогресса: SM-2 + общий прогресс. Работает с активным профилем."""
import json
from datetime import datetime, date, timedelta
from typing import Any, Dict
from core.profiles import profiles


# ============================================================
SM2_MIN_EASE = 1.3
SM2_DEFAULT_EASE = 2.5
SM2_EASY_BONUS = 1.3
SM2_HARD_MULT = 1.2
SM2_GRADUATING_INTERVAL = 4

LEARNING_STEPS = [1, 10]
RELEARNING_STEPS = [10]

RATING_AGAIN = 1
RATING_HARD = 2
RATING_GOOD = 3
RATING_EASY = 4

SCHEMA_VERSION = 2


def _now() -> datetime:
    return datetime.now()


def _iso(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


def _progress_file():
    return profiles.get_active_progress_file()


class Storage:
    def __init__(self):
        self._data: Dict[str, Any] = self._load()

    # ------------------------------------------------------------
    def reload(self):
        """Перезагружает данные (при смене профиля)."""
        self._data = self._load()

    def _load(self) -> Dict[str, Any]:
        path = _progress_file()
        if not path.exists():
            return self._default()
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[storage] ошибка чтения: {e}")
            return self._default()

        if data.get("srs_schema", 0) < SCHEMA_VERSION:
            print("[storage] Миграция SRS: старая схема → SM-2")
            data["srs"] = {}
            data["srs_schema"] = SCHEMA_VERSION
        return data

    def _default(self) -> Dict[str, Any]:
        return {
            "language": "ru",
            "completed_lessons": [],
            "lesson_scores": {},
            "vocab_stats": {},
            "last_lesson": None,
            "srs": {},
            "srs_schema": SCHEMA_VERSION,
            "activity": {},
            "streak_days": 0,
            "streak_last": None,
            "profile_name": "",
            "profile_started": None,
            "srs_session_size": 20,
            "srs_new_limit": 10,
            "sound_enabled": True,
            "accent_color": "blue",
        }

    def save(self):
        path = _progress_file()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[storage] ошибка записи: {e}")

    # ------------------------------------------------------------
    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def mark_lesson_complete(self, lesson_id: str):
        if lesson_id not in self._data["completed_lessons"]:
            self._data["completed_lessons"].append(lesson_id)
            self.save()

    def update_score(self, lesson_id: str, correct: int, total: int):
        scores = self._data.setdefault("lesson_scores", {})
        rec = scores.setdefault(lesson_id,
                                {"best": 0, "total": total, "attempts": 0})
        rec["attempts"] += 1
        rec["best"] = max(rec["best"], correct)
        rec["total"] = total
        self.save()

    def record_word(self, hanzi: str, correct: bool):
        stats = self._data.setdefault("vocab_stats", {})
        rec = stats.setdefault(hanzi, {"seen": 0, "correct": 0})
        rec["seen"] += 1
        if correct:
            rec["correct"] += 1
        self.save()

    # -------------------- SM-2 --------------------
    def _ensure_card(self, hanzi: str) -> Dict:
        srs = self._data.setdefault("srs", {})
        if hanzi not in srs:
            srs[hanzi] = {
                "state": "new", "step": 0,
                "ease": SM2_DEFAULT_EASE, "interval": 0,
                "due": _iso(_now()), "reps": 0, "lapses": 0,
                "last": None,
            }
        return srs[hanzi]

    def srs_get(self, hanzi: str):
        return self._data.get("srs", {}).get(hanzi)

    def srs_due(self):
        srs = self._data.get("srs", {})
        now = _iso(_now())
        return [hz for hz, rec in srs.items()
                if rec.get("due") and rec["due"] <= now]

    def srs_review(self, hanzi: str, rating: int):
        rec = self._ensure_card(hanzi)
        now = _now()
        rec["last"] = _iso(now)
        rec["reps"] = rec.get("reps", 0) + 1
        state = rec.get("state", "new")

        if state in ("new", "learning"):
            self._handle_learning(rec, rating, now, LEARNING_STEPS, "review")
        elif state == "review":
            self._handle_review(rec, rating, now)
        elif state == "relearning":
            self._handle_learning(rec, rating, now, RELEARNING_STEPS, "review")

        self._data["srs"][hanzi] = rec
        self.record_activity(1)
        self.save()

    def _handle_learning(self, rec, rating, now, steps, grad_state):
        step = rec.get("step", 0)
        if rating == RATING_AGAIN:
            rec["state"] = ("learning" if steps is LEARNING_STEPS
                            else "relearning")
            rec["step"] = 0
            rec["due"] = _iso(now + timedelta(minutes=steps[0]))
        elif rating == RATING_HARD:
            rec["due"] = _iso(now + timedelta(
                minutes=steps[min(step, len(steps) - 1)]))
        elif rating == RATING_GOOD:
            step += 1
            if step >= len(steps):
                rec["state"] = grad_state
                rec["step"] = 0
                rec["interval"] = SM2_GRADUATING_INTERVAL
                rec["due"] = _iso(now + timedelta(days=rec["interval"]))
            else:
                rec["step"] = step
                rec["due"] = _iso(now + timedelta(minutes=steps[step]))
        elif rating == RATING_EASY:
            rec["state"] = grad_state
            rec["step"] = 0
            rec["interval"] = int(round(
                SM2_GRADUATING_INTERVAL * SM2_EASY_BONUS))
            rec["due"] = _iso(now + timedelta(days=rec["interval"]))

    def _handle_review(self, rec, rating, now):
        ease = rec.get("ease", SM2_DEFAULT_EASE)
        interval = max(1, rec.get("interval", 1))
        if rating == RATING_AGAIN:
            rec["lapses"] = rec.get("lapses", 0) + 1
            rec["ease"] = max(SM2_MIN_EASE, ease - 0.20)
            rec["state"] = "relearning"
            rec["step"] = 0
            rec["interval"] = max(1, int(round(interval * 0.5)))
            rec["due"] = _iso(now + timedelta(minutes=RELEARNING_STEPS[0]))
        elif rating == RATING_HARD:
            rec["ease"] = max(SM2_MIN_EASE, ease - 0.15)
            rec["interval"] = max(1, int(round(interval * SM2_HARD_MULT)))
            rec["due"] = _iso(now + timedelta(days=rec["interval"]))
        elif rating == RATING_GOOD:
            rec["interval"] = max(1, int(round(interval * ease)))
            rec["due"] = _iso(now + timedelta(days=rec["interval"]))
        elif rating == RATING_EASY:
            rec["ease"] = ease + 0.15
            rec["interval"] = max(1, int(round(
                interval * ease * SM2_EASY_BONUS)))
            rec["due"] = _iso(now + timedelta(days=rec["interval"]))

    def srs_stats(self):
        srs = self._data.get("srs", {})
        out = {"new": 0, "learning": 0, "review": 0, "relearning": 0}
        for rec in srs.values():
            st = rec.get("state", "new")
            out[st] = out.get(st, 0) + 1
        return out

    def srs_total_known(self):
        return len(self._data.get("srs", {}))

    def srs_interval_distribution(self):
        srs = self._data.get("srs", {})
        buckets = [0, 0, 0, 0, 0]
        for rec in srs.values():
            if rec.get("state") != "review":
                continue
            i = rec.get("interval", 0)
            if i < 7:     buckets[0] += 1
            elif i < 30:  buckets[1] += 1
            elif i < 90:  buckets[2] += 1
            elif i < 180: buckets[3] += 1
            else:         buckets[4] += 1
        return buckets

    def srs_ease_avg(self):
        srs = self._data.get("srs", {})
        revs = [r["ease"] for r in srs.values() if r.get("state") == "review"]
        return round(sum(revs) / len(revs), 2) if revs else 0.0

    # -------------------- Activity / Streak --------------------
    def record_activity(self, count: int = 1):
        today = date.today().isoformat()
        activity = self._data.setdefault("activity", {})
        activity[today] = activity.get(today, 0) + count

        last = self._data.get("streak_last")
        if last == today:
            pass
        else:
            yesterday = (date.today() - timedelta(days=1)).isoformat()
            if last == yesterday:
                self._data["streak_days"] = self._data.get("streak_days", 0) + 1
            else:
                self._data["streak_days"] = 1
            self._data["streak_last"] = today

    def srs_forecast(self, days: int = 7):
        srs = self._data.get("srs", {})
        today = date.today()
        result = []
        for d in range(days):
            day = (today + timedelta(days=d)).isoformat()
            cnt = sum(1 for r in srs.values()
                      if r.get("due", "").startswith(day))
            result.append((day, cnt))
        return result


# Глобальный синглтон
storage = Storage()
