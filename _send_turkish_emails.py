#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Активирует Gowher и отправляет 2 письма на турецком через Brevo."""
import os
import sqlite3
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
DB = ROOT / "data" / "users.db"

BREVO_KEY = os.environ.get("BREVO_KEY", "").strip()
FROM_EMAIL = "poxsnox@gmail.com"
FROM_NAME = "HSK 5 Learner"
PUBLIC_URL = "https://alelatdin.pythonanywhere.com"


# ============================================================
# ПИСЬМО 1 — обновления (Wepa)
# ============================================================
EMAIL_UPDATES = {
    "subject": "HSK 5 Learner — Yeni Güncellemeler ve Türkçe Desteği",
    "html": """<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0e1620;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
<div style="max-width:600px;margin:0 auto;padding:32px 24px;">

  <div style="text-align:center;margin-bottom:28px;">
    <div style="font-size:28px;font-weight:800;letter-spacing:0.5px;color:#66B2FF;">中文 · HSK 5 Learner</div>
    <div style="font-size:13px;color:#8B9AAB;margin-top:4px;">Çince öğrenme platformunuz</div>
  </div>

  <div style="background:linear-gradient(160deg,#1b2333 0%,#141a26 100%);border:1px solid #2a3446;border-radius:16px;padding:28px 26px;">

    <h1 style="font-size:20px;margin:0 0 16px;color:#E6EDF5;">
      Sayın {name},
    </h1>

    <p style="font-size:15px;line-height:1.65;color:#D9E6F2;margin:0 0 18px;">
      HSK 5 Learner ailesinin bir üyesi olduğunuz için teşekkür ederiz.
      Öğrenme deneyiminizi geliştirmek amacıyla platformumuzda önemli
      güncellemeler yayınladık.
    </p>

    <div style="font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#66B2FF;margin:24px 0 12px;font-weight:700;">
      Yeni Özellikler
    </div>

    <ul style="font-size:14.5px;line-height:1.7;color:#D9E6F2;margin:0;padding-left:22px;">
      <li style="margin-bottom:10px;">
        <b style="color:#7EE0FF;">Türkçe dil desteği</b> — Arayüzün tamamı artık
        Türkçe olarak kullanılabilir. Menüler, butonlar, tüm ekranlar ve
        kelime çevirileri Türkçeye kazandırıldı.
      </li>
      <li style="margin-bottom:10px;">
        <b style="color:#7EE0FF;">HSK 6 modülü</b> — 2.460 resmî HSK 6 kelimesi,
        her biri için yapay zekâ tarafından oluşturulmuş derinlemesine
        açıklamalar, kullanım alanları ve üç örnek cümle ile birlikte.
      </li>
      <li style="margin-bottom:10px;">
        <b style="color:#7EE0FF;">Sesli okuma</b> — HSK 6 kelime kartlarında
        tek bir butonla kartın tamamını dinleyebilirsiniz: karakter, pinyin,
        çeviri, açıklama ve tüm örnek cümleler sırayla okunur.
      </li>
      <li style="margin-bottom:10px;">
        <b style="color:#7EE0FF;">HSK 5 dersleri Türkçe</b> — 18 dersin tamamı
        ve İş Çincesi kursunun 15 dersi Türkçeye çevrildi.
      </li>
      <li style="margin-bottom:10px;">
        <b style="color:#7EE0FF;">Otomatik tekrar kaydı</b> — Bir kelime
        üzerinde bir dakikadan fazla zaman geçirdiğinizde, o kelime otomatik
        olarak SRS tekrar listenize eklenir.
      </li>
      <li style="margin-bottom:0;">
        <b style="color:#7EE0FF;">Dil seçici ve bayraklar</b> — Dil değiştirme
        menüsünde artık her dil için yuvarlak bayrak simgeleri bulunuyor.
      </li>
    </ul>

    <p style="font-size:14.5px;line-height:1.7;color:#D9E6F2;margin:24px 0 20px;">
      Platformu kullanmaya devam edin; Çince öğrenme yolculuğunuzda
      başarılar dileriz.
    </p>

    <div style="text-align:center;margin:28px 0 8px;">
      <a href="{url}" style="display:inline-block;padding:13px 32px;background:#4a9eff;color:#fff;text-decoration:none;border-radius:10px;font-weight:600;font-size:15px;">
        Uygulamaya Git
      </a>
    </div>

  </div>

  <div style="text-align:center;margin-top:24px;font-size:13px;color:#8B9AAB;line-height:1.6;">
    Saygılarımızla,<br>
    <b style="color:#E6EDF5;font-size:14px;">AZIZOV MUHAMMETJAN</b><br>
    <span style="font-size:12px;">HSK 5 Learner Geliştirici Ekibi</span>
  </div>

  <div style="text-align:center;margin-top:20px;font-size:11px;color:#4a5568;">
    Bu e-posta HSK 5 Learner'a kaydolduğunuz için gönderilmiştir.<br>
    <a href="{url}" style="color:#66B2FF;text-decoration:none;">alelatdin.pythonanywhere.com</a>
  </div>

</div>
</body></html>""",
}


# ============================================================
# ПИСЬМО 2 — благодарность + активация (Gowher)
# ============================================================
EMAIL_GOWHER = {
    "subject": "HSK 5 Learner — Hesabınız Aktifleştirildi",
    "html": """<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#0e1620;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#F0F4F8;">
<div style="max-width:600px;margin:0 auto;padding:32px 24px;">

  <div style="text-align:center;margin-bottom:28px;">
    <div style="font-size:28px;font-weight:800;letter-spacing:0.5px;color:#66B2FF;">中文 · HSK 5 Learner</div>
    <div style="font-size:13px;color:#8B9AAB;margin-top:4px;">Çince öğrenme platformunuz</div>
  </div>

  <div style="background:linear-gradient(160deg,#1b2333 0%,#141a26 100%);border:1px solid #2a3446;border-radius:16px;padding:28px 26px;">

    <div style="text-align:center;font-size:44px;margin-bottom:12px;">🎉</div>

    <h1 style="font-size:20px;margin:0 0 16px;color:#E6EDF5;text-align:center;">
      Sayın {name},
    </h1>

    <p style="font-size:15px;line-height:1.65;color:#D9E6F2;margin:0 0 18px;">
      HSK 5 Learner'a kaydolduğunuz için içtenlikle teşekkür ederiz.
      Platformumuzu tercih etmeniz bizim için büyük bir memnuniyet kaynağıdır.
    </p>

    <div style="background:rgba(92,214,142,0.10);border:1px solid rgba(92,214,142,0.4);border-radius:12px;padding:16px 18px;margin:20px 0;">
      <div style="font-size:13px;font-weight:700;color:#5CD68E;letter-spacing:0.5px;text-transform:uppercase;margin-bottom:6px;">
        ✓ Hesabınız Aktifleştirildi
      </div>
      <div style="font-size:14.5px;line-height:1.6;color:#D9E6F2;">
        E-posta doğrulama adımını tamamlamadan doğrudan sisteme giriş
        yapabilirsiniz. Kayıt sırasında belirlediğiniz e-posta adresi ve
        şifre ile giriş yapmanız yeterlidir.
      </div>
    </div>

    <div style="font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#66B2FF;margin:24px 0 12px;font-weight:700;">
      Sizi Neler Bekliyor
    </div>

    <ul style="font-size:14.5px;line-height:1.7;color:#D9E6F2;margin:0;padding-left:22px;">
      <li style="margin-bottom:8px;">
        <b style="color:#7EE0FF;">HSK 5 dersleri</b> — 18 ders, 727 kelime,
        dil bilgisi, karşılaştırmalar ve alıştırmalar.
      </li>
      <li style="margin-bottom:8px;">
        <b style="color:#7EE0FF;">HSK 6 modülü</b> — 2.460 kelime, yapay zekâ
        destekli derinlemesine açıklamalar ve üç örnek cümle.
      </li>
      <li style="margin-bottom:8px;">
        <b style="color:#7EE0FF;">İş Çincesi kursu</b> — 5 modül, 15 ders,
        gerçek iş hayatına yönelik içerikler.
      </li>
      <li style="margin-bottom:8px;">
        <b style="color:#7EE0FF;">SRS tekrar sistemi</b> — Anki tarzı aralıklı
        tekrar yöntemiyle kelimeleri kalıcı olarak öğrenin.
      </li>
      <li style="margin-bottom:0;">
        <b style="color:#7EE0FF;">7 dil desteği</b> — Türkçe, Rusça, İngilizce,
        Türkmence, Özbekçe, Tacikçe ve Endonezce.
      </li>
    </ul>

    <p style="font-size:14.5px;line-height:1.7;color:#D9E6F2;margin:24px 0 8px;">
      Herhangi bir sorunuz, öneriniz veya geri bildiriminiz olursa, uygulama
      içindeki <b style="color:#7EE0FF;">"Geri Bildirim"</b> bölümünden bize
      ulaşabilirsiniz. Görüşleriniz bizim için çok değerlidir.
    </p>

    <div style="text-align:center;margin:28px 0 8px;">
      <a href="{url}" style="display:inline-block;padding:13px 32px;background:#4a9eff;color:#fff;text-decoration:none;border-radius:10px;font-weight:600;font-size:15px;">
        Giriş Yap
      </a>
    </div>

  </div>

  <div style="text-align:center;margin-top:24px;font-size:13px;color:#8B9AAB;line-height:1.6;">
    İyi öğrenmeler dileriz.<br><br>
    Saygılarımızla,<br>
    <b style="color:#E6EDF5;font-size:14px;">AZIZOV MUHAMMETJAN</b><br>
    <span style="font-size:12px;">HSK 5 Learner Geliştirici Ekibi</span>
  </div>

  <div style="text-align:center;margin-top:20px;font-size:11px;color:#4a5568;">
    Bu e-posta HSK 5 Learner'a kaydolduğunuz için gönderilmiştir.<br>
    <a href="{url}" style="color:#66B2FF;text-decoration:none;">alelatdin.pythonanywhere.com</a>
  </div>

</div>
</body></html>""",
}


def send_brevo(subject, html, to_email, to_name):
    if not BREVO_KEY:
        return False, "BREVO_KEY не задан"
    try:
        payload = {
            "sender": {"email": FROM_EMAIL, "name": FROM_NAME},
            "to": [{"email": to_email, "name": to_name}],
            "subject": subject,
            "htmlContent": html,
        }
        r = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "accept": "application/json",
                "api-key": BREVO_KEY,
                "content-type": "application/json",
            },
            json=payload,
            timeout=20,
        )
        if r.status_code in (200, 201, 202):
            return True, "OK"
        return False, f"HTTP {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    if not BREVO_KEY:
        print("!! Установи BREVO_KEY в этом окне и повтори:")
        print("   export BREVO_KEY=xkeysib-...")
        sys.exit(1)

    print("=" * 60)
    print("АКТИВАЦИЯ + ТУРЕЦКИЕ ПИСЬМА")
    print("=" * 60)

    # 1) Активируем Gowher
    db = sqlite3.connect(DB)
    db.execute(
        "UPDATE users SET activated=1, activate_token=NULL, activate_expires=NULL "
        "WHERE id=8"
    )
    db.commit()
    print("[1/3] Gowher активирована в БД")

    # 2) Читаем юзеров
    users = db.execute(
        "SELECT id, name, email, is_admin, activated FROM users ORDER BY id"
    ).fetchall()
    db.close()

    # 3) Отправляем письма
    print("\n[2/3] Отправка писем...")

    for uid, name, email, is_admin, activated in users:
        if is_admin:
            print(f"  skip {email} (admin — сам себе не пишем)")
            continue

        if uid == 8:
            # Gowher — персональное письмо
            html = EMAIL_GOWHER["html"].replace("{name}", name).replace("{url}", PUBLIC_URL)
            ok, msg = send_brevo(EMAIL_GOWHER["subject"], html, email, name)
            print(f"  [Gowher] {email} → {'✅ OK' if ok else '❌ ' + msg}")
        else:
            # Wepa — общее письмо про обновления
            html = EMAIL_UPDATES["html"].replace("{name}", name).replace("{url}", PUBLIC_URL)
            ok, msg = send_brevo(EMAIL_UPDATES["subject"], html, email, name)
            print(f"  [Updates] {email} → {'✅ OK' if ok else '❌ ' + msg}")

    print("\n[3/3] ГОТОВО.")
    print("\nОтправлено 2 письма на турецком языке.")


if __name__ == "__main__":
    main()