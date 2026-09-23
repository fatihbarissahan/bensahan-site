#!/usr/bin/env python3
"""
Builds the bensahan support site: one support page and one privacy policy per
app, each in Turkish and English. The App Store listing links to these pages
(Support URL, Privacy Policy URL), so every published app needs an entry here.

    python3 build.py          # rewrites the HTML next to this file

Adding an app: append to APPS, put its 192px icon at <slug>/icon.png, rebuild.
"""
import html
import os

# Shown on every page as the way to reach the developer. Apple requires a
# working contact on the support page.
CONTACT_EMAIL = "info@bensahan.com"
BRAND = "bensahan"
UPDATED = {"tr": "23 Eylül 2026", "en": "23 September 2026"}

APPS = [
    {
        "slug": "tavla",
        "name": {"tr": "Tavla 3D", "en": "Tavla 3D"},
        "tagline": {
            "tr": "Bilgisayara karşı, tam kurallı klasik tavla.",
            "en": "Classic backgammon against the computer, with the full rules.",
        },
        "faq": {
            "tr": [
                ("İlerlemem nerede saklanıyor?",
                 "Seviyen, rütbelerin ve ödüllerin yalnızca bu cihazda saklanır. Uygulamayı silersen ilerleme de silinir."),
                ("Dili nasıl değiştiririm?", "Ana menü → Ayarlar → Dil."),
                ("Tahta çok küçük görünüyor.", "Telefonu yan çevir; tahta ekranın uzun kenarını kullanır."),
                ("İnternet gerekiyor mu?", "Hayır. Oyun tamamen çevrimdışı çalışır."),
            ],
            "en": [
                ("Where is my progress stored?",
                 "Your level, ranks and rewards are stored on this device only. Deleting the app deletes them too."),
                ("How do I change the language?", "Main menu → Settings → Language."),
                ("The board looks small.", "Turn the phone sideways; the board then uses the long side of the screen."),
                ("Do I need an internet connection?", "No. The game works completely offline."),
            ],
        },
    },
    {
        "slug": "bilardo",
        "name": {"tr": "Bilardo 3D", "en": "Bilardo 3D"},
        "tagline": {
            "tr": "Gerçek fizikli 8-Top ve 9-Top, 30 bölümlük kariyer.",
            "en": "8-Ball and 9-Ball with real physics, and a 30-level career.",
        },
        "faq": {
            "tr": [
                ("İlerlemem nerede saklanıyor?",
                 "Seviyen, yıldızların ve ödüllerin yalnızca bu cihazda saklanır. Uygulamayı silersen ilerleme de silinir."),
                ("Nişan çizgisini nasıl kapatırım?", "Ana menü → Ayarlar → Nişan çizgisi."),
                ("Oyun telefonumda yavaş çalışıyor.", "Ana menü → Ayarlar → Görüntü kalitesi → Performans."),
                ("İnternet gerekiyor mu?", "Hayır. Oyun tamamen çevrimdışı çalışır."),
            ],
            "en": [
                ("Where is my progress stored?",
                 "Your level, stars and rewards are stored on this device only. Deleting the app deletes them too."),
                ("How do I turn off the aiming line?", "Main menu → Settings → Aiming line."),
                ("The game runs slowly on my phone.", "Main menu → Settings → Graphics → Performance."),
                ("Do I need an internet connection?", "No. The game works completely offline."),
            ],
        },
    },
]

T = {
    "tr": {
        "lang": "tr", "support": "Destek", "privacy": "Gizlilik Politikası",
        "contact": "İletişim",
        "contact_body": "Soru, hata bildirimi ya da önerin için e-posta gönder; genellikle birkaç gün içinde yanıt veriyoruz.",
        "faq": "Sık sorulanlar", "other": "English", "updated": "Son güncelleme",
        "apps": "Uygulamalar",
        "home_intro": "Bağımsız geliştirici bensahan'ın oyunları ve uygulamaları.",
    },
    "en": {
        "lang": "en", "support": "Support", "privacy": "Privacy Policy",
        "contact": "Contact",
        "contact_body": "Email us with questions, bug reports or ideas; we usually reply within a few days.",
        "faq": "FAQ", "other": "Türkçe", "updated": "Last updated",
        "apps": "Apps",
        "home_intro": "Games and apps by independent developer bensahan.",
    },
}


def privacy_body(app, lang):
    n = html.escape(app["name"][lang])
    e = html.escape(CONTACT_EMAIL)
    if lang == "tr":
        return f"""
<p>Bu politika, {BRAND} tarafından geliştirilen <strong>{n}</strong> uygulaması için geçerlidir.</p>
<h2>Kısaca</h2>
<p><strong>{n} hiçbir kişisel veri toplamaz, saklamaz ya da paylaşmaz.</strong></p>
<h2>Toplanan veriler</h2>
<p>Yok. Uygulama hesap istemez, internete bağlanmaz ve herhangi bir sunucuya veri göndermez. Uygulamada reklam, analiz (analytics) ya da takip aracı bulunmaz.</p>
<h2>Cihazda saklanan bilgiler</h2>
<p>Oyun ayarların (dil, ses, titreşim) ve oyun ilerlemen (seviye, ödüller, haftalık hedefler) yalnızca kendi cihazında saklanır. Bu bilgiler cihazdan çıkmaz ve bize ulaşmaz. Uygulamayı sildiğinde bu bilgiler de silinir.</p>
<h2>Çocuklar</h2>
<p>Uygulama hiçbir kullanıcıdan, çocuklar da dahil, veri toplamadığı için her yaştan kullanıcı için güvenlidir.</p>
<h2>Değişiklikler</h2>
<p>Bu politika değişirse güncel hali bu sayfada yayımlanır ve yukarıdaki tarih güncellenir.</p>
<h2>İletişim</h2>
<p>Sorularınız için: <a href="mailto:{e}">{e}</a></p>
"""
    return f"""
<p>This policy applies to the <strong>{n}</strong> app developed by {BRAND}.</p>
<h2>In short</h2>
<p><strong>{n} does not collect, store or share any personal data.</strong></p>
<h2>Data collected</h2>
<p>None. The app does not ask for an account, does not connect to the internet and does not send data to any server. It contains no advertising, analytics or tracking tools.</p>
<h2>Information kept on your device</h2>
<p>Your game settings (language, sound, vibration) and your progress (level, rewards, weekly goals) are stored only on your own device. They never leave the device and never reach us. Deleting the app deletes them.</p>
<h2>Children</h2>
<p>Because the app collects no data from anyone, including children, it is safe for users of all ages.</p>
<h2>Changes</h2>
<p>If this policy changes, the current version will be published on this page and the date above updated.</p>
<h2>Contact</h2>
<p>Questions: <a href="mailto:{e}">{e}</a></p>
"""


CSS = """
:root{--bg:#f7f5f0;--fg:#1d1b18;--dim:#6b665d;--card:#fff;--line:#e4dfd5;--accent:#8a5a14}
@media (prefers-color-scheme:dark){:root{--bg:#121110;--fg:#ece8e1;--dim:#a39d92;--card:#1c1a18;--line:#2f2c28;--accent:#e2b35f}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
main{max-width:680px;margin:0 auto;padding:32px 16px 64px}
header{display:flex;align-items:center;gap:14px;margin-bottom:24px}
header img{width:64px;height:64px;border-radius:14px}
h1{font-size:1.6rem;margin:0}
h2{font-size:1.1rem;margin:28px 0 6px}
p{margin:0 0 12px}
.dim{color:var(--dim)}
a{color:var(--accent)}
nav{display:flex;gap:16px;flex-wrap:wrap;margin:0 0 24px;font-size:.95rem}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin:0 0 12px}
.card h3{margin:0 0 4px;font-size:1rem}
.apps a{display:flex;gap:14px;align-items:center;text-decoration:none;color:inherit}
.apps img{width:52px;height:52px;border-radius:12px}
footer{margin-top:40px;font-size:.85rem;color:var(--dim)}
"""


def page(lang, title, body, alt_href, icon=None):
    t = T[lang]
    head_img = f'<img src="{icon}" alt="">' if icon else ""
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
<main>
<header>{head_img}<h1>{html.escape(title)}</h1></header>
<nav><a href="{alt_href}">{t['other']}</a></nav>
{body}
<footer>© 2026 {BRAND}</footer>
</main>
</body>
</html>
"""


def write(path, text):
    full = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    for lang in ("tr", "en"):
        t = T[lang]
        cards = "".join(
            f'<div class="card apps"><a href="{a["slug"]}/{"" if lang == "tr" else "en.html"}">'
            f'<img src="{a["slug"]}/icon.png" alt=""><div><h3>{html.escape(a["name"][lang])}</h3>'
            f'<p class="dim">{html.escape(a["tagline"][lang])}</p></div></a></div>'
            for a in APPS
        )
        body = f'<p class="dim">{t["home_intro"]}</p><h2>{t["apps"]}</h2>{cards}'
        write("index.html" if lang == "tr" else "en.html",
              page(lang, BRAND, body, "en.html" if lang == "tr" else "./"))

    for a in APPS:
        for lang in ("tr", "en"):
            t = T[lang]
            sfx = "" if lang == "tr" else "-en"
            support_file = "index.html" if lang == "tr" else "en.html"
            faq = "".join(
                f'<div class="card"><h3>{html.escape(q)}</h3><p class="dim">{html.escape(r)}</p></div>'
                for q, r in a["faq"][lang]
            )
            e = html.escape(CONTACT_EMAIL)
            body = (
                f'<p class="dim">{html.escape(a["tagline"][lang])}</p>'
                f'<h2>{t["contact"]}</h2><p>{t["contact_body"]}</p>'
                f'<p><a href="mailto:{e}">{e}</a></p>'
                f'<h2>{t["faq"]}</h2>{faq}'
                f'<p><a href="privacy{sfx}.html">{t["privacy"]}</a></p>'
            )
            write(f'{a["slug"]}/{support_file}',
                  page(lang, f'{a["name"][lang]} · {t["support"]}', body,
                       "en.html" if lang == "tr" else "./", "icon.png"))

            pbody = f'<p class="dim">{t["updated"]}: {UPDATED[lang]}</p>' + privacy_body(a, lang)
            write(f'{a["slug"]}/privacy{sfx}.html',
                  page(lang, f'{a["name"][lang]} · {t["privacy"]}', pbody,
                       "privacy-en.html" if lang == "tr" else "privacy.html", "icon.png"))


if __name__ == "__main__":
    main()
