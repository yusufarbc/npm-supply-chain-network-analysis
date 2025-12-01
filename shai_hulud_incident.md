# Shai-Hulud: NPM Ekosistemini Sarsan Tedarik Zinciri Saldırısı

## Giriş: Bir Dönüm Noktası
2025 yılı, yazılım tedarik zinciri güvenliği tarihinde bir kırılma noktası olarak kayıtlara geçti. NPM ekosistemi, "Shai-Hulud" (Dune evrenindeki dev kum solucanlarına atfen) adı verilen ve kendi kendini yayan (wormable) ilk büyük ölçekli kötü amaçlı yazılım saldırısına maruz kaldı. Bu olay, yalnızca binlerce projeyi etkilemekle kalmadı, aynı zamanda mevcut güvenlik paradigmalarının yetersizliğini de acı bir şekilde gözler önüne serdi. Bu proje, Shai-Hulud saldırısının ortaya çıkardığı yapısal zafiyetleri analiz etmek ve benzer tehditlere karşı topolojik bir risk modeli geliştirmek amacıyla başlatılmıştır.

## Saldırının Anatomisi

### 1. Dalga: Uyanış (Eylül 2025)
Saldırının ilk aşaması, `@ctrl/tinycolor`, `chalk` ve `debug` gibi popüler paketlerin taklit edilmesi ve ele geçirilmesiyle başladı. Shai-Hulud 1.0, `postinstall` betikleri aracılığıyla çalışarak geliştirici ortamlarındaki hassas verileri (token'lar, SSH anahtarları) hedef aldı. Ancak asıl tehlike, zararlının kendini kopyalayarak enfekte olan makineden yayınlanan diğer paketlere de sıçrama yeteneğiydi.

### 2. Dalga: "The Second Coming" (Kasım 2025)
Kasım ayında ortaya çıkan ikinci dalga, çok daha sofistike bir yapıdaydı. Saldırganlar, tespit edilmeyi zorlaştırmak için:
- **Preinstall Tetikleyicileri:** Zararlı kodun paket yüklenmeden hemen önce çalışmasını sağladılar.
- **Bun Runtime:** Node.js yerine daha hızlı ve güvenlik araçlarının henüz tam adapte olamadığı Bun çalışma zamanını kullandılar.
- **Çapraz Bulaşma (Cross-Exfiltration):** Çalınan verileri tek bir merkez yerine, ele geçirilen diğer kurbanların depolarına (repo) dağıtarak iz sürmeyi imkansız hale getirdiler.
- **Sabotaj Mekanizması:** Analiz edildiğini fark ettiğinde sistemdeki dosyaları silen "Dead Man's Switch" özellikleri eklediler.

## Yıkımın Boyutları
Kasım 2025 sonu itibarıyla tablonun vahameti şu şekildedir:
- **830+** Zehirli NPM paketi tespit edildi.
- **25.000+** GitHub deposu enfekte oldu.
- **14.000+** Kritik sır (API anahtarları, token'lar) sızdırıldı.
- **Milyonlarca** indirme işlemi risk altında gerçekleşti.

## Neden Bu Çalışma?
Shai-Hulud saldırısı, NPM ekosisteminin "küçük dünya" (small-world) yapısını ve merkezi paketlerin (hub) sistemik önemini kanıtladı. Geleneksel güvenlik tarayıcıları, paketlerin içeriğine odaklanırken, saldırganlar ağın topolojisini ve güven ilişkilerini kullandılar.

Bu projede geliştirilen **Bileşik Risk Skoru (BRS)** ve topolojik analiz metodolojisi, tam da bu tür saldırıların yayılma yollarını öngörmek için tasarlanmıştır. Shai-Hulud, ağdaki kritik düğümlerin (yüksek betweenness ve in-degree değerlerine sahip paketlerin) korunmasının, tüm ekosistemin sağlığı için ne denli hayati olduğunu göstermiştir.
