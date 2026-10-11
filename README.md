# guvendeyim.github.io

Güvendeyim uygulamasının tanıtım sitesi. Yedi sayfa, dış bağımlılık yok. Sayfalar `python3 build.py` ile üretilir; içerik ve menü `build.py` içindedir, biçim `css/site.css` dosyasındadır. Üretilen `*.html` dosyaları elle düzenlenmez.

- Yayın: https://guvendeyim.github.io/
- Buluşma noktası önerileri ayrı depodadır: https://github.com/guvendeyim/bulusma-noktalari

## Özel alan adı

Site `guvendeyim.org.tr` adresinde yayınlanır (`CNAME` dosyası). DNS Cloudflare'dedir: kök alan adı ve
`www`, `guvendeyim.github.io` adresine CNAME'dir ve proxy kapalıdır (yalnız DNS); GitHub'ın HTTPS
sertifikası çıkarabilmesi için böyle kalmalıdır.

GitHub, `guvendeyim.github.io/...` adreslerini `guvendeyim.org.tr/...` adresine yönlendirir; buna
`bulusma-noktalari` verisi de dahildir. Uygulamalar veriyi bu yönlendirme üzerinden indirir; DNS
kayıtları bozulursa uygulamalardaki öneri listesi boş gelir.
