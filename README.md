# npm-supply-chain-network-analysis
Directed network analysis of NPM package dependencies using centrality metrics to assess structural risks. The project aims to identify critical packages that pose systemic threats in potential supply chain attacks, moving beyond traditional vulnerability scoring. Includes Jupyter notebooks, visualizations, and Gephi-ready datasets.

# Yazılım Tedarik Zincirinde Kritiklik Haritalaması: NPM Ekosisteminde Topolojik Risk Analizi

Bu proje, NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip merkeziyet metrikleriyle yapısal riski ölçer. Amaç, klasik zafiyet skorlarının ötesine geçerek bir paketin ağ içindeki konumundan doğan sistemik riski görünür kılmaktır.

Canlı önizleme: https://yusufarbc.github.io/npm-supply-chain-network-analysis/

## Hızlı Başlangıç

Önkoşul: Python 3.11.x (önerilen 3.11.9)

1) Sanal ortamı kur ve etkinleştir (Windows PowerShell)
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2) Bağımlılıkları yükle
```
pip install -r analysis/requirements.txt
python -m pip install notebook
```
3) Notebook’u aç ve çalıştır
```
python -m notebook  # analysis/analysis.ipynb dosyasını aç
```
4) Sunumu görüntüle
- Yerel: `index.html`
- GitHub Pages: Actions ile otomatik dağıtım

## Kullanım (Notebook)

### 🚀 Tek Tıkla Tam Analiz

Notebook'u açın ve **ilk kod hücresini çalıştırın:**

```python
# ⚡ TAM PİPELİNE - HER ŞEYİ YAPAR
from analysis.run_pipeline import run_pipeline

# 🆕 VARSAYILAN: Most Dependents + 7 Kademe + Node Weights
result = run_pipeline(
    top_n=1000,                    # Kaç paket analiz edilecek
    leaderboard_mode="dependents",  # ⚠️ Varsayılan: En kritik altyapı paketleri
    depth=7,                        # 7 kademe derinlik (geniş ekosistem)
    results_dir="../results",      # Çıktı klasörü
    compute_plots=True,             # Görselleştirmeler
    export_gexf=False               # GEXF format (opsiyonel)
)

# 📊 Not: dependents_count otomatik node weight olarak eklenir
```

### 📊 Paket Seçim Modları (Leaderboard)

Başlangıç (Kademe 0) paket seti üç farklı kriterle çekilebilir:

| Mod | Parametre | Açıklama | Ne Zaman Kullanılır | Özellik |
|-----|-----------|----------|---------------------|----------|
| **Most Downloaded** | `downloads` | Haftalık/aylık indirme hacmi yüksek paketler | Genel ekosistem omurgası analizi | Yaygın kullanım |
| **Most Dependent**  | `dependents` | En çok bağımlı olunan paketler (transitif etki potansiyeli yüksek) | Kritiklik analizi (altyapı paketleri) | ⭐ **Varsayılan**, Yüksek in-degree korelasyonu |
| **Trending**        | `trending` | Ani indirme artışı yaşayan paketler (volatil) | Erken anomali / olası hedef izleme | Hızlı değişim, risk sinyali |

### ⚖️ Node Weight: dependents_count

Leaderboard API'sinden alınan **`dependents_count`** her düğüme otomatik eklenir:

```python
# Her paket için ekosistem genelindeki toplam dependent sayısı
G.nodes['lodash']['dependents_count']  # Örn: 156789
G.nodes['lodash']['downloads']         # Örn: 45000000
G.nodes['lodash']['rank']              # Örn: 12
```

**Fark:**
- **dependents_count**: Ekosistem geneli (NPM'deki tüm paketler) - API verisi
- **in_degree**: Sadece bu ağdaki bağımlılıklar (Top N + dependencies) - yerel hesaplama
- **Ilişki**: `dependents_count >= in_degree` (ekosistem > alt-ağ)

**Kullanım:**
- Ağırlıklı risk skoru hesaplama
- Kritiklik haritalam

a (gerçek ekosistem etkisi)
- Gephi'de node size olarak görselleritirme

**Kullanım Örnekleri:**

```python
# Varsayılan: En kritik altyapı paketleri (depth=7, dependents_count weight)
result = run_pipeline(top_n=1000)

# En çok indirilen paketlerle analiz
result = run_pipeline(top_n=1000, leaderboard_mode="downloads", depth=3)

# Trend paketleri izle (erken uyarı)
result = run_pipeline(top_n=500, leaderboard_mode="trending", depth=2)
```

**Risk Yorumları:**
- **dependents modu:** in-degree (kim bağımlı) yapısal önemle yüksek korelasyon → Çıkarıldığında maksimum ağ bozulması
- **downloads modu:** Kullanım yaygınlığı → Geniş etki yüzeyi, saldırı başarı oranı yüksek
- **trending modu:** Hızlı yükselen paketler → Potansiyel supply chain saldırı hedefi, erken tespit için ideal

### 🔄 İki Farklı Genişletme Modu

#### **Mod 1: Dependencies Zincirleme (depth parametresi)**
**Yön:** İleri → Paketlerin bağımlılıklarını takip et

```python
result = run_pipeline(
    top_n=1000,
    depth=2,                  # 🆕 İkinci kademe dependencies
    results_dir="../results"
)
```

**Çalışma Mantığı:**
```
Kademe 0: [react, lodash, webpack] (Top 1000)
    ↓ (dependencies)
Kademe 1: [prop-types, scheduler, ...] (~3K paket)
    ↓ (dependencies)  <-- depth=2 ile bu kademe eklenir
Kademe 2: [object-assign, fbjs, ...] (~8K paket)
```

**Veri Kaynağı:** NPM Registry (sınırsız, hızlı)
**Sonuç:** depth=1 → ~3K-5K düğüm, depth=2 → ~8K-15K düğüm

---

#### **Mod 2: Dependents Genişletme (expand_with_dependents)**
**Yön:** Geri ← Kim bu paketleri kullanıyor?

```python
result = run_pipeline(
    top_n=2000,                         # Max 2000 (ecosyste.ms limiti)
    expand_with_dependents=True,        # 🆕 Dependent paketleri de ekle
    max_packages_to_expand=500,         # İlk 500 paket için dependent çek
    max_dependents_per_package=20,      # Her paket için max 20 dependent
    results_dir="../results"
)
```

**Çalışma Mantığı:**
```
Top N: [react, lodash, ...]
    ↑ (kim kullanıyor?)  <-- Libraries.io API
Dependents: [gatsby, next, create-react-app, ...]
    ↓ (dependencies)  <-- Bu paketlerin bağımlılıkları da eklenir
Network genişler: ~15K-30K düğüm
```

**Veri Kaynağı:** Libraries.io API (rate limited ~60/dk, yavaş)
**Sonuç:** Ağ çok daha büyük, dependent ilişkileri görünür

---

**Karşılaştırma:**

| Özellik | depth=N | expand_with_dependents |
|---------|---------|------------------------|
| **Yön** | İleri (→) | Geri (←) + İleri |
| **Soru** | "Ne kullanıyor?" | "Kim kullanıyor?" |
| **API** | NPM Registry | Libraries.io + NPM |
| **Hız** | Hızlı | Yavaş (rate limit) |
| **Boyut** | Kontrollü | Çok büyür |
| **Öneri** | depth=1-2 yeterli | Özel analizler için |

⚠️ **Önemli Limitler ve Veri Kaynakları:**

**1. ecosyste.ms / npmleaderboard (Sadece İlk Liste):**
- Max **2000** paket → Bu sadece **Kademe 0** (başlangıç seed listesi) içindir
- `top_n` parametresi için üst limit
- **DİKKAT:** Bu limit tüm graf için değil, sadece ilk Top N seçimi için!

**2. NPM Registry (Dependencies - Sınırsız):**
- Her paket için `package.json` çeker
- Kademe 1, 2, 3... için **sınırsız** bağımlılık çekebilir
- `depth` parametresi ile kontrol edilir (varsayılan: 1 kademe)

**3. Libraries.io API (Dependents - Rate Limited):**
- Rate limit: ~60 istek/dakika
- **Sadece** `expand_with_dependents=True` iken kullanılır
- Öneri: `max_packages_to_expand=500-1000`, `max_dependents_per_package=20`

**depth Parametresi Nasıl Çalışır:**
```
depth=1 (varsayılan):
  Kademe 0: Top N (örn: 1000)           [ecosyste.ms]
  Kademe 1: Dependencies (0 → 1)        [NPM Registry]
  Toplam: ~3K-5K düğüm

depth=2:
  Kademe 0: Top N                       [ecosyste.ms]
  Kademe 1: Dependencies (0 → 1)        [NPM Registry]
  Kademe 2: Dependencies (1 → 2)        [NPM Registry]
  Toplam: ~8K-15K düğüm

depth=7:
  Kademe 0: Top N                       [ecosyste.ms]
  Kademe 1-7: Dependencies zincirleme   [NPM Registry - sınırsız]
  Toplam: ~50K-100K düğüm (tehlikeli!)
```

**Öneri:** `depth=1` yeterlidir, `depth=2` analiz için makul, `depth>3` önerilmez (hesaplama patlaması)

**Bu tek hücre tüm pipeline'ı çalıştırır:**
1. ✅ Top N paket listesini çeker (seçilen leaderboard moduna göre, max 2000)
2. ✅ Bağımlılık grafını oluşturur
3. ✅ Metrikleri hesaplar
4. ✅ **Gephi dosyalarını otomatik üretir**
5. ✅ Görselleştirmeleri yapar
6. ✅ Raporları oluşturur

**NOT:** Leaderboard modu seçimine göre analiz sonuçları değişir:
- `downloads`: Yaygın kullanım → Geniş kaskad etkisi
- `dependents`: Çekirdek altyapı → Çıkarıldığında yüksek ağ bozulması  
- `trending`: Volatil büyüme → Erken uyarı, anomali avı

### 📚 Alternatif: Adım Adım

Notebook'ta manuel kontrol için adım adım hücreler de mevcut.

**NOT:** Artık CLI kullanımı yok - tüm işlemler Jupyter Notebook içinden yapılır.

## Üretilen Çıktılar

### 📊 Temel Analiz Dosyaları
- `results/edges.csv` — Kenar listesi (source=dependent, target=dependency)
- `results/metrics.csv` — `package,in_degree,out_degree,betweenness,is_topN`
- `results/risk_scores.csv` — Bileşik risk skoru + metrikler
- `results/graph_stats.json` — Genel ağ istatistikleri
- `results/edge_betweenness_top10.csv` — En yüksek köprü kenarlar
- `results/cascade_impact_top20.csv` — Ters yön (dependents) kaskad etkisi

### 🎨 Gephi İçin Hazır Dosyalar (OTOMATİK ÜRETİLİR) ⭐
- **`results/gephi_edges.csv`** — ID bazlı kenar listesi (Source,Target,Type,Weight)
- **`results/gephi_nodes.csv`** — ID bazlı düğüm listesi (Id,Label,package,metrikler)
- Pipeline çalıştırıldığında otomatik üretilir!
- Detaylı kullanım: [`analysis/GEPHI_GUIDE.md`](analysis/GEPHI_GUIDE.md)

### 📈 Görselleştirmeler
- Görseller (PNG+SVG): histogramlar, saçılımlar, top10, top20 risk, ağ görselleri
- LaTeX Tabloları: `*.tex` (bkz. `analysis/make_tables.py`)

## Proje Yapısı
- `analysis/` — Notebook ve yardımcı Python kodlar (veri çekme, ağ kurma, metrikler)
- `results/` — Üretilen CSV/JSON, görseller ve LaTeX tablolar
- `academic/` — Literatür ve rapor materyali (bkz. `academic/topolojik-risk-degerlendirmesi.md`, `academic/Readme.md`)
 - `academic/` — Literatür ve rapor materyali (bkz. `academic/LITERATURE_REVIEW.md`, `academic/topolojik-risk-degerlendirmesi.md`, `academic/Readme.md`)
- `index.html` — Sonuçların statik sunumu (GitHub Pages)

Detaylar: `analysis/README.md`, `results/README.md`.

## Yöntem Özeti
- Ağ modeli: Düğümler paketleri, kenarlar Dependent → Dependency yönünü temsil eder; yönlü grafik (DiGraph).
- Metrikler: in-degree, out-degree, betweenness (büyük graflarda örnekleme ile hızlandırılır).
- Normalizasyon: min–max; tüm değerler eşitse 0 atanır.
- Risk: `risk = 0.5·in' + 0.2·out' + 0.3·btw'` (varsayılan).

## Notlar
- Büyük graflarda betweenness pahalı olabilir; örnekleme (`SAMPLE_K`) önerilir.
- API yanıtlarındaki geçici sorunlar için önbellek kullanılır: `results/cache_deps.json`.
- Örneklemeli betweenness için `seed=42` ile tekrarlanabilirlik sağlanır.

## 🎨 Gephi Görselleştirme

**Artık tamamen otomatik!** Notebook'u çalıştırdığınızda Gephi dosyaları hazır olur.

### Notebook'tan Otomatik Üretim
```python
# Notebook'ta ilk hücreyi çalıştırın, Gephi dosyaları otomatik üretilir
result = run_pipeline(top_n=1000)
# ✓ results/gephi_edges.csv  ⭐ ID bazlı kenar listesi
# ✓ results/gephi_nodes.csv  ⭐ ID bazlı düğüm listesi
```

### Gephi'de Açma
1. Gephi → **Import spreadsheet**
2. **`gephi_edges.csv`** seç → Edges table → Directed
3. Tekrar import → **`gephi_nodes.csv`** → Nodes table
4. Layout → Force Atlas 2

**Detaylı kılavuz:** 
- Layout önerileri (Force Atlas 2, OpenORD)
- Düğüm boyutu/renk ayarları
- Filtreleme senaryoları
- Risk haritası oluşturma

### Özellikler
- ✅ Notebook'tan tek tıkla üretim
- ✅ Deterministik ID'ler (alfabetik sıralı)
- ✅ Tüm metrikler dahil (in/out-degree, betweenness, risk)
- ✅ is_topN filtrelemesi
- ✅ Directed graph desteği
- ✅ Opsiyonel GEXF format

## Eylul 2025 NPM Saldırıları

### Olayın Özeti

Eylül 2025'te Node Package Manager (NPM) ekosistemi, tarihin en büyük tedarik zinciri saldırılarından birine maruz kaldı. Bu saldırı, phishing kampanyaları yoluyla paket bakıcılarının hesaplarının ele geçirilmesiyle başladı ve chalk, debug gibi popüler JavaScript paketlerine kötü amaçlı kod enjekte edilmesiyle devam etti. Saldırganlar, kripto para cüzdan adreslerini değiştirerek kullanıcıların fonlarını çalmayı hedefledi. Olay, açık kaynak yazılım ekosisteminin kırılganlığını bir kez daha gözler önüne serdi.

Saldırı, 5 Eylül 2025'te "npmjs.help" adlı sahte bir alan adının kaydedilmesiyle hazırlık aşamasına girdi. Bu alan, resmi NPM destek sitesini taklit ederek paket bakıcılarına phishing e-postaları gönderdi. E-postalar, iki faktörlü kimlik doğrulama (2FA) sıfırlama talebi gibi görünüyor ve bakıcıları kullanıcı adı, şifre ve TOTP kodlarını paylaşmaya ikna ediyordu. En bilinen mağdur, "qix-" olarak bilinen geliştirici Josh Junon'du. Hesabı ele geçirildikten sonra, saldırganlar 8 Eylül 2025'te saat 13:16 UTC'de kötü amaçlı sürümleri yayınlamaya başladı. Bu sürümler, tarayıcı ortamında çalışan bir "crypto-stealer" veya "wallet-drainer" içeriyordu.

Etkilenen paketler arasında chalk (konsol renklendirme), debug (hata ayıklama), ansi-styles (ANSI kodları işleme) gibi temel kütüphaneler yer alıyordu. Bu paketler, toplamda haftada 2.6 milyardan fazla indiriliyor ve birçok web uygulamasında geçişli bağımlılık olarak kullanılıyor. Saldırının mekanizması, kötü kodun tarayıcıya enjekte edilmesiyle başlıyordu: fetch, XMLHttpRequest ve cüzdan API'leri (örneğin window.ethereum, Solana API'leri) gibi işlevleri kancalıyor, ağ trafiğini izliyor ve kripto para adreslerini saldırganın kontrolündeki adreslerle değiştiriyordu. Desteklenen zincirler arasında Ethereum, Bitcoin, Solana, Tron, Litecoin ve Bitcoin Cash vardı. Kod, Levenshtein algoritması kullanarak benzer adresler üretiyor ve kullanıcı arayüzünde değişiklik yapmadan işlemi gizli tutuyordu. Ayrıca, veri hırsızlığı için hassas bilgileri exfiltre edebiliyordu.

Zaman çizelgesi şöyleydi:
- **5 Eylül 2025**: Sahte alan adı kaydedildi.
- **8 Eylül 2025, 13:16 UTC**: Kötü amaçlı sürümler yayınlandı (örneğin chalk@5.6.1, debug@4.4.2).
- **8 Eylül 2025, ~15:20 UTC**: Topluluk, GitHub'da şüpheli kodu fark etti ve uyarılar başladı.
- **8 Eylül 2025, öğleden sonra**: Bakıcılar, kötü sürümleri kaldırdı ve temiz sürümleri yayınladı. Saldırı yaklaşık 2 saat sürdü.
- **9-10 Eylül 2025**: Güvenlik firmaları (Palo Alto, Cycode) raporlar yayınladı.
- **15 Eylül 2025**: "Shai-Hulud" adlı solucan benzeri bir gelişme ortaya çıktı; bu, saldırıdan esinlenerek kendi kendine çoğalan bir malware olup yüzlerce paketi etkiledi.
- **23 Eylül 2025**: CISA, yaygın tedarik zinciri uyarısı yayınladı.

Olayın genel etkisi büyük oldu: Potansiyel olarak milyonlarca geliştirici ve milyarlarca indirme etkilendi. Kripto kayıpları sınırlı kaldı (yaklaşık 503 USD rapor edildi), çünkü erken tespit edildi. Ancak ekosistem riski yüksekti; CI/CD hatlarında çökmelere neden oldu ve web3 uygulamalarını tehdit etti. Shai-Hulud solucanı, saldırıyı genişleterek 500'den fazla paketi enfekte etti ve geliştirici kimlik bilgilerini çalmayı hedefledi.

### Etkilenen Paketler ve Etkiler

Aşağıdaki tablo, etkilenen 18 paketi, haftalık indirme sayılarını (yaklaşık değerler, NPM istatistiklerine göre), rollerini ve saldırı etkisini listeliyor. Toplam haftalık indirmeler 2.6 milyardan fazla; bu, JavaScript ekosisteminin %10'unu etkileyebilecek bir ölçek.

| Paket Adı       | Haftalık İndirme Sayısı | Rolü                          | Saldırı Etkisi                                                                 |
|-----------------|------------------------|-------------------------------|-------------------------------------------------------------------------------|
| ansi-styles    | 371.4 milyon          | ANSI kodları ile stil işleme | Adres değiştirme için tarayıcı kancaları enjekte edildi; veri hırsızlığı.    |
| debug          | 357.6 milyon          | Hata ayıklama aracı          | Cüzdan API'lerini hedef aldı; işlem hijack'i.                                 |
| chalk          | 299.9 milyon          | Konsol renklendirme         | Ağ trafiğini izleme ve adres swap'i; milyarlarca indirme riski.              |
| supports-color | 250 milyon            | Renk desteği tespiti         | Tarayıcı entegrasyonu yoluyla malware yayılımı.                               |
| strip-ansi     | 200 milyon            | ANSI kodlarını kaldırma      | Veri exfiltrasyonu; kripto zincirleri (ETH, SOL) hedeflendi.                  |
| ansi-regex     | 180 milyon            | ANSI regex eşleştirme        | Gizli işlem manipülasyonu.                                                    |
| wrap-ansi      | 150 milyon            | Metin sarma                  | Cüzdan adresi değiştirme.                                                     |
| color-convert  | 140 milyon            | Renk dönüştürme              | Bitcoin, Tron gibi zincirlerde adres hijack'i.                                |
| color-name     | 130 milyon            | Renk isimlendirme            | Malware obfuscation ile gizlendi.                                             |
| is-arrayish    | 120 milyon            | Dizi benzeri kontrol         | Tarayıcı trafiği interception.                                                |
| slice-ansi     | 110 milyon            | ANSI metin dilimleme         | Veri hırsızlığı riski.                                                        |
| color          | 100 milyon            | Renk yönetimi                | Solana API'leri hedeflendi.                                                   |
| color-string   | 90 milyon             | Renk dize ayrıştırma         | Litecoin, BCH adres swap'i.                                                   |
| simple-swizzle | 80 milyon             | Renk swizzle işlevi          | Genel ekosistem riski artırdı.                                                |
| supports-hyperlinks | 70 milyon        | Hiperlink desteği            | Web3 uygulamalarında yayılım.                                                 |
| has-ansi       | 60 milyon             | ANSI varlığını kontrol       | Erken tespit edildiği için sınırlı etki.                                      |
| chalk-template | 50 milyon             | Şablon renklendirme          | CI/CD çökmelerine neden oldu.                                                 |
| backslash      | 40 milyon             | Backslash işleme             | Malware'in stealth modunda kullanıldı.                                        |

Genel etki: Milyarlarca indirme risk altında kaldı, potansiyel kripto kayıpları milyonlarca USD olabilirdi ancak erken müdahale ile sınırlı tutuldu (yaklaşık 503 USD rapor edildi). Ekosistem riski, geçişli bağımlılıklardan kaynaklanıyordu; web uygulamaları ve DeFi platformları en çok etkilendi. Shai-Hulud solucanı gibi sonraki gelişmeler, saldırıyı kendi kendine çoğaltan bir hale getirdi; 16 Eylül 2025'te keşfedildi ve 500'den fazla paketi enfekte ederek geliştirici kimlik bilgilerini çaldı. Bu, tedarik zinciri saldırılarının evrimini gösterdi.

### Haber ve Rapor Kaynakları

Bu olay, web ve X (Twitter) üzerinde geniş yankı buldu. Aşağıda en az 15 kaynak özetleniyor; her birinin Türkçe özeti, orijinal link'i ve önemli alıntıları (İngilizce'den çevrilmiş) veriliyor. Türkçe kaynaklar sınırlı olduğundan, İngilizce olanlar çevrildi. Kaynaklar, güvenilir kurumlar (CISA, Palo Alto, Trend Micro) öncelikli.

1. **Palo Alto Networks Blog**: 8 Eylül 2025'te başlayan saldırıyı detaylandırıyor; phishing ile hesap ele geçirme ve 18 paketin kötü kod enjektesi. Link: https://www.paloaltonetworks.com/blog/cloud-security/npm-supply-chain-attack/. Alıntı: "Saldırganlar, tarayıcıda çalışan kodla kripto adreslerini değiştirerek fon çalıyor; haftalık 2.6 milyar indirme risk altında."

2. **Upwind Blog**: Debug ve chalk gibi paketlerin compromise'ını anlatıyor; 2 saatlik pencerede binlerce geliştirici etkilendi. Link: https://www.upwind.io/feed/npm-supply-chain-attack-massive-compromise-of-debug-chalk-and-16-other-packages. Alıntı: "Phishing e-postası, 2FA kodunu çalarak hesap erişimi sağladı; malware, cüzdan çağrılarını kancalıyor."

3. **NVD (CVE-2025-59144)**: Debug paketinin phishing ile ele geçirilmesini belgeleyen resmi CVE. Link: https://nvd.nist.gov/vuln/detail/CVE-2025-59144. Alıntı: "8 Eylül 2025'te NPM hesabı phishing saldırısıyla alınmış; kötü sürüm yayınlanmış."

4. **Cycode Blog**: Zaman çizelgesi ve mekanizma rehberi; sahte domain kullanımı. Link: https://cycode.com/blog/npm-debug-chalk-supply-chain-attack-the-complete-guide/. Alıntı: "Saldırı, npmjs.help domainiyle başladı; malware, işlem imzalamadan önce adres değiştiriyor."

5. **Vercel Blog**: Yanıt zaman çizelgesi; paket kaldırma süreci. Link: https://vercel.com/blog/critical-npm-supply-chain-attack-response-september-8-2025. Alıntı: "18 paket etkilendi; kötü kod, chalk ve debug'te enjekte edildi."

6. **Wiz Blog**: Qix'in hesabının ele geçirilmesini analiz ediyor. Link: https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk. Alıntı: "Tehdit aktörü, sosyal mühendislik ile hesabı aldı; milyarlarca indirme etkilendi."

7. **C3 Blog**: Etki ve yanıt rehberi. Link: https://c3.unu.edu/blog/the-largest-npm-supply-chain-attack-what-happened-impact-and-how-to-respond. Alıntı: "2 milyar haftalık indirme hedeflendi; kripto-clipper kod enjekte edildi."

8. **Kudelski Security**: Malware'in crypto-clipper olarak tanımlanması. Link: https://kudelskisecurity.com/research/npm-supply-chain-attack. Alıntı: "Kötü kod, cüzdan adreslerini değiştirerek işlem manipüle ediyor."

9. **CSA Singapur Uyarısı**: Kendiliğinden çoğalan payload uyarısı. Link: https://www.csa.gov.sg/alerts-and-advisories/alerts/al-2025-093/. Alıntı: "Kompromise edilmiş paketler, diğer paketleri enfekte eden payload içeriyor."

10. **Reddit (r/programming)**: Topluluk tartışması; bakıcı açıklaması. Link: https://www.reddit.com/r/programming/comments/1nbqt4d/largest_npm_compromise_in_history_supply_chain/. Alıntı: "NPM bakıcısı: 'Pwned oldum'; saldırı phishing ile başladı."

11. **CISA Uyarısı**: Yaygın compromise uyarısı; Shai-Hulud dahil. Link: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem. Alıntı: "NPM ekosistemi, tedarik zinciri compromise'ına maruz kaldı; bağımlılıkları kontrol edin."

12. **Trellix Raporu**: Hesap hijack ve Shai-Hulud analizi. Link: https://www.trellix.com/blogs/research/npm-account-hijacking-and-the-rise-of-supply-chain-attacks/. Alıntı: "Shai-Hulud, önceki saldırıdan evrildi; kimlik çalma odaklı."

13. **Trend Micro Araştırması**: Phishing kampanyası detayı. Link: https://www.trendmicro.com/en_us/research/25/i/npm-supply-chain-attack.html. Alıntı: "Hedefli phishing, NPM hesaplarını compromise etti; kötü kod enjekte edildi."

14. **Bleeping Computer Haber**: 2 milyar indirme etkilendi. Link: https://www.bleepingcomputer.com/news/security/hackers-hijack-npm-packages-with-2-billion-weekly-downloads-in-supply-chain-attack/. Alıntı: "Saldırganlar, phishing ile hesap aldı; 18 paket malware içeriyor."

15. **Ledger Uyarısı**: Kripto kullanıcılarına uyarı. Link: https://www.coindesk.com/tech/2025/09/08/ledger-cto-warns-of-npm-supply-chain-attack-hitting-1b-downloads. Alıntı: "Donanım cüzdan kullanıcıları işlem doğrulasın; yazılım cüzdanlar on-chain işlem yapmasın."

X postları da benzer detaylar içeriyor; örneğin Charles Guillemet'in uyarısı.

### Güvenlik Tavsiyeleri ve Yanıtlar

NPM, GitHub ve CISA gibi kurumlar hızlı yanıt verdi. NPM, compromise hesapları kilitledi ve kötü sürümleri kaldırdı. GitHub, zorunlu 2FA ve erişim token'larını güçlendirdi. CISA, bağımlılık kontrolleri önerdi.

Geliştiriciler için korunma yöntemleri:
- **MFA ve Pinning**: Çok faktörlü doğrulama kullanın; bağımlılıkları belirli sürümlere sabitleyin (dependency pinning).
- **Donanım Cüzdanları**: Ledger gibi donanım cüzdanları kullanın; işlem doğrulaması yapın.
- **Phishing'e Karşı Dikkat**: URL'leri kontrol edin; sahte e-postalara karşı eğitim alın.
- **Tarama Araçları**: Snyk, Dependabot gibi araçlarla bağımlılıkları tarayın; SBOM (Software Bill of Materials) oluşturun.
- **Güncelleme ve İzleme**: Paketleri güncelleyin; CI/CD'de güvenlik kuralları uygulayın (örneğin npm audit).
- **Runtime İzleme**: Uygulama runtime'ında anomalileri tespit edin; unused bağımlılıkları kaldırın.

Kurum yanıtları: NPM, yayın token'larını granüler hale getirdi; CISA, endüstri standartlarına (CIS, OWASP) uyumu teşvik etti.

### Benzer Olaylar ve Dersler

Bu saldırı, SolarWinds (2020) gibi tedarik zinciri saldırılarını andırıyor; orada Rus aktörler, yazılım güncellemelerine malware enjekte ederek hükümet ağlarını compromise etti. Log4j (2021) ise bir loglama kütüphanesindeki zero-day ile milyonlarca sistemi etkiledi; uzaktan kod çalıştırma sağladı. NPM olayı, phishing odaklı ve kripto hedefli olmasıyla ayrılıyor, ancak hepsi açık kaynak bağımlılıklarının riskini gösteriyor.

Dersler: Açık kaynak ekosistemi için MFA zorunluluğu, bağımlılık minimizasyonu ve otomatik tarama şart. Tedarik zinciri güvenliği, SLSA gibi çerçevelerle güçlendirilmeli. Geliştiriciler, phishing eğitimine odaklanmalı; kurumlar, primary kaynaklara (NVD, CISA) güvenmeli. Bu olay, 2025'te saldırıların evrimini (solucanlar gibi) vurguluyor; dengeli görüş için karşı argümanlar (örneğin erken tespit başarısı) dikkate alınmalı.

**Anahtar Kaynaklar:**
- Palo Alto Networks: https://www.paloaltonetworks.com/blog/cloud-security/npm-supply-chain-attack/
- CISA: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem
- Trend Micro: https://www.trendmicro.com/en_us/research/25/i/npm-supply-chain-attack.html
- Bleeping Computer: https://www.bleepingcomputer.com/news/security/hackers-hijack-npm-packages-with-2-billion-weekly-downloads-in-supply-chain-attack/
- Ledger: https://www.coindesk.com/tech/2025/09/08/ledger-cto-warns-of-npm-supply-chain-attack-hitting-1b-downloads
- Trellix: https://www.trellix.com/blogs/research/npm-account-hijacking-and-the-rise-of-supply-chain-attacks/
- Ve diğerleri yukarıda listelenenler.
