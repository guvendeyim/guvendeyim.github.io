"""Tanıtım sitesinin sayfalarını üretir: python3 build.py

Üst menü ve alt bilgi tek yerde durur; sayfa içerikleri aşağıdaki PAGES sözlüğündedir.
Üretilen *.html dosyaları elle düzenlenmez.
"""
import hashlib

# Tarayıcı eski biçim dosyasını önbellekten kullanmasın diye bağlantıya dosyanın özeti eklenir;
# css/site.css değişince sürüm kendiliğinden değişir.
with open("css/site.css", "rb") as _css:
    CSS_VERSION = hashlib.sha256(_css.read()).hexdigest()[:8]

MENU = [
    ("index.html", "Ana sayfa"),
    ("ozellikler.html", "Özellikler"),
    ("nasil-calisir.html", "Nasıl çalışır"),
    ("bulusma-noktasi.html", "Buluşma noktası"),
    ("afete-hazirlik.html", "Afete hazırlık"),
    ("hakkinda.html", "Hakkında"),
    ("indir.html", "İndir"),
]

STORES = """<div class="magazalar">
  <a class="magaza" href="https://apps.apple.com/tr/app/id1488896334"><small>iPhone için</small><b>App Store</b></a>
  <a class="magaza" href="https://play.google.com/store/apps/details?id=genel.akut.guvendeyim"><small>Android için</small><b>Google Play</b></a>
  <a class="magaza" href="https://appgallery.huawei.com/app/C102224999"><small>Huawei için</small><b>AppGallery</b></a>
</div>"""

SUGGESTIONS_URL = "https://www.guvendeyim.org.tr/bulusma-noktalari/"


def card(title, text, link=None, label=None):
    more = f'<a class="devam" href="{link}">{label} →</a>' if link else ""
    return f'<div class="kart"><h3>{title}</h3><p>{text}</p>{more}</div>'


def checklist(title, items):
    rows = "".join(f"<li>{item}</li>" for item in items)
    return f'<div class="kart"><h3>{title}</h3><ul class="liste">{rows}</ul></div>'


def page_head(title, lead):
    return f'<div class="sayfa-basi"><div class="ic"><h1>{title}</h1><p>{lead}</p></div></div>'


PAGES = {}

PAGES["index.html"] = ("Güvendeyim – Afet anında tek tuşla haber verin",
    "AKUT'un ücretsiz Güvendeyim uygulaması: afet ve acil durumda tek tuşla yakınlarınıza konumunuzu SMS ile bildirin.",
    f"""<div class="kahraman"><div class="ic">
  <div>
    <h1>Afet anında tek tuşla “Güvendeyim” deyin.</h1>
    <p>Güvendeyim, acil durumda yakınlarınıza nerede olduğunuzu bildirir: tek tuşla, konumunuzla birlikte, en fazla 10 kişiye SMS gider. AKUT tarafından geliştirilmiştir ve ücretsizdir.</p>
    {STORES}
  </div>
  <div class="gorsel"><img src="img/icon.png" alt="Güvendeyim uygulama simgesi: birbirini tutan iki el"></div>
</div></div>
<main><section><div class="ic">
  <div class="izgara">
    {card("Neler yapar?", "Tek tuşla konumlu SMS, düdük, bildirimler ve internet olmadan okunabilen afet rehberleri.", "ozellikler.html", "Özellikler")}
    {card("Nasıl çalışır?", "Kurulum birkaç dakika sürer: adınızı ve en fazla 10 acil kişiyi ekleyin, düğme yeşile dönsün.", "nasil-calisir.html", "Adım adım")}
    {card("Buluşma noktası", "Ailenizle bir asıl, bir yedek buluşma noktası belirleyin ve tek bağlantıyla paylaşın.", "bulusma-noktasi.html", "Nasıl seçilir")}
    {card("Afete hazırlık", "Deprem, sel ve yangında ne yapılır, acil durum çantasına ne konur.", "afete-hazirlik.html", "Rehberler")}
  </div>
</div></section></main>""")

PAGES["ozellikler.html"] = ("Özellikler – Güvendeyim",
    "Güvendeyim uygulamasının özellikleri: tek tuşla konumlu SMS, 10 acil kişi, düdük, afet rehberleri, buluşma noktaları, altı dil.",
    page_head("Özellikler", "Afet ve acil durumda en çok ihtiyaç duyulan şeyi, haber vermeyi, mümkün olduğunca basit hale getirir.") + f"""
<main><section><div class="ic"><div class="izgara">
  {card("Tek tuşla haber", "Ana ekrandaki düğmeye basın; adınız, telefonunuz, konumunuz ve harita bağlantısı kayıtlı kişilerinize SMS olarak gider.")}
  {card("10 acil kişi", "Mesajın gideceği en fazla 10 kişiyi önceden rehberinizden seçersiniz. Acil anda kimseyi aramanız gerekmez.")}
  {card("Düdük", "Sesinizi duyuramadığınızda düdük düğmesiyle bulunduğunuz yeri belli edebilirsiniz.")}
  {card("Bildirimler", "AKUT'un duyuruları uygulamaya bildirim olarak gelir ve sonradan okunmak üzere listede saklanır.")}
  {card("Temel bilgiler", "Deprem, sel ve yangında ne yapılır, acil durum çantasına ne konur: internet olmadan da okunabilen kısa rehberler.", "afete-hazirlik.html", "Rehberlere bakın")}
  {card('Buluşma noktaları <span class="etiket">Yeni</span>', "Ailenizle bir asıl, bir yedek buluşma noktası belirleyin; haritadan seçin, tek bağlantıyla paylaşın. Yeni sürümle geliyor.", "bulusma-noktasi.html", "Ayrıntılar")}
  {card("Altı dil", "Türkçe, İngilizce, Almanca, Azerbaycan Türkçesi, Farsça ve Arapça. Acil numaralar seçtiğiniz ülkeye göre gösterilir.")}
  {card("Üyelik yok", "Hesap açmanız ya da giriş yapmanız gerekmez. Bilgileriniz telefonunuzda kalır.")}
</div></div></section></main>""")

PAGES["nasil-calisir.html"] = ("Nasıl çalışır – Güvendeyim",
    "Güvendeyim nasıl kurulur ve kullanılır: ayarları açın, kişilerinizi ekleyin, acil durumda yeşil düğmeye basın.",
    page_head("Nasıl çalışır?", "Kurulum birkaç dakika sürer ve bir kez yapılır. Afetten önce yapın.") + """
<main><section class="gri"><div class="ic">
  <ol class="adimlar">
    <li><h3>Ayarları açın</h3><p>Adınızı, telefon numaranızı ve en fazla 10 acil kişiyi ekleyin.</p></li>
    <li><h3>Kaydedin</h3><p>Bilgileriniz kaydedilince ana ekrandaki düğme yeşile döner.</p></li>
    <li><h3>Acil durumda basın</h3><p>Yeşil düğmeye basın; uygulama konumunuzu tüm kişilerinize SMS ile gönderir.</p></li>
    <li><h3>Yakınlarınız görür</h3><p>Kişileriniz adınızı, numaranızı, konumunuzu ve harita bağlantısını içeren mesajı alır.</p></li>
    <li><h3>Düdük</h3><p>Düdük düğmesiyle acil durumda kendinizi duyurabilirsiniz.</p></li>
  </ol>
</div></section>
<section><div class="ic">
  <h2>Uygulamanın hazır kalması için</h2>
  <p class="alt-baslik">Acil durum uygulaması en gerektiği anda çalışmalıdır. Kurduktan sonra şunlara dikkat edin.</p>
  <div class="izgara">
    <div class="kart"><h3>Konum izni verin</h3><p>Kesin konumunuzun belirlenmesi için uygulamaya konum izni gerekir.</p></div>
    <div class="kart"><h3>iPhone</h3><p>iPhone, yer açmak için uzun süre kullanılmayan uygulamaları kaldırabilir; internet yokken uygulama yeniden indirilemez. Ayarlar'da App Store bölümünden “Kullanılmayan Uygulamaları Kaldır” seçeneğini kapatın.</p></div>
    <div class="kart"><h3>Android ve Huawei</h3><p>Telefonunuz uzun süre kullanılmayan uygulamaları uyutabilir, izinlerini kaldırabilir ya da arşivleyebilir. Telefon ayarlarından Güvendeyim için bu özellikleri kapatın ve uygulamayı ara sıra açın.</p></div>
  </div>
</div></section></main>""")

PAGES["bulusma-noktasi.html"] = ("Buluşma noktası – Güvendeyim",
    "Afet sonrası ailenizle buluşacağınız yeri önceden belirleyin: bir asıl, bir yedek nokta. Yakınınızdaki açık alan önerileri.",
    page_head("Buluşma noktası", "Afet sonrası telefonlar çalışmayabilir. Ailenizle nerede buluşacağınızı önceden kararlaştırın.") + f"""
<main><section><div class="ic">
  <h2>İki nokta belirleyin</h2>
  <p class="alt-baslik">Önce birinci noktaya gidilir; oraya ulaşılamıyorsa yedek noktaya.</p>
  <div class="izgara">
    {card("1 · Asıl nokta", "Evinize en yakın, ailede herkesin bildiği açık alan.")}
    {card("2 · Yedek nokta", "İlkine ulaşılamazsa gidilecek, farklı yöndeki ikinci yer.")}
    {checklist("Nasıl bir yer?", ["Açık alan, binalardan ve duvarlardan uzak", "Ailede herkesin yürüyerek ulaşabileceği kadar yakın", "Tarifi kolay: “parkın çeşme tarafı” gibi", "Çocukların da bulabileceği bir yer"])}
  </div>
</div></section>
<section class="gri"><div class="ic iki">
  <div>
    <h2>Yakınınızdaki açık alanlar</h2>
    <p>Türkiye genelinde park, meydan, pazar yeri, spor sahası ve oyun alanlarından oluşan bir öneri listesi hazırladık. İl ve ilçenizi seçip harita üzerinde bakabilirsiniz.</p>
    <p>Liste OpenStreetMap verisinden otomatik üretilmiş bir öneridir; resmi bir belirleme ya da güvenlik garantisi değildir. Seçtiğiniz yeri kendiniz görün.</p>
    <a class="dugme" href="{SUGGESTIONS_URL}">Öneri listesini açın</a>
  </div>
  <div class="kart"><h3>Uygulamada <span class="etiket">Yeni</span></h3><p>Yeni sürümle birlikte buluşma noktalarınızı uygulamada haritadan seçebilir, ailenizle tek bağlantıyla paylaşabilir ve sizinle paylaşılan noktaları ayrı bir listede görebilirsiniz.</p></div>
</div></section></main>""")

PAGES["afete-hazirlik.html"] = ("Afete hazırlık – Güvendeyim",
    "Deprem, sel ve yangından önce, sırasında ve sonrasında yapılacaklar; acil durum çantasına konacaklar.",
    page_head("Afete hazırlık", "Uygulamadaki temel bilgiler burada da var. Kısa listeler; önceden okuyun.") + f"""
<main>
<section id="deprem"><div class="ic">
  <h2>Deprem</h2>
  <p class="alt-baslik">Deprem sırasında binadan çıkmaya çalışmayın. Sarsıntı durana kadar bekleyin.</p>
  <div class="izgara">
    {checklist("Depremden önce", ["Acil durum çantası hazırlayın", "Gaz, su ve elektriği nasıl keseceğinizi öğrenin", "Evdeki güvenli yerleri belirleyin", "Aile ile buluşma noktası belirleyin", "Ağır mobilyaları sabitleyin"])}
    {checklist("Deprem sırasında", ["Çökün, sağlam bir masanın altına geçin", "Pencere ve dış duvarlardan uzak durun", "Sokağa koşmayın", "Asansör kullanmayın", "Sakin olun ve başınızı koruyun"])}
    {checklist("Depremden sonra", ["Binadan merdivenle sakin şekilde çıkın", "Gaz borularını kontrol edin; koku varsa hemen havalandırın", "Açık ateş kullanmayın", "Resmi uyarıları takip edin", "Yakınlarınıza haber vermek için Güvendeyim düğmesine basın"])}
  </div>
</div></section>
<section id="sel" class="gri"><div class="ic">
  <h2>Sel</h2>
  <p class="alt-baslik">Akan sudan gereksiz yere geçmeyin. 15 cm derinliğinde hızla akan su bile tehlikeli olabilir.</p>
  <div class="izgara">
    {checklist("Selden önce", ["Hava tahminlerini ve uyarıları takip edin", "Acil durum çantası hazırlayın", "Değerli eşyaları üst katlara taşıyın", "Alçak bölgelerdeki elektrikli cihazları kapatın", "Bölgenizdeki tahliye güzergahlarını öğrenin"])}
    {checklist("Sel sırasında", ["Hemen yüksek bir yere geçin", "Su basan yollardan geçmeye çalışmayın", "Suya yakın elektrikli cihazlara dokunmayın", "Araç su içinde kalırsa hemen çıkın", "Yetkililerin talimatlarına uyun"])}
    {checklist("Selden sonra", ["Binaya yalnızca resmi izinle girin", "Güvenli ilan edilene kadar musluk suyu içmeyin", "Hasarları kayıt altına alın", "Küf ve neme dikkat edin", "Yakınlarınıza haber vermek için Güvendeyim düğmesine basın"])}
  </div>
</div></section>
<section id="yangin"><div class="ic">
  <h2>Yangın</h2>
  <span class="acil">Acil: 112</span>
  <p class="alt-baslik">Büyük yangını kendiniz söndürmeye çalışmayın. Güvenliğiniz her şeyden önemlidir.</p>
  <div class="izgara">
    {checklist("Önleme", ["Duman dedektörü takın ve düzenli kontrol edin", "Yangın söndürücü bulundurun", "Yanan mumları gözetimsiz bırakmayın", "Elektrik prizlerini aşırı yüklemeyin", "Aile ile kaçış yollarını belirleyin ve pratik yapın"])}
    {checklist("Yangın sırasında", ["Hemen 112'yi arayın", "Binadan derhal çıkın; hiçbir şey almayın", "Kapıları arkanızda kapatın (kilitlemeyin)", "Asansör kullanmayın", "Dumanlı alanlarda eğilerek ilerleyin", "Çıkış kapalıysa pencereyi açın ve yardım isteyin"])}
    {checklist("Yangından sonra", ["Binaya yalnızca itfaiye izninden sonra girin", "Yapısal hasarlara dikkat edin", "Yakınlarınıza haber vermek için Güvendeyim düğmesine basın"])}
  </div>
</div></section>
<section id="canta" class="gri"><div class="ic">
  <h2>Acil durum çantası</h2>
  <p class="alt-baslik">Çantanızı önceden hazırlayın. Acil durumda dakikalar içinde tahliye etmeniz gerekebilir.</p>
  <div class="izgara">
    {checklist("Tıbbi malzeme", ["İlk yardım çantası", "Reçeteli ilaçlar (en az 7 günlük)", "Ağrı kesici ve ateş düşürücü", "Bandaj malzemesi ve antiseptik", "Tek kullanımlık eldiven"])}
    {checklist("Su ve gıda", ["Kişi başı en az 3 litre su", "Uzun ömürlü gıda (konserve, granola, kuru meyve)", "Konserve açacağı", "Su arıtma tableti"])}
    {checklist("Önemli belgeler", ["Kimlik / pasaport (fotokopi)", "Sağlık sigortası kartı", "Acil iletişim listesi (basılı)", "Bozuk para ve küçük banknotlar"])}
    {checklist("Ekipman", ["El feneri ve yedek pil", "Düdük", "Isı battaniyesi", "Şarj kablosu ve powerbank", "Yedek kıyafet ve yağmurluk", "Hijyen ürünleri (diş fırçası, sabun, ıslak mendil)"])}
  </div>
</div></section>
</main>""")

PAGES["hakkinda.html"] = ("Hakkında – Güvendeyim",
    "Güvendeyim, AKUT Arama Kurtarma Derneği tarafından geliştirilen ücretsiz bir acil durum uygulamasıdır.",
    page_head("Hakkında", "Güvendeyim, AKUT Arama Kurtarma Derneği tarafından geliştirilir.") + """
<main><section class="akut"><div class="ic iki">
  <div class="metin">
    <h2>AKUT</h2>
    <p>AKUT Arama Kurtarma Derneği, 1996 yılında Türkiye'de kurulan, kâr amacı gütmeyen bir kuruluştur. Tamamen gönüllülerden oluşan dernek, doğal afet ve kazalarda arama kurtarma operasyonları yürütür.</p>
    <p>AKUT uzman gönüllüler yetiştirir; ilk yardım, dağ kurtarma, su kurtarma ve kentsel arama konularında eğitimler verir. Tüm faaliyetler gönüllülük esasıyla yürütülür.</p>
    <a class="dugme" href="https://www.akut.org.tr">akut.org.tr</a>
  </div>
  <div><img src="img/akut.png" alt="AKUT Arama Kurtarma Derneği logosu"></div>
</div></section>
<section class="gri"><div class="ic"><div class="izgara">
  <div class="kart"><h3>Gizlilik</h3><p>Uygulama üyelik istemez. Kişileriniz, mesajınız ve buluşma noktalarınız telefonunuzda saklanır.</p><a class="devam" href="https://www.akut.org.tr/guvendeyim-uygulamasi-gizlilik-politikasi">Gizlilik politikası →</a></div>
  <div class="kart"><h3>İletişim</h3><p>Soru, öneri ve hata bildirimleri için bize yazın.</p><a class="devam" href="mailto:guvendeyim@akut.org.tr">guvendeyim@akut.org.tr →</a></div>
  <div class="kart"><h3>Açık veri</h3><p>Buluşma noktası önerileri OpenStreetMap verisinden üretilir ve açık lisansla yayınlanır.</p><a class="devam" href="https://github.com/guvendeyim/bulusma-noktalari">Kaynak ve veri →</a></div>
</div></div></section></main>""")

PAGES["indir.html"] = ("İndir – Güvendeyim",
    "Güvendeyim'i App Store, Google Play ve AppGallery'den ücretsiz indirin.",
    page_head("Güvendeyim'i indirin", "Ücretsizdir, üyelik ya da giriş gerektirmez. Afetten önce kurun ve kişilerinizi ekleyin.") + f"""
<main><section class="indir"><div class="ic">
  {STORES}
</div></section>
<section class="gri"><div class="ic"><div class="izgara">
  {card("Kurduktan sonra", "Ayarlar'dan adınızı, numaranızı ve acil kişilerinizi ekleyin; düğme yeşile dönmeden mesaj gönderilemez.", "nasil-calisir.html", "Kurulum adımları")}
  {card("Ailenize de kurun", "Uygulama herkesin telefonunda kurulu ve ayarlı olduğunda işe yarar. Buluşma noktanızı da birlikte belirleyin.", "bulusma-noktasi.html", "Buluşma noktası")}
</div></div></section></main>""")


def render(name, title, description, body):
    def link(href, label):
        current = ' aria-current="page"' if href == name else ""
        return f'<a href="{href}"{current}>{label}</a>'

    nav = "".join(link(href, label) for href, label in MENU)
    return f"""<!doctype html>
<html lang="tr" class="betiksiz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.guvendeyim.org.tr/img/icon.png">
<link rel="icon" type="image/png" href="img/favicon.png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="stylesheet" href="css/site.css?v={CSS_VERSION}">
</head>
<body>
<header class="ust"><div class="ic">
  <a class="marka" href="index.html"><img src="img/icon.png" alt=""><strong>Güvendeyim</strong></a>
  <button class="menu-dugme" type="button" aria-expanded="false" aria-controls="ana-menu">Menü</button>
  <nav id="ana-menu" aria-label="Ana menü">{nav}</nav>
</div></header>
{body}
<footer><div class="ic">
  <span>© AKUT Arama Kurtarma Derneği</span>
  <nav aria-label="Alt menü">
    <a href="https://www.akut.org.tr/guvendeyim-uygulamasi-gizlilik-politikasi">Gizlilik politikası</a>
    <a href="mailto:guvendeyim@akut.org.tr">guvendeyim@akut.org.tr</a>
    <a href="{SUGGESTIONS_URL}">Buluşma noktası önerileri</a>
  </nav>
</div></footer>
<script>
document.documentElement.classList.remove("betiksiz");
(function () {{
  var dugme = document.querySelector(".menu-dugme"), menu = document.getElementById("ana-menu");
  dugme.addEventListener("click", function () {{
    var acik = menu.classList.toggle("acik");
    dugme.setAttribute("aria-expanded", acik);
  }});
}})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, description, body) in PAGES.items():
        with open(name, "w", encoding="utf-8") as f:
            f.write(render(name, title, description, body))
        print("yazıldı:", name)
