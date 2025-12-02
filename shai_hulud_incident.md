# Shai-Hulud: NPM Ekosisteminde Tedarik Zinciri Güvenliğinin Çöküşü

## 1. Giriş: Bir Dönüm Noktası
2025 yılı, yazılım tedarik zinciri güvenliği literatüründe kesin bir kırılma noktası olarak kayıtlara geçmiştir. NPM ekosistemi, Frank Herbert’ın *Dune* evrenindeki dev kum solucanlarına atıfla "Shai-Hulud" olarak adlandırılan ve kendi kendini yayan (wormable) ilk büyük ölçekli kötü amaçlı yazılım saldırısına maruz kalmıştır. Bu olay dizisi, yalnızca binlerce projeyi etkilemekle kalmamış, aynı zamanda mevcut güvenlik paradigmalarının—özellikle paket içeriğine odaklanan geleneksel tarayıcıların—yetersizliğini acı bir şekilde gözler önüne sermiştir.

Bu rapor, Shai-Hulud saldırısının iki dalgasını (Eylül ve Kasım 2025) teknik derinlikle analiz etmekte ve bu tür tehditlere karşı geliştirilen **topolojik risk modelinin (Bileşik Risk Skoru - BRS)** gerekliliğini ortaya koymaktadır.

## 2. Birinci Dalga: Uyanış (Shai-Hulud 1.0)
**Tarih Aralığı:** 5 – 23 Eylül 2025
**Kod Adı:** "Chalk & Debug Saldırısı"

Eylül ayındaki ilk dalga, ekosistemin merkezi düğümlerini hedef alan bir keşif saldırısı niteliğindeydi. Tehdit aktörleri, `@ctrl/tinycolor`, `chalk` ve `debug` gibi haftalık indirme sayısı 2.6 milyarı aşan 18 kritik paketi ele geçirmiştir.

### Saldırı Vektörü ve İnfaz
Saldırı, `npmjs.help` gibi inandırıcı sahte alan adları üzerinden, Josh Junon gibi kritik bakımcıların (maintainer) hesaplarının oltalama (phishing) yöntemiyle ele geçirilmesiyle başlamıştır.
* **Mekanizma:** Zararlı kod, `postinstall` betikleri aracılığıyla çalıştırılmıştır.
* **Payload:** Tarayıcı ortamında çalışan bir *crypto-clipper*. `fetch` ve `XMLHttpRequest` yapıları kancalanarak (hooking), kripto cüzdan adresleri Levenshtein mesafesi algoritması kullanılarak saldırganın adresleriyle anlık olarak değiştirilmiştir.
* **Etki:** Erken tespit sayesinde finansal zarar (~503 USD) sınırlı kalsa da, saldırının erişim potansiyeli ekosistemin kırılganlığını kanıtlamıştır.

## 3. İkinci Dalga: Yıkım ve Yayılma (Shai-Hulud 2.0)
**Tarih Aralığı:** 21 Kasım 2025 – Günümüz (Aktif)
**Kod Adı:** "The Second Coming"

Kasım ayında başlayan ikinci dalga, bir hırsızlık girişiminden ziyade, **otonom bir siber silaha** dönüşmüştür. Saldırganlar, tespit edilmeyi zorlaştırmak ve kalıcılığı sağlamak adına çok daha sofistike yöntemler kullanmıştır.

### Teknik Yenilikler ve Sofistikasyon
Shai-Hulud 2.0, önceki sürümden farklı olarak şu dört temel yetenekle donatılmıştır:

1.  **Preinstall Tetikleyicileri ve Bun Runtime:** Zararlı kod, paket henüz diskte tam oluşmadan (`preinstall`) devreye girmekte ve güvenlik araçlarının henüz tam adaptasyon sağlayamadığı **Bun** çalışma zamanını kullanarak Node.js tabanlı izleme araçlarını atlatmaktadır.
2.  **GitHub Actions ve CI/CD Zehirlenmesi:** `pull_request_target` zafiyetleri kullanılarak Zapier, Postman ve NextAuth gibi devlerin CI/CD süreçlerine sızılmış, `discussion.yaml` dosyaları üzerinden sisteme kalıcı (persistence) *self-hosted runner*lar eklenmiştir.
3.  **Çapraz Bulaşma (Cross-Exfiltration):** Çalınan veriler tek bir merkeze gönderilmek yerine, ele geçirilen diğer kurbanların depolarına (repo) dağıtılarak adli bilişim (forensics) takibi imkansız hale getirilmiştir.
4.  **Sabotaj Mekanizması (Dead Man's Switch):** Zararlı yazılım, analiz edildiğini veya engellendiğini fark ettiği anda `rm -rf /home` komutu ile sistemdeki dosyaları güvenli silme (secure overwrite) yöntemiyle yok etmektedir.

### Yıkımın Sayısal Boyutu (Kasım Sonu İtibarıyla)
* **Enfekte Paket:** 830+ benzersiz NPM paketi.
* **Etkilenen Repo:** 25.000+ GitHub deposu.
* **Sızan Kritik Veri:** 14.000+ API anahtarı ve token (Bunların 2.485'i saldırı anında hala aktifti).

## 4. Karşılaştırmalı Teknik Analiz

Aşağıdaki tablo, aynı tehdit aktörü tarafından gerçekleştirilen ancak motivasyon ve teknik kapasite açısından evrimleşen iki saldırı dalgasını karşılaştırmaktadır.

| Kriter | Shai-Hulud 1.0 (Eylül) | Shai-Hulud 2.0 (Kasım - Aktif) |
| :--- | :--- | :--- |
| **Ana Hedef** | Son kullanıcı kripto cüzdanları | Geliştirici kimlikleri ve Bulut (Cloud) erişimi |
| **Giriş Vektörü** | Klasik Phishing + 2FA Atlatma | GitHub Actions PR Exploit + Phishing |
| **Çalışma Zamanı (Runtime)** | Node.js | **Bun** (Daha hızlı, az tespit edilir) |
| **İnfaz (Execution)** | `postinstall` (Kurulum sonrası) | `preinstall` (Kurulum öncesi - daha agresif) |
| **Veri Sızdırma** | Basit betikler | TruffleHog entegrasyonu + Cloud SDK Full Dump |
| **Yayılma Modeli** | Manuel / Yarı-otomatik | **Tam Otomatik Worm** (Çalınan token ile kendini yayınlama) |
| **Kalıcılık (Persistence)** | Yok | Self-hosted runner + Workflow manipülasyonu |
| **Sabotaj** | Yok | "Dead man’s switch" (Veri imhası) |

## 5. Sonuç: Topolojik Analizin Zorunluluğu

Shai-Hulud saldırısı, NPM ekosisteminin "küçük dünya" (small-world) yapısını ve merkezi paketlerin (hub) sistemik önemini kanıtlayan en somut örnektir. Geleneksel güvenlik araçları paketlerin *içeriğine* (kod analizi) odaklanırken, saldırganlar ağın *topolojisini* ve *güven ilişkilerini* (graph structure) silah olarak kullanmıştır.

Bu bağlamda yürütülen **"NPM Tedarik Zinciri Ağ Analizi"** projesi, reaktif bir çözümden ziyade proaktif bir gerekliliktir. Proje kapsamında geliştirilen **Bileşik Risk Skoru (BRS)**; yüksek "betweenness centrality" (aradalık merkeziyeti) ve "dependent count" (bağımlı sayısı) değerlerine sahip paketleri belirleyerek, tam da Shai-Hulud 2.0'ın hedef aldığı yayılma rotalarını matematiksel olarak modellemeyi ve öngörmeyi amaçlamaktadır. Shai-Hulud bir uyarı değil, sistemin topolojik savunmasızlığının bir kanıtıdır.