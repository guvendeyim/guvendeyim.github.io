# guvendeyim.github.io

Güvendeyim uygulamasının tanıtım sitesi. Yedi sayfa, dış bağımlılık yok. Sayfalar `python3 build.py` ile üretilir; içerik ve menü `build.py` içindedir, biçim `css/site.css` dosyasındadır (bağlantıya dosya özetinden üretilen `?v=` sürümü eklenir; CSS değişince `build.py` yeniden çalıştırılmalıdır). Üretilen `*.html` dosyaları elle düzenlenmez.

- Yayın: https://guvendeyim.github.io/
- Buluşma noktası önerileri ayrı depodadır: https://github.com/guvendeyim/bulusma-noktalari

## Özel alan adı

Site `www.guvendeyim.org.tr` adresinde yayınlanır (`CNAME` dosyası); `guvendeyim.org.tr` oraya yönlendirilir. DNS Cloudflare'dedir: kök alan adı ve
`www`, `guvendeyim.github.io` adresine CNAME'dir ve proxy kapalıdır (yalnız DNS); GitHub'ın HTTPS
sertifikası çıkarabilmesi için böyle kalmalıdır.

GitHub, `guvendeyim.github.io/...` ve `guvendeyim.org.tr/...` adreslerini `www.guvendeyim.org.tr/...` adresine yönlendirir; buna
`bulusma-noktalari` verisi de dahildir. Uygulamalar veriyi bu yönlendirme üzerinden indirir; DNS
kayıtları bozulursa uygulamalardaki öneri listesi boş gelir.

## Buluşma noktası önerileri sayfası

`www.guvendeyim.org.tr/bulusma-noktalari/` ayrı bir depodadır (`guvendeyim/bulusma-noktalari`) ama sitenin parçasıdır;
aynı üst menü, alt bilgi ve `css/site.css` ile üretilir. `build.py`, o depo bu deponun yanında duruyorsa
(`../bulusma-noktalari`) `sayfa/govde.html` dosyasını okuyup `docs/index.html` dosyasını yazar. Menü ya da düzen
değişince iki depo da commit edilip gönderilmelidir. Sayfaya özgü biçimler `css/site.css` sonundadır.
