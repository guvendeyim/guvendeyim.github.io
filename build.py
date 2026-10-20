"""Tanıtım sitesinin sayfalarını üretir: python3 build.py

Üst menü ve alt bilgi tek yerde durur; sayfa içerikleri aşağıdaki PAGES sözlüğündedir.
Üretilen *.html dosyaları elle düzenlenmez.
"""
import hashlib
import os

# Tarayıcı eski biçim dosyasını önbellekten kullanmasın diye bağlantıya dosyanın özeti eklenir;
# css/site.css değişince sürüm kendiliğinden değişir.
with open("css/site.css", "rb") as _css:
    CSS_VERSION = hashlib.sha256(_css.read()).hexdigest()[:8]

MENU = [
    ("index.html", "Ana sayfa"),
    ("nasil-calisir.html", "Nasıl çalışır"),
    ("bulusma-noktasi.html", "Buluşma noktası"),
    ("afete-hazirlik.html", "Afete hazırlık"),
    ("sikca-sorulan-sorular.html", "Sıkça Sorulan Sorular"),
    ("hakkinda.html", "Hakkında"),
    ("indir.html", "İndir"),
]

# Kaldırılan sayfaların eski bağlantıları yeni sayfaya yönlenir.
REDIRECTS = {
    "ozellikler.html": "nasil-calisir.html",
}

STORES = """<div class="magazalar">
  <a class="magaza" href="https://apps.apple.com/tr/app/g%C3%BCvendeyim/id1488896334"><small>iPhone için</small><b class="notranslate">App Store</b></a>
  <a class="magaza" href="https://play.google.com/store/apps/details?id=genel.akut.guvendeyim"><small>Android için</small><b class="notranslate">Google Play</b></a>
  <a class="magaza" href="https://appgallery.huawei.com/app/C102224999"><small>Huawei için</small><b class="notranslate">AppGallery</b></a>
</div>"""

SUGGESTIONS_URL = "https://www.guvendeyim.org.tr/bulusma-noktalari/"

# Dil seçici: sayfalar Türkçe yazılır, başka dil seçilince Google Çeviri ile makineyle çevrilir.
# Google'ın betiği yalnızca ziyaretçi bir dil seçtiğinde yüklenir (googtrans çerezi).
LANGUAGES = [
    ("tr", "Türkçe"), ("en", "English"), ("de", "Deutsch"), ("az", "Azərbaycanca"),
    ("fa", "فارسی"), ("ar", "العربية"), ("ru", "Русский"),
    ("uk", "Українська"), ("fr", "Français"), ("es", "Español"),
]
LANGUAGE_OPTIONS = "".join(f'<option value="{code}" lang="{code}">{label}</option>' for code, label in LANGUAGES)


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
    <h1>Afet anında tek tuşla <span class="vurgu">“Güvendeyim”</span> deyin.</h1>
    <p>Güvendeyim, acil durumda yakınlarınıza nerede olduğunuzu bildirir: tek tuşla, konumunuzla birlikte, en fazla 10 kişiye SMS gider. AKUT tarafından geliştirilmiştir ve ücretsizdir.</p>
    {STORES}
  </div>
  <div class="gorsel"><img src="img/icon.png" alt="Güvendeyim uygulama simgesi: birbirini tutan iki el"></div>
</div></div>
<main><section aria-labelledby="video-baslik"><div class="ic">
  <h2 id="video-baslik">Tanıtım videosu</h2>
  <p class="alt-baslik">Güvendeyim'in nasıl kullanıldığını AKUT'un tanıtım videosundan izleyin.</p>
  <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/pXO9Wrw-71I" title="Güvendeyim Uygulaması | AKUT" loading="lazy" allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
</div></section>
<section class="gri"><div class="ic">
  <div class="izgara">
    {card("Neler yapar?", "Tek tuşla konumlu SMS, düdük, bildirimler ve internet olmadan okunabilen afet rehberleri.", "nasil-calisir.html", "Özellikler")}
    {card("Nasıl çalışır?", "Kurulum birkaç dakika sürer: adınızı ve en fazla 10 acil kişiyi ekleyin, soluk gri düğme kırmızıya dönsün.", "nasil-calisir.html", "Adım adım")}
    {card("Buluşma noktası", "Ailenizle bir asıl, bir yedek buluşma noktası belirleyin ve tek bağlantıyla paylaşın.", "bulusma-noktasi.html", "Nasıl seçilir")}
    {card("Afete hazırlık", "Deprem, sel ve yangında ne yapılır, acil durum çantasına ne konur.", "afete-hazirlik.html", "Rehberler")}
  </div>
</div></section></main>""")

PAGES["nasil-calisir.html"] = ("Nasıl çalışır – Güvendeyim",
    "Güvendeyim nasıl kurulur ve kullanılır, neler yapar: tek tuşla konumlu SMS, 10 acil kişi, düdük, afet rehberleri, buluşma noktaları, altı dil.",
    page_head("Nasıl çalışır?", "Kurulum birkaç dakika sürer ve bir kez yapılır. Afetten önce yapın.") + f"""
<main><section class="gri"><div class="ic">
  <h2>Adım adım</h2>
  <p class="alt-baslik">Afet ve acil durumda en çok ihtiyaç duyulan şeyi, haber vermeyi, mümkün olduğunca basit hale getirir.</p>
  <ol class="adimlar">
    <li><h3>Ayarları açın</h3><p>Adınızı, telefon numaranızı ve en fazla 10 acil kişiyi ekleyin.</p></li>
    <li><h3>Kaydedin</h3><p>Bilgileriniz kaydedilince ana ekrandaki soluk gri düğme kırmızıya döner.</p></li>
    <li><h3>Acil durumda basın</h3><p>Kırmızı düğmeye basın; uygulama konumunuzu tüm kişilerinize SMS ile gönderir.</p></li>
    <li><h3>Yakınlarınız görür</h3><p>Kişileriniz adınızı, numaranızı, konumunuzu ve harita bağlantısını içeren mesajı alır.</p></li>
    <li><h3>Düdük</h3><p>Düdük düğmesiyle acil durumda kendinizi duyurabilirsiniz.</p></li>
  </ol>
</div></section>
<section id="ozellikler"><div class="ic">
  <h2>Özellikler</h2>
  <p class="alt-baslik">Uygulamanın yaptığı her şey, kısaca.</p>
  <div class="izgara">
  {card("Tek tuşla haber", "Ana ekrandaki düğmeye basın; adınız, telefonunuz, konumunuz ve harita bağlantısı kayıtlı kişilerinize SMS olarak gider.")}
  {card("10 acil kişi", "Mesajın gideceği en fazla 10 kişiyi önceden rehberinizden seçersiniz. Acil anda kimseyi aramanız gerekmez.")}
  {card("Düdük", "Sesinizi duyuramadığınızda düdük düğmesiyle bulunduğunuz yeri belli edebilirsiniz.")}
  {card("Bildirimler", "AKUT'un duyuruları uygulamaya bildirim olarak gelir ve sonradan okunmak üzere listede saklanır.")}
  {card("Temel bilgiler", "Deprem, sel ve yangında ne yapılır, acil durum çantasına ne konur: internet olmadan da okunabilen kısa rehberler.", "afete-hazirlik.html", "Rehberlere bakın")}
  {card('Buluşma noktaları <span class="etiket">Yeni</span>', "Ailenizle bir asıl, bir yedek buluşma noktası belirleyin; haritadan seçin, tek bağlantıyla paylaşın. Yeni sürümle geliyor.", "bulusma-noktasi.html", "Ayrıntılar")}
  {card("Altı dil", "Türkçe, İngilizce, Almanca, Azerbaycan Türkçesi, Farsça ve Arapça. Acil numaralar seçtiğiniz ülkeye göre gösterilir.")}
  {card("Üyelik yok", "Hesap açmanız ya da giriş yapmanız gerekmez. Bilgileriniz telefonunuzda kalır.")}
</div>
</div></section>
<section class="gri"><div class="ic">
  <h2>Uygulamanın hazır kalması için</h2>
  <p class="alt-baslik">Acil durum uygulaması en gerektiği anda çalışmalıdır. Kurduktan sonra şunlara dikkat edin.</p>
  <div class="izgara">
    <div class="kart"><h3>Konum izni verin</h3><p>Kesin konumunuzun belirlenmesi için uygulamaya konum izni gerekir.</p></div>
    <div class="kart"><h3>iPhone</h3><p>iPhone, yer açmak için uzun süre kullanılmayan uygulamaları kaldırabilir; internet yokken uygulama yeniden indirilemez. Ayarlar'da App Store bölümünden “Kullanılmayan Uygulamaları Kaldır” seçeneğini kapatın.</p></div>
    <div class="kart"><h3>Android ve Huawei</h3><p>Telefonunuz uzun süre kullanılmayan uygulamaları uyutabilir, izinlerini kaldırabilir ya da arşivleyebilir. Telefon ayarlarından Güvendeyim için bu özellikleri kapatın ve uygulamayı ara sıra açın.</p></div>
  </div>
  <p class="kaynak">Aklınıza takılan başka bir şey varsa <a href="sikca-sorulan-sorular.html">Sıkça Sorulan Sorular</a> sayfasına bakın.</p>
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
    {checklist("Su ve gıda", ["Yeteri kadar su", "Uzun ömürlü gıda (konserve, granola, kuru meyve)", "Konserve açacağı", "Su arıtma tableti"])}
    {checklist("Önemli belgeler", ["Kimlik / pasaport (fotokopi)", "Sağlık sigortası kartı", "Acil iletişim listesi (basılı)", "Bozuk para ve küçük banknotlar"])}
    {checklist("Ekipman", ["El feneri ve yedek pil", "Düdük", "Isı battaniyesi", "Şarj kablosu ve powerbank", "Yedek kıyafet ve yağmurluk", "Hijyen ürünleri (diş fırçası, sabun, ıslak mendil)"])}
  </div>
</div></section>
</main>""")

PAGES["hakkinda.html"] = ("Hakkında – Güvendeyim",
    "Güvendeyim, AKUT Arama Kurtarma Derneği tarafından geliştirilen ücretsiz bir acil durum uygulamasıdır.",
    page_head("Hakkında", "Güvendeyim, AKUT Arama Kurtarma Derneği tarafından geliştirilmektedir.") + """
<main><section class="akut"><div class="ic iki">
  <div class="metin">
    <h2>AKUT</h2>
    <p>AKUT Arama Kurtarma Derneği, 1996 yılında Türkiye'de kurulan, kâr amacı gütmeyen bir kuruluştur. Tamamen gönüllülerden oluşan dernek, doğal afet ve kazalarda arama kurtarma operasyonları yürütmektedir.</p>
    <p>AKUT uzman gönüllüler yetiştirmekte; ilk yardım, dağ kurtarma, su kurtarma ve kentsel arama konularında eğitimler vermektedir. Tüm faaliyetler gönüllülük esasıyla yürütülmektedir.</p>
    <p>AKUT'un Türkiye'de 2.500'den fazla aktif gönüllü üyesi vardır.</p>
    <a class="dugme" href="https://www.akut.org.tr">akut.org.tr</a>
  </div>
  <div><img src="img/akut.png" alt="AKUT Arama Kurtarma Derneği logosu"></div>
</div></section>
<section id="katkida-bulunanlar" aria-labelledby="katki-baslik"><div class="ic">
  <h2 id="katki-baslik">Katkıda bulunanlar</h2>
  <p class="alt-baslik">Güvendeyim, AKUT adına gönüllülerin, farklı uzmanlıkların ve kurumsal destekçilerin katkılarıyla gelişmektedir.</p>
  <div class="metin">
    <p>Projenin ilk fikrini, dönemin AKUT Bilgi Teknolojileri Birim Sorumlusu <strong><a href="https://www.linkedin.com/in/ozgur-celik-89569917/">Özgür Çelik</a></strong> ortaya koydu. AKUT üyesi <strong><a href="https://www.linkedin.com/in/bmericc">Bahri Meriç Canlı</a></strong>, Genel Bilgi Teknolojileri döneminde proje koordinasyonunu üstlendi; daha sonra ana geliştirici oldu ve bugün de uygulamanın geliştirilmesini ve bakımını sürdürmektedir.</p>
    <p>Aralık 2019’da Android ve iOS kullanıcılarıyla buluşan Güvendeyim, yıllar içinde yeni cihazlara ve dillere genişledi. AKUT’un proje koordinasyonu, yazılım, içerik ve tanıtım katkıları bugün de devam etmektedir.</p>
  </div>
  <div class="izgara">
    <div class="kart"><h3>Yazılım geliştirme</h3><p><strong><a href="https://www.linkedin.com/in/mremre/">Emre Olgun</a></strong>, Genel Bilgi Teknolojileri adına ilk Android ve iOS uygulamalarını geliştirdi; sonraki özelliklere ve 2021’de Huawei platform desteğine katkı sundu. Bahri Meriç Canlı, ana geliştirici olarak uygulamaları, ortak dil altyapısını, buluşma noktalarını ve web projelerini geliştirmektedir.</p></div>
    <div class="kart"><h3>Görsel tasarım</h3><p><strong><a href="https://www.linkedin.com/in/emrullahyigin/">Emrullah YIGIN</a></strong>, AKUT Tasarım Birimi adına Güvendeyim’in logosu dahil tüm görsel ihtiyaçlarını karşıladı.</p></div>
    <div class="kart"><h3>İçerik ve tanıtım</h3><p><strong>AKUT Seminer Birimi</strong> uygulamanın içeriklerini sağlamaktadır. <strong>AKUT Kurumsal İletişim Birimi</strong> tanıtım çalışmalarını yürütmektedir.</p></div>
  </div>
</div></section>
<section class="gri" aria-labelledby="destek-baslik"><div class="ic">
  <h2 id="destek-baslik">Kurumsal destek</h2>
  <p class="alt-baslik">Güvendeyim’in farklı dönemlerinde Genel Bilgi Teknolojileri, Huawei Türkiye ve Amazon AWS projeye destek verdi.</p>
  <div class="izgara">
    <div class="kart"><h3>Genel Bilgi Teknolojileri</h3><p>İlk uygulamaların geliştirilmesine destek verdi. Bu dönemde Bahri Meriç Canlı proje koordinasyonunu yürütürken Emre Olgun şirket adına Android ve iOS geliştirmelerini gerçekleştirdi.</p></div>
    <div class="kart"><h3>Huawei Türkiye</h3><p>Güvendeyim’in AppGallery’de yer almasına ve dönemin Huawei akıllı saatlerine entegre edilmesine destek verdi. <strong><a href="https://www.linkedin.com/in/sabrina-cara-01054a15a/">Sabrina Cara</a></strong>, Huawei Türkiye adına 2021’de saat entegrasyonu, GT3 uyumluluğu, konum ve SMS geliştirmelerine katkı sundu. Watch GT2 Pro ve Watch GT3 desteği 2022’de duyuruldu.</p><a class="devam" href="https://www.huawei.com/tr/news/2022/akut-guvendeyim-uygulamasi-huawei-ile-artik-bileginizde">Huawei’nin duyurusu →</a></div>
    <div class="kart"><h3>Amazon AWS ve Sufle’nin katkısı</h3><p>Amazon AWS, 6 Şubat 2023 depremlerinin ardından uygulamanın artan kullanımını karşılamasına ve internet üzerinden SMS gönderimine destek verdi. Bu kapsamda <strong>Sufle</strong> teknik katkı sundu; <strong><a href="https://www.linkedin.com/in/gizemgur/">Gizem Gür</a></strong>, Sufle adına Android ve iOS SMS entegrasyonunu gerçekleştirdi. Bu destek, projenin o dönemdeki çalışmalarının bir parçasıdır.</p><a class="devam" href="https://www.aboutamazon.co.uk/news/community/how-amazon-is-helping-communities-impacted-by-the-earthquake-in-turkey">Amazon’un açıklaması →</a></div>
  </div>
</div></section>
<section aria-labelledby="tesekkur-baslik"><div class="ic metin">
  <h2 id="tesekkur-baslik">Teşekkürler</h2>
  <p>Güvendeyim’in 2019’da başlayan yolculuğunda görev yapan AKUT Yönetim Kurulu başkanları <strong><a href="https://www.hurriyet.com.tr/gundem/akutun-guvendeyim-uygulamasina-depremden-sonra-ilgi-41433594">Recep Şalcı</a>, <a href="https://www.adjustbrand.com/soylesiler/is-dunyasindaki-profesyonellerin-gonullu-olarak-katilimi-cok-onemli/">Zeynep Yosun Akverdi</a>, Barış Altan Doğan ve Serhat Akbel</strong>, projeye kişisel olarak da destek verdiler. Kendilerine ve Güvendeyim’e emek veren tüm gönüllülere teşekkür ederiz.</p>
  <p>Buluşma noktası önerilerinin açık coğrafi verilerini sağlayan <a href="https://www.openstreetmap.org/copyright">OpenStreetMap katkıcılarına</a> da teşekkür ederiz.</p>
</div></section>
<section class="gri"><div class="ic"><div class="izgara">
  <div class="kart"><h3>Gizlilik</h3><p>Uygulama üyelik istemez. Kişileriniz, mesajınız ve buluşma noktalarınız telefonunuzda saklanır.</p><a class="devam" href="https://www.akut.org.tr/guvendeyim-uygulamasi-gizlilik-politikasi">Gizlilik politikası →</a></div>
  <div class="kart"><h3>İletişim</h3><p>Soru, öneri ve hata bildirimleri için bize yazın.</p><a class="devam" href="mailto:guvendeyim@akut.org.tr">guvendeyim@akut.org.tr →</a></div>
  <div class="kart"><h3>Açık veri</h3><p>Buluşma noktası önerileri OpenStreetMap verisinden üretilmekte ve açık lisansla yayınlanmaktadır.</p><a class="devam" href="https://github.com/guvendeyim/bulusma-noktalari">Kaynak ve veri →</a></div>
</div></div></section></main>""")

PAGES["indir.html"] = ("İndir – Güvendeyim",
    "Güvendeyim'i App Store, Google Play ve AppGallery'den ücretsiz indirin.",
    page_head("Güvendeyim'i indirin", "Ücretsizdir, üyelik ya da giriş gerektirmez. Afetten önce kurun ve kişilerinizi ekleyin.") + f"""
<main><section class="indir"><div class="ic">
  {STORES}
</div></section>
<section class="gri"><div class="ic"><div class="izgara">
  {card("Kurduktan sonra", "Ayarlar'dan adınızı, numaranızı ve acil kişilerinizi ekleyin; düğme kırmızıya dönmeden mesaj gönderilemez.", "nasil-calisir.html", "Kurulum adımları")}
  {card("Ailenize de kurun", "Uygulama herkesin telefonunda kurulu ve ayarlı olduğunda işe yarar. Buluşma noktanızı da birlikte belirleyin.", "bulusma-noktasi.html", "Buluşma noktası")}
</div></div></section></main>""")


# Sıkça sorulan sorular: (soru, cevap). Cevaplar HTML olabilir; arama motorları için etiketsiz hali
# sayfaya FAQPage yapılandırılmış verisi olarak da eklenir.
FAQ = [
    ("Neden “Güvende değilim” düğmesi yok? Acil durumda aileme durumumu nasıl bildiririm?",
     "<p>Güvendeyim, afetten sonra yakınlarınıza hızlıca “iyiyim” diyebilmeniz ve hatların gereksiz aramalarla "
     "tıkanmaması için tasarlandı. Mesaj yalnızca sizin seçtiğiniz kişilere gider; AKUT'a, 112'ye ya da kurtarma "
     "ekiplerine ulaşmaz. “Güvende değilim” diye bir mesaj da yardım çağırmazdı; yardım için doğru yol 112'dir.</p>"
     "<p>Yardıma ihtiyacınız varsa önce <strong>112</strong>'yi arayın. Yakınlarınıza durumunuzu bildirmek için "
     "Güvendeyim düğmesine yine basabilirsiniz: mesajda konumunuz ve harita bağlantısı olduğu için yakınlarınız "
     "nerede olduğunuzu bilir ve yetkililere iletebilir. iPhone'da mesaj, göndermeden önce ekranda açılır; "
     "“yaralıyım” ya da “enkaz altındayım” gibi bir not ekleyebilirsiniz. Sesinizi duyuramıyorsanız düdük düğmesini kullanın.</p>"),
    ("Kişisel verilerimi saklıyor musunuz?",
     "<p>Uygulama üyelik istemez. Adınız, telefon numaranız, acil kişileriniz, mesajınız ve buluşma noktalarınız "
     "yalnızca telefonunuzda saklanır; AKUT'a gönderilmez. Konumunuz da AKUT'a gitmez: yalnızca düğmeye bastığınızda, "
     "mesajın içinde seçtiğiniz kişilere SMS ile gider.</p>"
     "<p>Uygulamayı geliştirebilmek için kimliğinizle ilişkilendirilmeyen kullanım istatistikleri ve hata kayıtları "
     "toplanır. Uygulamayı sildiğinizde telefondaki bilgileriniz de silinir. Ayrıntılar "
     "<a href=\"https://www.akut.org.tr/guvendeyim-uygulamasi-gizlilik-politikasi\">gizlilik politikasında</a>.</p>"),
    ("Düdük düğmesi telefonu titretiyor da. Bu, şarjımın daha çabuk bitmesine yol açmaz mı?",
     "<p>Titreşim bilerek eklendi. Arama kurtarma ekiplerinin kullandığı sismik dinleme cihazları, sesten çok "
     "titreşimi algılar. Enkaz altında sesiniz dışarıya ulaşmasa bile telefonun titreşimi enkaz içinde yayılır ve "
     "bu cihazlarla algılanabilir. Şarjınızı korumak için düdüğü sürekli değil, aralıklarla çalıştırın.</p>"),
    ("Mesaj AKUT'a ya da 112'ye gider mi?",
     "<p>Hayır. Mesaj yalnızca Ayarlar'da seçtiğiniz en fazla 10 kişiye gider. Hayati tehlikedeyseniz 112'yi arayın.</p>"),
    ("Güvendeyim ücretli mi?",
     "<p>Uygulama ücretsizdir. Mesajlar sizin hattınızdan normal SMS olarak gider; ücreti operatörünüzün tarifesine "
     "göredir, paketinizde SMS varsa oradan düşer.</p>"),
    ("İnternet olmadan çalışır mı?",
     "<p>Evet. SMS mobil şebeke üzerinden gider, konumunuz GPS ile bulunur; ikisi için de internet gerekmez. "
     "İnternet yokken konumun bulunması biraz daha uzun sürebilir. Afet rehberleri de internetsiz okunur.</p>"),
    ("Şebeke yoksa ne olur?",
     "<p>Şebeke yoksa SMS gönderilemez. Şebekenin çektiği bir yere, mümkünse açık alana geçip düğmeye yeniden basın.</p>"),
    ("Mesajı alacak kişilerin de uygulamayı kurması gerekir mi?",
     "<p>Hayır. Mesaj normal SMS olarak gelir; her telefonda okunur. Yine de ailenizin her bireyinin kendi "
     "telefonuna kurması, herkesin haber verebilmesi için önerilir.</p>"),
    ("Mesajda neler yazar? Metni değiştirebilir miyim?",
     "<p>Mesajda adınız, telefon numaranız, mesajınız, konumunuz ve harita bağlantısı bulunur. Mesaj metnini "
     "Ayarlar'dan değiştirebilirsiniz.</p>"),
    ("Kaç kişiye mesaj gönderebilirim?", "<p>En fazla 10 kişiye. Kişileri önceden rehberinizden seçersiniz.</p>"),
    ("Düğme neden gri, mesaj neden gitmiyor?",
     "<p>Adınız, telefon numaranız ya da acil kişileriniz henüz kaydedilmemiştir. Ayarlar'dan bilgileri girip "
     "kaydedin; düğme kırmızıya döner. <a href=\"nasil-calisir.html\">Kurulum adımları</a></p>"),
    ("iPhone'da neden “Gönder”e basmam gerekiyor?",
     "<p>Apple, uygulamaların kendi başına SMS göndermesine izin vermez. Güvendeyim mesajı ve alıcıları hazırlayıp "
     "mesaj ekranını açar, siz “Gönder”e basarsınız. Android ve Huawei telefonlarda mesaj doğrudan gönderilir.</p>"),
    ("Konumum bulunamazsa ne olur?",
     "<p>Konum birkaç saniye içinde bulunamazsa mesaj konumsuz da gönderilebilir. Konum izni verdiğinizden emin "
     "olun; açık alanda konum daha hızlı bulunur.</p>"),
    ("Hangi telefonlarda çalışır?",
     "<p>iOS 13 ve üstü iPhone'larda, Android 7.0 ve üstü telefonlarda ve Google hizmetleri olmayan Huawei "
     "telefonlarda (AppGallery) çalışır. <a href=\"indir.html\">İndirme bağlantıları</a></p>"),
    ("Hangi dillerde kullanılabilir?",
     "<p>Türkçe, İngilizce, Almanca, Azerbaycan Türkçesi, Farsça ve Arapça. Acil numaralar dile göre değil, "
     "Ayarlar'da seçtiğiniz ülkeye göre gösterilir.</p>"),
    ("Buluşma noktasını ailemle nasıl paylaşırım?",
     "<p>Uygulamada buluşma noktalarınızı seçip paylaş düğmesine basın; bir bağlantı oluşur. Bağlantıyı açan kişinin "
     "telefonunda Güvendeyim kuruluysa noktalar uygulamada açılır, kurulu değilse uygulamayı indirme sayfası gösterilir. "
     "<a href=\"bulusma-noktasi.html\">Buluşma noktası nasıl seçilir</a></p>"),
    ("Telefonumu değiştirirsem bilgilerim taşınır mı?",
     "<p>Bilgileriniz yalnızca telefonunuzda saklandığı için yeni telefonda Ayarlar'ı yeniden doldurmanız "
     "gerekebilir. Kurduktan sonra düğmenin kırmızı olduğunu kontrol edin.</p>"),
    ("Hata ya da öneriyi nereye bildiririm?",
     "<p><a href=\"mailto:guvendeyim@akut.org.tr\">guvendeyim@akut.org.tr</a> adresine yazın.</p>"),
]


def faq_schema():
    import html, json, re
    def plain(text):
        return html.unescape(re.sub(r"<[^>]+>", " ", text)).split()
    items = [{"@type": "Question", "name": q,
              "acceptedAnswer": {"@type": "Answer", "text": " ".join(plain(a))}} for q, a in FAQ]
    data = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items},
                      ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/ld+json">{data}</script>\n'


PAGES["sikca-sorulan-sorular.html"] = ("Sıkça Sorulan Sorular – Güvendeyim",
    "Güvendeyim hakkında sıkça sorulan sorular: neden “Güvende değilim” düğmesi yok, kişisel veriler saklanıyor mu, "
    "internetsiz çalışır mı, SMS ücretli mi.",
    page_head("Sıkça Sorulan Sorular", "Bize en çok sorulanlar. Cevabını bulamadığınız soruyu "
              '<a href="mailto:guvendeyim@akut.org.tr">guvendeyim@akut.org.tr</a> adresine yazın.') +
    '\n<main><section><div class="ic"><div class="sss">\n' +
    "".join(f'  <details><summary>{q}</summary><div class="cevap">{a}</div></details>\n' for q, a in FAQ) +
    "</div></div></section></main>")
PAGE_HEAD = {"sikca-sorulan-sorular.html": faq_schema()}


def redirect_page(target):
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Güvendeyim</title>
<link rel="canonical" href="https://www.guvendeyim.org.tr/{target}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body><p><a href="{target}">Sayfa taşındı: {target}</a></p></body>
</html>
"""


def render(name, title, description, body, base="", head=""):
    """base: bağlantı öneki; site kökü dışındaki sayfalar için "/". head: sayfaya özgü <head> etiketleri."""
    def link(href, label):
        current = ' aria-current="page"' if href == name else ""
        return f'<a href="{base}{href}"{current}>{label}</a>'

    nav = "".join(link(href, label) for href, label in MENU)
    return f"""<!doctype html>
<html lang="tr" class="betiksiz">
<head>
<meta charset="utf-8">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NT2BRHJYRX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-NT2BRHJYRX');
</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:image" content="https://www.guvendeyim.org.tr/img/icon.png">
<link rel="icon" type="image/png" href="{base}img/favicon.png">
<link rel="apple-touch-icon" href="{base}img/apple-touch-icon.png">
<link rel="stylesheet" href="{base}css/site.css?v={CSS_VERSION}">
{head}</head>
<body>
<header class="ust"><div class="ic">
  <a class="marka notranslate" href="{base}index.html"><img src="{base}img/icon.png" alt=""><strong>Güvendeyim</strong></a>
  <select class="dil notranslate" id="dil" aria-label="Dil / Language">{LANGUAGE_OPTIONS}</select>
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
(function () {{
  var secim = document.getElementById("dil");
  var m = document.cookie.match(/(?:^|; )googtrans=\\/tr\\/([^;]+)/);
  var dil = m ? decodeURIComponent(m[1]) : "tr";
  secim.value = dil;
  if (dil !== "tr") {{
    document.documentElement.lang = dil;
    if (dil === "ar" || dil === "fa") document.documentElement.dir = "rtl";
    window.googleTranslateElementInit = function () {{
      new google.translate.TranslateElement({{ pageLanguage: "tr", autoDisplay: false }}, "google_translate_element");
    }};
    var kutu = document.createElement("div");
    kutu.id = "google_translate_element";
    document.body.appendChild(kutu);
    var betik = document.createElement("script");
    betik.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    document.body.appendChild(betik);
  }}
  function cerez(deger, yasam) {{
    var alanlar = ["", "; domain=" + location.hostname, "; domain=." + location.hostname.replace(/^www\\./, "")];
    alanlar.forEach(function (alan) {{ document.cookie = "googtrans=" + deger + "; path=/" + alan + yasam; }});
  }}
  secim.addEventListener("change", function () {{
    if (secim.value === "tr") cerez("", "; expires=Thu, 01 Jan 1970 00:00:00 GMT");
    else cerez("/tr/" + secim.value, "");
    location.reload();
  }});
}})();
</script>
</body>
</html>
"""


# Buluşma noktası önerileri ayrı bir depoda (guvendeyim/bulusma-noktalari) durur ama sitenin parçasıdır:
# aynı menü ve düzenle üretilir. Gövdesi o depodaki sayfa/govde.html dosyasıdır; depo bu deponun
# yanında duruyorsa docs/index.html oraya yazılır.
SUGGESTIONS_REPO = os.path.join("..", "bulusma-noktalari")
SUGGESTIONS_HEAD = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">\n'


def write_suggestions_page():
    source = os.path.join(SUGGESTIONS_REPO, "sayfa", "govde.html")
    if not os.path.exists(source):
        print("atlandı (depo yanında değil):", source)
        return
    with open(source, encoding="utf-8") as f:
        body = f.read()
    target = os.path.join(SUGGESTIONS_REPO, "docs", "index.html")
    with open(target, "w", encoding="utf-8") as f:
        f.write(render("bulusma-noktasi.html", "Buluşma noktası önerileri — Güvendeyim",
                       "Afet sonrası ailenizle buluşabileceğiniz açık alanlar: il ve ilçeye göre park, meydan, "
                       "pazar yeri, spor sahası ve oyun alanı önerileri.",
                       body, base="/", head=SUGGESTIONS_HEAD))
    print("yazıldı:", target)


if __name__ == "__main__":
    for name, (title, description, body) in PAGES.items():
        with open(name, "w", encoding="utf-8") as f:
            f.write(render(name, title, description, body, head=PAGE_HEAD.get(name, "")))
        print("yazıldı:", name)
    for name, target in REDIRECTS.items():
        with open(name, "w", encoding="utf-8") as f:
            f.write(redirect_page(target))
        print("yönlendirme:", name, "→", target)
    write_suggestions_page()
