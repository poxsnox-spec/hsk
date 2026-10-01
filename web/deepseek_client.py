# -*- coding: utf-8 -*-
"""Общий DeepSeek-клиент. Переиспользует DEEPSEEK_API_KEY из env."""
import json
import os
import time

import requests

API_KEY = "".join(c for c in os.environ.get("DEEPSEEK_API_KEY", "") if 32 < ord(c) < 127)
BASE = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"


def chat(messages, temperature=0.7, retries=2):
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY не задан")
    payload = {"model": MODEL, "messages": messages, "temperature": temperature}
    last = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(
                BASE,
                headers={"Authorization": "Bearer " + API_KEY,
                         "Content-Type": "application/json"},
                json=payload,
                timeout=90,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
            last = "HTTP %s: %s" % (r.status_code, r.text[:200])
        except Exception as e:
            last = str(e)
        if attempt < retries:
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError("DeepSeek fail: " + str(last))


def chat_json(messages, temperature=0.7):
    if not API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY не задан")
    payload = {"model": MODEL, "messages": messages, "temperature": temperature,
               "response_format": {"type": "json_object"}}
    r = requests.post(
        BASE,
        headers={"Authorization": "Bearer " + API_KEY,
                 "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError("DeepSeek HTTP %s: %s" % (r.status_code, r.text[:300]))
    return json.loads(r.json()["choices"][0]["message"]["content"])