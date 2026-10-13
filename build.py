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
# Data controller named in policies of apps that process personal data.
CONTROLLER = "Fatih Barış Şahan"
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
    {
        "slug": "ehliyet",
        "name": {"tr": "Online Ehliyet Dersleri", "en": "Online Ehliyet Dersleri"},
        "tagline": {
            "tr": "Ehliyet sınavına hazırlık: konu anlatımı, soru bankası ve deneme sınavları.",
            "en": "Prepare for the Turkish driving-licence theory exam: lessons, question bank and mock exams.",
        },
        "updated": {"tr": "13 Ekim 2026", "en": "13 October 2026"},
        "privacy": "ehliyet_privacy",
        # (file stem, title per language, body function, languages)
        "pages": [
            ("kvkk", {"tr": "KVKK Aydınlatma Metni"}, "ehliyet_kvkk", ("tr",)),
            ("delete-account", {"tr": "Hesap Silme", "en": "Delete Account"}, "ehliyet_delete", ("tr", "en")),
        ],
        "faq": {
            "tr": [
                ("Hesap açmak zorunda mıyım?",
                 "Hayır. Misafir olarak çalışabilirsin; ilerlemen bu cihazda saklanır. Hesap açarsan ilerlemen hesabına bağlanır."),
                ("İnternet gerekiyor mu?",
                 "Konu anlatımları, alıştırmalar ve deneme sınavı internetsiz çalışır. Giriş yapmak ve ilerlemeyi yedeklemek için internet gerekir."),
                ("Bir soruda hata buldum.",
                 "Soru numarasını ve hatayı e-postayla bildir; inceleyip düzeltiriz."),
                ("Hesabımı nasıl silerim?",
                 "Profil → Hesap → Hesabımı ve verilerimi sil. Ayrıntılar hesap silme sayfasında."),
                ("Sorular gerçek sınavdakiyle aynı mı?",
                 "Hayır. Sorular MEB müfredatına göre özgün olarak hazırlanır; deneme sınavı gerçek e-Sınav'ın soru sayısı, süresi ve ders dağılımını taklit eder. Uygulama MEB ile bağlantılı değildir."),
            ],
            "en": [
                ("Do I need an account?",
                 "No. You can study as a guest; your progress stays on this device. With an account your progress is linked to it."),
                ("Do I need an internet connection?",
                 "Lessons, practice and mock exams work offline. Signing in and backing up progress need a connection."),
                ("I found a mistake in a question.",
                 "Email us the question and the problem; we will review and fix it."),
                ("How do I delete my account?",
                 "Profil → Hesap → Hesabımı ve verilerimi sil. Details are on the account deletion page."),
                ("Are these the real exam questions?",
                 "No. Questions are written originally to the official curriculum; the mock exam mirrors the real e-exam's length, time and subject mix. The app is not affiliated with the Ministry of Education."),
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


def ehliyet_privacy(app, lang):
    n = html.escape(app["name"][lang])
    e = html.escape(CONTACT_EMAIL)
    if lang == "tr":
        return f"""
<p>Bu politika, {CONTROLLER} ({BRAND}) tarafından geliştirilen <strong>{n}</strong> uygulaması için geçerlidir. Kişisel verilerin 6698 sayılı Kanun (KVKK) kapsamında nasıl işlendiği <a href="kvkk.html">KVKK Aydınlatma Metni</a>'nde ayrıca açıklanır.</p>
<h2>Kısaca</h2>
<p>Uygulamayı hesap açmadan, misafir olarak kullanabilirsin. Hesap açarsan ilerlemen hesabına bağlanır. Verilerini satmayız, reklam için kullanmayız ve seni başka uygulamalarda ya da sitelerde takip etmeyiz. Uygulamada reklam yoktur.</p>
<h2>Topladığımız veriler</h2>
<div class="card"><h3>Hesap bilgileri</h3><p class="dim">Hesap açarsan: e-posta adresin ve giriş yöntemin (e-posta/şifre, Google ya da Apple). Google veya Apple ile girişte bu sağlayıcıların paylaştığı ad ve e-posta bilgisi. Şifren bize ulaşmaz; kimlik doğrulamayı Google Firebase Authentication yapar. Misafir kullanımda yalnızca rastgele üretilmiş bir kullanıcı kimliği oluşur.</p></div>
<div class="card"><h3>Çalışma verileri</h3><p class="dim">Çözdüğün alıştırma ve deneme sınavları: hangi soruya ne cevap verdiğin, doğru/yanlış sonucu, süre ve tarih. Bu veriler ilerlemeni, zayıf konularını ve tekrar zamanlarını hesaplamak için kullanılır; hesabın varsa sunucuya da yedeklenir.</p></div>
<div class="card"><h3>Cihazda kalan bilgiler</h3><p class="dim">Planladığın sınav tarihi, günlük hedefin, hatırlatma saatin ve tema tercihin yalnızca cihazında saklanır.</p></div>
<div class="card"><h3>Bildirim kimliği</h3><p class="dim">Bildirimlere izin verirsen cihazına bildirim gönderebilmek için bir bildirim anahtarı (Firebase Cloud Messaging token) saklanır. İzni cihaz ayarlarından istediğin zaman kapatabilirsin.</p></div>
<div class="card"><h3>Kullanım ve hata verileri</h3><p class="dim">Uygulamanın nasıl kullanıldığına dair anonim istatistikler (Firebase Analytics) ve uygulama çöktüğünde oluşan hata kayıtları (Firebase Crashlytics): cihaz modeli, işletim sistemi sürümü, uygulama sürümü, hata ayrıntısı. Adın ya da e-posta adresin bu kayıtlara eklenmez.</p></div>
<p>Uygulama konumuna, rehberine, fotoğraflarına, kamerana ya da mikrofonuna erişmez.</p>
<h2>Verileri ne için kullanıyoruz</h2>
<p>Hesabını oluşturmak ve korumak, ilerlemeni cihazlar arasında saklamak, sana uygun soru ve tekrarları seçmek, izin verdiysen çalışma hatırlatması göndermek, hataları bulup uygulamayı iyileştirmek.</p>
<h2>Verilerin nerede saklanır, kimlerle paylaşılır</h2>
<p>Veriler Google Firebase altyapısında saklanır (Google Ireland Limited / Google LLC). Çalışma verilerinin tutulduğu veritabanı Avrupa Birliği'ndeki (Frankfurt) sunucularda bulunur; kimlik doğrulama, analiz ve hata kayıtları Google'ın yurt dışındaki sunucularında işlenebilir. Google ya da Apple ile giriş yaparsan kimlik doğrulama için ilgili sağlayıcıyla iletişim kurulur. Bunların dışında verilerin üçüncü kişilerle paylaşılmaz; yalnızca yasal bir zorunluluk olduğunda yetkili makamlara verilebilir.</p>
<h2>Saklama süresi ve silme</h2>
<p>Verilerin hesabın var olduğu sürece saklanır. Hesabını ve tüm verilerini uygulama içinden <strong>Profil → Hesap → Hesabımı ve verilerimi sil</strong> adımlarıyla kalıcı olarak silebilirsin. Uygulamaya erişemiyorsan <a href="delete-account.html">hesap silme sayfasındaki</a> adımları izle. Hata kayıtları Google tarafından en fazla 90 gün tutulur.</p>
<h2>Hakların</h2>
<p>Verilerine erişme, düzeltilmesini ya da silinmesini isteme ve işlenmesine itiraz etme hakkın vardır. Ayrıntılar <a href="kvkk.html">KVKK Aydınlatma Metni</a>'ndedir. Taleplerin için: <a href="mailto:{e}">{e}</a></p>
<h2>Çocuklar</h2>
<p>Uygulama sürücü belgesi sınavına hazırlanan adaylar içindir ve 13 yaşından küçük çocuklara yönelik değildir. Uygulamada kullanıcılar arası mesajlaşma yoktur.</p>
<h2>Güvenlik</h2>
<p>Veriler cihaz ile sunucu arasında şifreli bağlantıyla (TLS) taşınır. Sunucudaki verilerine yalnızca kendi hesabınla erişilebilir.</p>
<h2>Değişiklikler</h2>
<p>Bu politika değişirse güncel hali bu sayfada yayımlanır ve yukarıdaki tarih güncellenir.</p>
<h2>İletişim</h2>
<p>{CONTROLLER} · <a href="mailto:{e}">{e}</a></p>
"""
    return f"""
<p>This policy applies to the <strong>{n}</strong> app developed by {CONTROLLER} ({BRAND}).</p>
<h2>In short</h2>
<p>You can use the app as a guest, without an account. If you create an account, your progress is linked to it. We do not sell your data, use it for advertising, or track you across other apps and websites. The app contains no ads.</p>
<h2>Data we collect</h2>
<div class="card"><h3>Account details</h3><p class="dim">If you create an account: your email address and sign-in method (email/password, Google or Apple). With Google or Apple sign-in, the name and email those providers share. We never receive your password; authentication is handled by Google Firebase Authentication. Guest use only creates a randomly generated user ID.</p></div>
<div class="card"><h3>Study data</h3><p class="dim">The practice sessions and mock exams you complete: which answer you gave to which question, whether it was correct, time taken and date. This is used to calculate your progress, weak topics and review schedule; if you have an account it is also backed up to the server.</p></div>
<div class="card"><h3>Information kept on your device</h3><p class="dim">Your planned exam date, daily goal, reminder time and theme preference are stored on your device only.</p></div>
<div class="card"><h3>Notification identifier</h3><p class="dim">If you allow notifications, a push token (Firebase Cloud Messaging) is stored so that reminders can be delivered to your device. You can turn this off at any time in your device settings.</p></div>
<div class="card"><h3>Usage and crash data</h3><p class="dim">Anonymous statistics on how the app is used (Firebase Analytics) and crash reports (Firebase Crashlytics): device model, OS version, app version and error details. Your name or email is not added to these records.</p></div>
<p>The app does not access your location, contacts, photos, camera or microphone.</p>
<h2>How we use the data</h2>
<p>To create and protect your account, keep your progress across devices, choose suitable questions and reviews, send study reminders if you allowed them, and find bugs and improve the app.</p>
<h2>Where data is stored and who it is shared with</h2>
<p>Data is stored on Google Firebase (Google Ireland Limited / Google LLC). The database holding study data is located in the European Union (Frankfurt); authentication, analytics and crash data may be processed on Google servers in other countries. If you sign in with Google or Apple, the app communicates with that provider to authenticate you. Otherwise your data is not shared with third parties, except where the law requires disclosure to authorities.</p>
<h2>Retention and deletion</h2>
<p>Your data is kept for as long as your account exists. You can permanently delete your account and all your data in the app under <strong>Profil → Hesap → Hesabımı ve verilerimi sil</strong>. If you cannot access the app, follow the steps on the <a href="delete-account-en.html">account deletion page</a>. Crash reports are kept by Google for up to 90 days.</p>
<h2>Your rights</h2>
<p>You may ask to access, correct or delete your data, or object to its processing: <a href="mailto:{e}">{e}</a></p>
<h2>Children</h2>
<p>The app is intended for driving-licence candidates and is not directed at children under 13. It has no user-to-user messaging.</p>
<h2>Security</h2>
<p>Data travels between your device and the server over an encrypted connection (TLS). Data on the server can only be accessed with your own account.</p>
<h2>Changes</h2>
<p>If this policy changes, the current version will be published on this page and the date above updated.</p>
<h2>Contact</h2>
<p>{CONTROLLER} · <a href="mailto:{e}">{e}</a></p>
"""


def ehliyet_kvkk(app, lang):
    n = html.escape(app["name"]["tr"])
    e = html.escape(CONTACT_EMAIL)
    return f"""
<p>Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu'nun ("KVKK") 10. maddesi uyarınca, <strong>{n}</strong> uygulamasını kullananları bilgilendirmek için hazırlanmıştır.</p>
<h2>1. Veri sorumlusu</h2>
<p>{CONTROLLER} ("{BRAND}"). İletişim: <a href="mailto:{e}">{e}</a></p>
<h2>2. İşlenen kişisel veriler</h2>
<p><strong>Kimlik ve iletişim:</strong> e-posta adresi; Google ya da Apple ile girişte sağlayıcının paylaştığı ad ve e-posta.<br>
<strong>Kullanıcı işlem verileri:</strong> kullanıcı kimliği, çözülen sorular ve verilen cevaplar, sınav sonuçları, süre ve tarih bilgileri.<br>
<strong>Cihaz ve kullanım verileri:</strong> bildirim anahtarı, cihaz modeli, işletim sistemi ve uygulama sürümü, anonim kullanım istatistikleri, hata kayıtları.</p>
<p>Özel nitelikli kişisel veri işlenmez.</p>
<h2>3. İşleme amaçları</h2>
<p>Üyelik hesabının oluşturulması ve yönetilmesi; eğitim hizmetinin sunulması ve ilerlemenin saklanması; kişiye uygun soru ve tekrar önerilerinin hazırlanması; izin verilmişse çalışma hatırlatmalarının gönderilmesi; hataların giderilmesi, güvenliğin sağlanması ve hizmetin geliştirilmesi; yasal yükümlülüklerin yerine getirilmesi.</p>
<h2>4. Hukuki sebepler</h2>
<p>Hesap ve çalışma verileri, KVKK md. 5/2-c uyarınca sözleşmenin kurulması ve ifası için; hata ve güvenlik kayıtları md. 5/2-f uyarınca veri sorumlusunun meşru menfaati için; yasal bildirimler md. 5/2-ç uyarınca hukuki yükümlülük için işlenir. Bildirim gönderimi ve kullanım istatistikleri açık rızana (md. 5/1) dayanır; rızanı cihaz ayarlarından dilediğin zaman geri alabilirsin.</p>
<h2>5. Toplama yöntemi</h2>
<p>Veriler, uygulamayı kullanman sırasında elektronik ortamda, doğrudan senden ve cihazından otomatik yollarla toplanır.</p>
<h2>6. Aktarım</h2>
<p>Veriler, barındırma, kimlik doğrulama, bildirim, analiz ve hata izleme hizmetlerini sağlayan Google'a (Google Ireland Limited / Google LLC, Firebase) aktarılır. Çalışma verilerinin veritabanı Almanya'da (Frankfurt) bulunur; diğer hizmetlerde veriler yurt dışındaki sunucularda işlenebilir. Yurt dışına aktarım KVKK md. 9 kapsamında yapılır. Apple ya da Google ile girişte kimlik doğrulama için ilgili sağlayıcıyla veri alışverişi olur. Veriler satılmaz, reklam amacıyla paylaşılmaz; yalnızca yasal zorunluluk hâlinde yetkili kurumlara aktarılabilir.</p>
<h2>7. Saklama süresi</h2>
<p>Veriler hesabın var olduğu sürece saklanır; hesabını sildiğinde silinir. Hata kayıtları en fazla 90 gün tutulur. Yasal saklama yükümlülükleri saklıdır.</p>
<h2>8. KVKK md. 11 kapsamındaki hakların</h2>
<p>Kişisel verilerinin işlenip işlenmediğini öğrenme; işlenmişse bilgi talep etme; işlenme amacını ve amacına uygun kullanılıp kullanılmadığını öğrenme; yurt içinde ya da yurt dışında aktarıldığı üçüncü kişileri bilme; eksik ya da yanlış işlenmişse düzeltilmesini isteme; silinmesini ya da yok edilmesini isteme; bu işlemlerin aktarıldığı üçüncü kişilere bildirilmesini isteme; otomatik sistemlerle analiz sonucu aleyhine bir sonuç çıkmasına itiraz etme; kanuna aykırı işleme nedeniyle zarara uğraman hâlinde zararın giderilmesini talep etme.</p>
<h2>9. Başvuru</h2>
<p>Taleplerini <a href="mailto:{e}">{e}</a> adresine, hesabında kayıtlı e-posta adresinden gönderebilirsin. Başvurular en geç 30 gün içinde ücretsiz olarak yanıtlanır. Hesabını ve verilerini beklemeden silmek için: <a href="delete-account.html">hesap silme</a>.</p>
"""


def ehliyet_delete(app, lang):
    n = html.escape(app["name"][lang])
    e = html.escape(CONTACT_EMAIL)
    if lang == "tr":
        return f"""
<p><strong>{n}</strong> hesabını ve hesabına bağlı tüm verileri iki yoldan silebilirsin.</p>
<h2>Uygulama içinden (anında)</h2>
<div class="card"><p>1. Uygulamayı aç ve <strong>Profil</strong> sekmesine git.<br>2. <strong>Hesap</strong>'a dokun.<br>3. <strong>Hesabımı ve verilerimi sil</strong>'e dokun ve onayla.</p></div>
<h2>E-posta ile</h2>
<p>Uygulamaya erişemiyorsan hesabında kayıtlı e-posta adresinden <a href="mailto:{e}?subject=Hesap%20silme%20talebi">{e}</a> adresine "Hesap silme talebi" konulu bir e-posta gönder. Talebin en geç 30 gün içinde yerine getirilir.</p>
<h2>Neler silinir</h2>
<p>Hesabın (e-posta adresi ve giriş bilgileri), çözdüğün alıştırma ve deneme sınavı kayıtları, ilerleme ve rozetlerin, bildirim anahtarın. Silme işlemi geri alınamaz.</p>
<h2>Neler bir süre daha tutulur</h2>
<p>Kimliğinle ilişkilendirilmemiş hata kayıtları Google Firebase tarafından en fazla 90 gün saklanır ve ardından kendiliğinden silinir.</p>
"""
    return f"""
<p>You can delete your <strong>{n}</strong> account and all data linked to it in two ways.</p>
<h2>In the app (immediate)</h2>
<div class="card"><p>1. Open the app and go to the <strong>Profil</strong> tab.<br>2. Tap <strong>Hesap</strong>.<br>3. Tap <strong>Hesabımı ve verilerimi sil</strong> and confirm.</p></div>
<h2>By email</h2>
<p>If you cannot access the app, send an email with the subject "Account deletion request" to <a href="mailto:{e}?subject=Account%20deletion%20request">{e}</a> from the address registered on your account. Requests are completed within 30 days.</p>
<h2>What is deleted</h2>
<p>Your account (email address and sign-in details), your practice and mock-exam records, your progress and badges, and your push token. Deletion cannot be undone.</p>
<h2>What is kept for a while</h2>
<p>Crash reports that are not linked to your identity are kept by Google Firebase for up to 90 days and then deleted automatically.</p>
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
                + "".join(
                    f'<p><a href="{stem}{sfx}.html">{html.escape(titles[lang])}</a></p>'
                    for stem, titles, _, langs in a.get("pages", []) if lang in langs
                )
            )
            write(f'{a["slug"]}/{support_file}',
                  page(lang, f'{a["name"][lang]} · {t["support"]}', body,
                       "en.html" if lang == "tr" else "./", "icon.png"))

            updated = a.get("updated", UPDATED)[lang]
            body_fn = globals()[a["privacy"]] if "privacy" in a else privacy_body
            pbody = f'<p class="dim">{t["updated"]}: {updated}</p>' + body_fn(a, lang)
            write(f'{a["slug"]}/privacy{sfx}.html',
                  page(lang, f'{a["name"][lang]} · {t["privacy"]}', pbody,
                       "privacy-en.html" if lang == "tr" else "privacy.html", "icon.png"))

            for stem, titles, fn, langs in a.get("pages", []):
                if lang not in langs:
                    continue
                other = "tr" if lang == "en" else "en"
                alt = (f'{stem}{"-en" if other == "en" else ""}.html' if other in langs
                       else ("en.html" if lang == "tr" else "./"))
                xbody = f'<p class="dim">{t["updated"]}: {updated}</p>' + globals()[fn](a, lang)
                write(f'{a["slug"]}/{stem}{sfx}.html',
                      page(lang, f'{a["name"][lang]} · {titles[lang]}', xbody, alt, "icon.png"))


if __name__ == "__main__":
    main()
