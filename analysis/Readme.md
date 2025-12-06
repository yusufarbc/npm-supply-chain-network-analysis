## analysis/ — Running with Notebook (single method)

The analysis in this folder runs **only through Jupyter Notebook**. Please open the `analysis/analysis.ipynb` file and run the cells in order.

## 🎨 Using Gephi

Analysis creates Gephi-compatible files in the `results/` directory:

### 1. `gephi_nodes.csv` (Node List)
Contains columns like `Id`, `Label`, `RiskScore`, `InDegree`, `OutDegree`, `Betweenness`, `DependentsCount`, `Downloads`, `CommunityGroup`.

### 2. `gephi_edges.csv` (Edge List)
Contains 3 columns (Source, Target, Type).

### 3. Top 20 Lists (`results/top_lists/`)
CSV files containing the top 20 packages for each metric:
- `top20_risk_score.csv`
- `top20_betweenness.csv`
- `top20_in_degree.csv`
- ...and others.

### 4. Network Statistics (`results/network_stats.txt`)
A text report containing global network metrics such as Density, Transitivity, Assortativity, and Component counts.

### Opening in Gephi

1. **Import Nodes:**
   - File → Import spreadsheet...
   - File: `gephi_nodes.csv`
   - Separator: Comma
   - Import as: Nodes table
   - Force nodes to be created as new ones: ✓

2. **Import Edges:**
   - File → Import spreadsheet...
   - File: `gephi_edges.csv`
   - Separator: Comma
   - Import as: Edges table
   - Create missing nodes: ✗ (nodes already exist)

### Visualization Recommendations

- **Layout:** Force Atlas 2 (Scaling: 10.0, Prevent Overlap: ✓)
- **Node Size:** Ranking → InDegree or Betweenness
- **Node Color:** Partition → CommunityGroup (for clusters) OR Ranking → RiskScore (Green-Red)

## 🎯 Goal

Criticality mapping in the software supply chain: Analyzing the topological risk of the NPM ecosystem using **complex network theory**:

1. **Data Collection:** Fetch the most popular NPM packages and their dependencies
2. **Network Construction:** Create a directed dependency graph (Dependent → Dependency)
3. **Metric Calculation:** In-degree, out-degree, betweenness centrality, clustering, community detection
4. **Risk Scoring:** Generate Behavioral Risk Score (BRS) using weighted structural metrics
5. **Expansion (Optional):** Add packages dependent on Top N (1st degree expansion)

## 📊 Data Source

### Three Different Data Sources and Limits

#### 1. ecosyste.ms Leaderboard API (Tier 0 - Initial Seed List)
- **URL:** `https://ecosyste.ms/api/v1/registry/npm/leaderboard`
- **Limit:** Max **2000 packages** → This limit applies **ONLY** to the initial list (Tier 0)!
- **Usage:** `top_n` and `leaderboard_mode` parameters
- **Ranking Modes:**
  - `downloads`: By download count (default)
  - `dependents`: Most depended-upon packages
  - `trending`: Packages with sudden download spikes
- **Example:** `top_n=1000, leaderboard_mode="dependents"` → Top 1000 most critical packages

**IMPORTANT:** This 2000 limit is not for the entire graph, only for the Top N selection!

**Leaderboard Mode Comparison:**

| Mode | What it Measures | Advantage | Disadvantage | Use Case |
|-----|----------|---------|------------|---------------------|
| `downloads` | Weekly download volume | Widespread usage → Broad impact | Popularity ≠ criticality | General ecosystem analysis |
| `dependents` | How many packages depend on it | High infrastructure criticality | Low volatility | **Criticality mapping** ⭐ |
| `trending` | Sudden growth rate | Early signal, anomaly detection | Short-term volatile | Supply chain monitoring |

**Recommendation:** Use `leaderboard_mode="dependents"` for criticality analysis!

#### 2. NPM Registry (Tier 1, 2, 3... - Unlimited Dependencies)
- **URL:** `https://registry.npmjs.org/{package}`
- **Limit:** **Unlimited!** Dependencies can be fetched for every package
- **Usage:** Controlled by `depth` parameter
- **Version:** Latest tag or most current version
- **Field:** `dependencies` (optional: `peerDependencies`)
- **Cache:** `results/cache_deps.json` (prevents re-queries)

**How the depth Parameter Works:**
```
top_n=1000, depth=1:
  Tier 0: 1000 packages (ecosyste.ms - max 2000)
  Tier 1: ~3K-5K packages (NPM Registry - unlimited)
  Total: ~4K-6K nodes

top_n=1000, depth=2:
  Tier 0: 1000 packages (ecosyste.ms - max 2000)
  Tier 1: ~3K-5K packages (NPM Registry - unlimited)
  Tier 2: ~8K-15K packages (NPM Registry - unlimited)
  Total: ~12K-20K nodes

top_n=1000, depth=7:
  Tier 0: 1000 packages (ecosyste.ms - max 2000)
  Tier 1-7: ~50K-100K packages (NPM Registry - unlimited)
  Total: ~50K-100K nodes (!!!) - Not Recommended
```

**Result:** With 1000 packages and depth=7 → 10K-50K nodes are possible!

#### 3. Libraries.io API (Dependents - Rate Limited)
- **URL:** `https://libraries.io/api/npm/{package}/dependents`
- **Limit:** Rate limited (~60 istek/dakika)
- **Kullanım:** `expand_with_dependents=True` parametresi ile aktif edilir
- **Yön:** Ters bağımlılık (kim bu paketi kullanıyor?)
- **Özellik:** Yavaş ama dependent ilişkilerini gösterir

## 📁 İçerik

- **`analysis.ipynb`** — Adım adım veri çekme, ağ kurma, metrikler ve görselleştirme (tek çalışma yolu)
- **`analysis_helpers.py`** — API, önbellek, metrik ve görselleştirme yardımcıları
- **`run_pipeline.py`** — Tam pipeline orchestrator (notebook'tan çağrılır)
- **`exporter.py`** — Gephi export fonksiyonları
- **`make_tables.py`** — LaTeX tablo üreticileri
- **`requirements.txt`** — Çalışma zamanı bağımlılıkları
- **`GEPHI_GUIDE.md`** — Gephi görselleştirme kılavuzu
- Kavramsal rapor: `../academic/topolojik-risk-degerlendirmesi.md`

## 🔄 Çalışma Mantığı

Analiz pipeline'ı şu adımlardan oluşur:

```
┌─────────────────────────────────────────────┐
│  1. Top N Paket Listesi (Leaderboard API)  │
│     • Üç mod: downloads/dependents/trending │
│     • MAX 2000 paket (Kademe 0 seed list)   │
│     • Bu limit SADECE ilk liste için!       │
│     • Önerilen: leaderboard_mode=dependents │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  2. Dependencies Çekme (NPM Registry)       │
│     • Her paket için package.json al        │
│     • depth parametresi ile kademe kontrolü │
│     • Kademe 1, 2, ... SINIRSIZ çekilir    │
│     • Cache ile tekrar sorguları önle       │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  3. Yönlü Graf Oluşturma (NetworkX)         │
│     • Kenar: Dependent → Dependency         │
│     • Düğüm sayısı depth'e göre değişir:    │
│       - depth=1: ~3K-5K düğüm              │
│       - depth=2: ~8K-15K düğüm             │
│       - depth=7: ~50K-100K düğüm (!!!)     │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  4. Metrik Hesaplama                        │
│     • In-Degree: Etki alanı (dependent)     │
│     • Out-Degree: Karmaşıklık (dependency)  │
│     • Betweenness: Köprü rolü (k=200)       │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  5. Risk Skorlama (Min-Max Normalizasyon)   │
│     Risk = 0.5×In + 0.2×Out + 0.3×Between   │
│     • En kritik paketleri tespit et         │
│     • Leaderboard moduna göre yorumlama:    │
│       - dependents: Yapısal kritiklik       │
│       - downloads: Etki yüzeyi              │
│       - trending: Erken risk sinyali        │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│  6. Export & Görselleştirme                 │
│     • CSV: edges, metrics, risk_scores      │
│     • Gephi: nodes.csv + edges.csv          │
│     • PNG/SVG: Dağılım ve top N grafikleri  │
└─────────────────────────────────────────────┘
```

**Beklenen Sonuçlar (depth ve leaderboard_mode'a göre):**

| top_n | mode | depth | Düğüm | Kenar | Süre | Açıklama |
|-------|------|-------|-------|-------|------|----------|
| 1000 | dependents | 1 | ~3K-5K | ~8K-12K | 2-3 dk | **⭐ Önerilen** (kritik altyapı) |
| 1000 | downloads | 1 | ~3K-5K | ~8K-12K | 2-3 dk | Yaygın kullanım analizi |
| 1000 | trending | 1 | ~2K-4K | ~5K-10K | 2-3 dk | Erken uyarı (volatil) |
| 1000 | dependents | 2 | ~8K-15K | ~25K-40K | 5-10 dk | Derin kritiklik analizi |
| 2000 | dependents | 1 | ~6K-10K | ~15K-25K | 5-8 dk | Max seed (ecosyste.ms limiti) |

**Kritik Paketler (mod'a göre):**
- `dependents`: tslib, @smithy/types, @babel/helper-plugin-utils (yüksek in-degree)
- `downloads`: react, lodash, chalk (yaygın kullanım)
- `trending`: Yeni yükselen paketler (volatil, erken tespit)

**DİKKAT:** 
- ecosyste.ms'in 2000 limiti **sadece Kademe 0** içindir
- Kademe 1, 2, 3... NPM Registry'den **sınırsız** çekilir
- depth > 2 önerilmez (exponansiyel büyüme)

## ⚠️ Teknik Zorluklar ve Sınırlamalar

### 1. Dependent (Ters Bağımlılık) Verisinin Eksikliği

**Sorun:** NPM ekosisteminde bir paketi **kimin kullandığını** (dependents) bulmak teknik olarak zordur.

#### 1.1 Libraries.io API Devre Dışı
```
❌ https://libraries.io/api/npm/{package}/dependents
→ {"message": "Disabled for performance reasons"}
```
- **Açıklama:** Libraries.io, `/dependents` endpoint'ini **performans nedeniyle kapatmış**
- **Test Edildi:** 2025-11-23 tarihinde doğrulandı (react, lodash gibi popüler paketlerde)
- **Etki:** 1. derece dependent verisi API üzerinden çekilemiyor

#### 1.2 NPM Registry API'sinde Reverse Dependency Yok
- NPM Registry sadece **ileri yönlü bağımlılıklar** (dependencies) sağlar
- Bir paketi kimin kullandığını bulmak için **tüm 3.6M+ paketi taramak** gerekir
- **Maliyet:** Kabul edilemez düzeyde yavaş ve API rate limit sorunları

#### 1.3 Mevcut Çözüm: In-Degree Metriği
✅ **Alternatif yaklaşım:** Top N paketlerin dependencies'ini çekip, her dependency'nin **in-degree** (kaç Top N paketi ona bağlı) metriğini kullanarak **dolaylı dependent analizi** yapıyoruz.

**Örnek:**
```
react → loose-envify  (react, loose-envify'e bağımlı)
babel → loose-envify  (babel, loose-envify'e bağımlı)
→ loose-envify'nin in-degree = 2 (2 paket ona dependent)
```

**Sonuç:** Tam dependent verisi yerine, **in-degree metriği kritik paketleri tespit etmek için yeterli**.

### 2. Ağ Boyutu ve Hesaplama Performansı

#### 2.1 İkinci Kademe Dependencies Maliyeti
- **1. Kademe:** Top 1000 paketi → ~1200-1500 düğüm, ~2000-4000 kenar
- **2. Kademe:** + Dependencies'lerin dependencies → ~10K-50K düğüm, ~100K+ kenar
- **Sorun:** Betweenness centrality hesabı O(n³) karmaşıklığında, büyük graflarda saatler sürebilir

#### 2.2 Mevcut Çözüm: Örnekleme ve 1. Kademe Sınırı
```python
# Betweenness için k-node sampling
btw = nx.betweenness_centrality(G, k=200, normalized=True)

# Sadece 1. kademe dependencies (2. kademe devre dışı)
G, top_set = build_dependency_graph(top_packages, expand_with_dependents=False)
```

### 3. API Rate Limiting ve Güvenilirlik

#### 3.1 Ecosyste.ms API
- **Limit:** Max 1000 paket/sayfa, toplam ~2000-5000 paket çekilebilir
- **Sıralama:** İndirme sayısına göre, ancak güncel olmayabilir
- **Sorun:** Nadir durumlarda timeout veya boş yanıt

#### 3.2 NPM Registry
- **Rate Limit:** Sınırsız (public endpoint) ama yavaş
- **Güvenilirlik:** %99+ uptime, ama network hataları olabilir
- **Çözüm:** 3 denemeli retry mekanizması ve local cache

#### 3.3 Önbellek Stratejisi
```python
cache_deps.json  # Her paket için dependencies önbelleği
→ Tekrar çalıştırmada API sorgusu yapılmaz (hızlı test)
```

### 4. Veri Kalitesi ve Tamlık

#### 4.1 Deprecated ve Eski Paketler
- **Sorun:** Top N listesinde deprecated veya bakımsız paketler olabilir
- **Etki:** Risk analizi güncel olmayabilir
- **Örnek:** left-pad gibi kaldırılmış paketler

#### 4.2 PeerDependencies Dahil Edilmemesi
- **Varsayılan:** Sadece `dependencies` çekiliyor
- **İsteğe Bağlı:** `include_peer_deps=True` ile aktif edilebilir
- **Sorun:** PeerDeps dahil edilirse graf çok büyür, gürültü artar

### 5. Görselleştirme Sınırlamaları

#### 5.1 Matplotlib ile Büyük Graf Çizimi
- **Mümkün Değil:** 1000+ düğümlü grafı matplotlib'de çizmek okunaksız
- **Çözüm:** Gephi CSV export, sadece metrik grafikleri matplotlib'de

#### 5.2 Gephi Performansı
- **10K+ düğüm:** Force Atlas 2 layout saatler sürebilir
- **Çözüm:** Filter ile en riskli 500-1000 düğüme odaklan

## 🔧 Kurulum

### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r analysis/requirements.txt
python -m pip install notebook
```

### macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r analysis/requirements.txt
python -m pip install notebook
```

## 🚀 Notebook'u Başlatma

```bash
python -m notebook
```
Ardından `analysis/analysis.ipynb` dosyasını açın ve hücreleri sırayla çalıştırın.

### ⚡ Hızlı Başlangıç (Tek Hücre)

Notebook'ta ilk kod hücresini çalıştırın - tüm pipeline otomatik çalışır:

```python
from analysis.run_pipeline import run_pipeline

# Standart analiz (Top 1000)
result = run_pipeline(
    top_n=1000,
    results_dir="../results",
    compute_plots=True
)
```

**Bu tek komut şunları yapar:**
1. ✅ Top N paket listesini çeker (ecosyste.ms API)
2. ✅ Her paket için dependencies çeker (npm registry + önbellek)
3. ✅ Yönlü graf oluşturur (NetworkX DiGraph)
4. ✅ Metrikleri hesaplar (degree, betweenness)
5. ✅ Risk skorları üretir
6. ✅ Gephi CSV dosyalarını otomatik üretir ⭐
7. ✅ Görselleştirmeleri oluşturur (PNG+SVG)
8. ✅ LaTeX tabloları hazırlar

## 🔄 İki Tür Ağ Genişletme

### 📌 Temel Fark: depth vs expand_with_dependents

| Özellik | **depth=N** | **expand_with_dependents=True** |
|---------|-------------|----------------------------------|
| **Yön** | İleri (→) | Geri (←) + İleri |
| **Soru** | "Bu paket neye bağımlı?" | "Kim bu paketi kullanıyor?" |
| **API** | NPM Registry | Libraries.io + NPM Registry |
| **Limit** | **Sınırsız** (NPM Registry) | Rate limited (~60/dk) |
| **2000 Limiti** | **Sadece Kademe 0 için** | **Sadece Kademe 0 için** |
| **Hız** | Hızlı (2-10 dk) | Yavaş (30 dk - 2 saat) |
| **Düğüm Artışı** | Kontrollü (exponansiyel) | Çok büyük (dependent sayısına bağlı) |
| **Kullanım** | **Varsayılan - önerilir** | Özel analiz (dependent haritası) |

---

### Mod 1: Dependencies Zincirleme (depth parametresi) **[ÖNERİLEN]**

**Yön:** İleri → "Bu paket neye bağımlı?"

```
Kademe 0: [react, lodash, webpack] (Top 1000 - ecosyste.ms)
    ↓ (dependencies - NPM Registry)
Kademe 1: [prop-types, scheduler, ...] (~3K paket - SINIRSIZ)
    ↓ (dependencies - depth=2 ile)
Kademe 2: [object-assign, fbjs, ...] (~8K paket - SINIRSIZ)
    ↓ (depth=3 ile)
Kademe 3: [...] (~20K paket - SINIRSIZ)
```

**Örnek:**
```python
result = run_pipeline(
    top_n=1000,     # ecosyste.ms'den Top 1000 (Kademe 0)
    depth=2,        # Kademe 1 + Kademe 2 dependencies çek
)
# Kademe 0: 1000 paket (ecosyste.ms limiti)
# Kademe 1: ~3K paket (NPM Registry - sınırsız)
# Kademe 2: ~8K paket (NPM Registry - sınırsız)
# Toplam: ~12K düğüm
```

**Veri Kaynağı:** NPM Registry (sınırsız, hızlı)
**2000 Limiti:** Sadece Kademe 0 seed list için geçerli, Kademe 1+ sınırsız!

---

### Mod 2: Dependents Genişletme (expand_with_dependents) **[ÖZEL KULLANIM]**

**Yön:** Geri (←) + İleri → "Kim bu paketi kullanıyor?"

```
Top N Paketler: [react, lodash, ...]
    ↑ (kim kullanıyor? - Libraries.io API)
Dependents: [gatsby, next, create-react-app, ...]
    ↓ (dependencies - NPM Registry)
Dependent'ların Bağımlılıkları: [...]
```

**Örnek:**
```python
result = run_pipeline(
    top_n=2000,                      # Max 2000 (ecosyste.ms limiti)
    expand_with_dependents=True,     # 🆕 Dependent ekleme AÇIK
    max_packages_to_expand=500,      # İlk 500 paket için dependent çek
    max_dependents_per_package=20,   # Her paket için max 20 dependent
)
# Top 2000 + her birinin 20 dependent + dependent'ların deps
# Toplam: ~15K-30K düğüm
```

**Veri Kaynağı:** Libraries.io API (rate limited, yavaş)
**Sonuç:** Ağ çok büyür, dependent ilişkileri görünür

### Nasıl Çalışır?

```python
result = run_pipeline(
    top_n=2000,                        # Top 2000 paket (ecosyste.ms max 2K)
    expand_with_dependents=True,       # 🔄 Genişletme AÇIK
    max_packages_to_expand=500,        # İlk 500 paket için dependent çek
    max_dependents_per_package=20,     # Her paket için max 20 dependent
    results_dir="../results"
)
```

### Genişletme Adımları:

1. **Aşama 1:** Top N paketlerin dependencies'ini ekle (normal)
   ```
   react → [react-dom, prop-types, ...]
   lodash → []
   ```

2. **Aşama 2:** İlk `max_packages_to_expand` paket için dependents çek
   ```
   Libraries.io API: "react'i kim kullanıyor?"
   → [gatsby, next, create-react-app, ...]
   ```

3. **Aşama 3:** Bu dependent paketleri graph'e node olarak ekle
   ```
   gatsby → react (kenar ekle)
   next → react (kenar ekle)
   ```

4. **Aşama 4:** Dependent paketlerin dependencies'ini çek
   ```
   gatsby → [react, webpack, babel, ...]
   next → [react, styled-jsx, ...]
   ```

### Neden Sınırlama Var?

- **Libraries.io rate limit:** ~60 istek/dakika
- **2000 paket × 50 dependent** = 100K API çağrısı = **28+ saat!** 😱
- **Çözüm:** `max_packages_to_expand` ve `max_dependents_per_package` ile kontrol

### Önerilen Ayarlar (depth vs expand_with_dependents):

#### 🚀 Standart Analiz (depth parametresi - Önerilen)

| Senaryo | top_n | depth | Süre | Düğüm | Kenar | Açıklama |
|---------|-------|-------|------|-------|-------|----------|
| **Test** | 100 | 1 | 1 dk | ~500-800 | ~1K-2K | Hızlı test |
| **Küçük** | 500 | 1 | 2 dk | ~2K-3K | ~5K-8K | Temel analiz |
| **Orta** | 1000 | 1 | 3-5 dk | ~3K-5K | ~8K-12K | **Önerilen** |
| **Derin** | 1000 | 2 | 8-15 dk | ~8K-15K | ~25K-40K | İleri analiz |
| **Max Seed** | 2000 | 1 | 5-8 dk | ~6K-10K | ~15K-25K | ecosyste.ms max |
| ⚠️ **Patlama** | 1000 | 7 | 1-2 saat | ~50K-100K | ~200K+ | **Önerilmez!** |

#### 🔬 Dependent Genişletme (expand_with_dependents - Özel)

| Senaryo | top_n | max_expand | max_deps | Süre | Düğüm | Açıklama |
|---------|-------|------------|----------|------|-------|----------|
| **Test** | 100 | 50 | 10 | 5-10 dk | ~800-1200 | Dependent test |
| **Küçük** | 500 | 200 | 15 | 20-30 dk | ~3K-6K | Dependent analiz |
| **Orta** | 1000 | 500 | 20 | 1-1.5 saat | ~8K-15K | Dependent haritası |
| **Büyük** | 2000 | 1000 | 20 | 2-3 saat | ~15K-30K | Tam dependent ağ |

⚠️ **ÖNEMLİ:** 
- **ecosyste.ms limiti (2000):** Sadece **Kademe 0** (başlangıç seed listesi) için!
- **NPM Registry:** Kademe 1, 2, 3... için **sınırsız** bağımlılık çekebilir
- **depth parametresi:** Sınırsız kademe çeker, ama exponansiyel büyüme nedeniyle depth>2 önerilmez
- **expand_with_dependents:** Libraries.io rate limit nedeniyle yavaş, özel kullanım için

## 📦 Çıktılar

Tüm dosyalar `results/` dizinine yazılır.

### 🎯 Ana Çıktı Dosyaları

#### 1. Gephi Görselleştirme (Otomatik Üretilir) ⭐
- **`gephi_edges.csv`** — ID bazlı kenar listesi (Source, Target, Type, Weight)
- **`gephi_nodes.csv`** — ID bazlı düğüm listesi (Id, Label, metrikler)
- **Kullanım:** Gephi → Import spreadsheet (detay: `GEPHI_GUIDE.md`)

#### 2. Ham Veri Dosyaları
- **`edges.csv`** — Kenar listesi (source=dependent, target=dependency)
  ```csv
  source,target
  react-dom,react
  gatsby,react
  webpack,lodash
  ```

- **`metrics.csv`** — Tüm paketler için metrikler
  ```csv
  package,in_degree,out_degree,betweenness,is_topN
  react,823,0,0.156234,True
  lodash,1247,0,0.234567,True
  ```

- **`risk_scores.csv`** — Bileşik risk skorları
  ```csv
  package,risk_score,in_degree,out_degree,betweenness,is_topN
  react,0.892341,823,0,0.156234,True
  ```

- **`graph_stats.json`** — Genel ağ istatistikleri
  ```json
  {
    "nodes": 4523,
    "edges": 12847,
    "avg_degree": 5.67,
    "density": 0.00062
  }
  ```

- **`cache_deps.json`** — Bağımlılık önbelleği (tekrar sorguları önler)

#### 3. Analiz Çıktıları
- **`edge_betweenness_top10.csv`** — En yüksek köprü kenarlar
- **`cascade_impact_top20.csv`** — Ters yön (dependents) kaskad etkisi
- **`metrics_top20_*.tex`** — LaTeX tabloları (in_degree, out_degree, betweenness)
- **`risk_scores_top20.tex`** — En riskli 20 paket tablosu

#### 4. Görselleştirmeler (PNG + SVG)
```
results/plots/
├── in_degree_distribution.png
├── out_degree_distribution.png
├── betweenness_distribution.png
├── risk_score_distribution.png
├── in_out_degree_scatter.png
├── degree_betweenness_scatter.png
├── top10_in_degree.png
├── top10_out_degree.png
├── top20_risk_scores.png
└── *.svg (vektör versiyonları)
```

## 🔬 Yöntem Detayları

### 1. Veri Toplama

#### Top N Paket Listesi
```python
# analysis_helpers.py: fetch_top_packages()
def fetch_top_packages(limit: int = 100) -> List[str]:
    # 1. Öncelik: ecosyste.ms (per_page=1000, sayfalama)
    # 2. Yedek: npm search aggregate (multi-seed)
    # 3. Son yedek: npms.io (popularity score)
```

**ecosyste.ms API Çağrısı:**
```http
GET https://packages.ecosyste.ms/api/v1/registries/npmjs.org/package_names
    ?per_page=1000
    &sort=downloads
    &page=1
```

#### Bağımlılık Çekme
```python
# analysis_helpers.py: fetch_dependencies()
def fetch_dependencies(package: str) -> Dict[str, str]:
    # NPM registry'den latest version bağımlılıkları
    # Önbellek ile tekrar sorguları önle
    # 3 deneme, başarısız olursa boş dict
```

**NPM Registry API:**
```http
GET https://registry.npmjs.org/{package}
Response: {
  "dist-tags": {"latest": "18.2.0"},
  "versions": {
    "18.2.0": {
      "dependencies": {
        "loose-envify": "^1.1.0",
        "scheduler": "^0.23.0"
      }
    }
  }
}
```

#### Dependent Çekme (Genişletme Modu)
```python
# analysis_helpers.py: fetch_dependents()
def fetch_dependents(package: str, max_dependents: int = 100) -> List[str]:
    # Libraries.io API ile sayfalama
    # Her sayfa 30 paket, max_dependents'a kadar
```

**Libraries.io API:**
```http
GET https://libraries.io/api/npm/{package}/dependents
    ?page=1
    &per_page=30
Response: [
  {"name": "react-dom", "platform": "npm", ...},
  {"name": "gatsby", "platform": "npm", ...}
]
```

### 2. Ağ Kurma (Graph Construction)

```python
# analysis_helpers.py: build_dependency_graph()
G = nx.DiGraph()  # Yönlü graf

# Kenar yönü: Dependent → Dependency
# Örnek: react-dom → react (react-dom, react'e bağımlı)
for pkg in top_packages:
    deps = fetch_dependencies(pkg)
    for dep in deps:
        G.add_edge(pkg, dep)  # Yönlü kenar

# Genişletme modu aktifse:
if expand_with_dependents:
    for pkg in top_packages[:max_packages_to_expand]:
        dependents = fetch_dependents(pkg, max_dependents_per_package)
        for dep_pkg in dependents:
            G.add_edge(dep_pkg, pkg)  # Dependent → Top Package
            # Dependent'ın dependencies'ini de ekle
            deps = fetch_dependencies(dep_pkg)
            for dep in deps:
                G.add_edge(dep_pkg, dep)
```

**Graf Özellikleri:**
- **Tip:** NetworkX DiGraph (yönlü)
- **Düğümler:** Paket adları (string)
- **Kenarlar:** Dependent → Dependency
- **Ağırlık:** Yok (unweighted)

### 3. Metrik Hesaplama

#### In-Degree (Gelen Derece)
```python
in_deg = dict(G.in_degree())
# Bir pakete kaç paket bağımlı?
# Örnek: react → 823 (823 paket react kullanıyor)
```

#### Out-Degree (Giden Derece)
```python
out_deg = dict(G.out_degree())
# Bir paket kaç pakete bağımlı?
# Örnek: webpack → 12 (webpack 12 pakete bağımlı)
```

#### Betweenness Centrality (Arasındalık Merkezi)
```python
# Tam hesaplama (küçük graflar < 1000 düğüm)
btw = nx.betweenness_centrality(G, normalized=True)

# Örneklemeli (büyük graflar > 1000 düğüm)
btw = nx.betweenness_centrality(G, k=sample_k, seed=42, normalized=True)
```

**Betweenness Formülü:**
$$
C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}
$$
- $\sigma_{st}$: s'den t'ye en kısa yol sayısı
- $\sigma_{st}(v)$: v'den geçen en kısa yol sayısı

**Yorumlama:**
- Yüksek betweenness = Ağın "köprüsü"
- Paketi kaldırınca çok yol kesilir
- Kritik altyapı bileşeni

### 4. Normalizasyon (Min-Max)

```python
def minmax_normalize(values: Dict[str, float]) -> Dict[str, float]:
    vals = list(values.values())
    vmin, vmax = min(vals), max(vals)
    
    if vmax == vmin:  # Tüm değerler aynı
        return {k: 0.0 for k in values}
    
    return {
        k: (v - vmin) / (vmax - vmin)
        for k, v in values.items()
    }
```

**Sonuç:** Her metrik [0, 1] aralığına ölçeklenir.

### 5. Risk Skoru Hesaplama

```python
# analysis_helpers.py: compute_risk_scores()
ALPHA = 0.5   # In-degree ağırlığı
BETA = 0.2    # Out-degree ağırlığı
GAMMA = 0.3   # Betweenness ağırlığı

risk[pkg] = (
    ALPHA * in_norm[pkg] +
    BETA * out_norm[pkg] +
    GAMMA * btw_norm[pkg]
)
```

**Risk Skoru Formülü:**
$$
\text{Risk}(p) = 0.5 \cdot \text{InDeg}'(p) + 0.2 \cdot \text{OutDeg}'(p) + 0.3 \cdot \text{Betw}'(p)
$$

**Yorumlama:**
- **Yüksek in-degree** (0.5): Çok paket buna bağımlı → Kritik
- **Yüksek out-degree** (0.2): Çok bağımlılığı var → Kararsız
- **Yüksek betweenness** (0.3): Ağın köprüsü → Kaldırılırsa sistem parçalanır

### 6. Kaskad Etki Analizi

```python
# analysis_helpers.py: estimate_cascade_impact()
def estimate_cascade_impact(G: nx.DiGraph, seed_nodes: List[str]) -> Dict[str, int]:
    """Bir paket kaldırılırsa kaç düğüme ulaşılamaz?"""
    G_rev = G.reverse()  # Kenarları ters çevir
    
    for seed in seed_nodes:
        # BFS ile seed'den ulaşılabilenleri say
        reachable = nx.single_source_shortest_path_length(G_rev, seed)
        impact[seed] = len(reachable) - 1  # Kendisi hariç
```

**Yorumlama:**
- Paket kaldırılınca kaç dependent etkilenir?
- Yüksek impact = Büyük kaskad riski

## 🎨 Görselleştirme

## 🎨 Görselleştirme

### Matplotlib Grafikleri (Otomatik Üretilir)

```python
# analysis_helpers.py: plot_distributions(), plot_scatter(), plot_top_packages()
```

**Üretilen Grafikler:**
1. **Dağılım Grafikleri:** In-degree, out-degree, betweenness, risk histogramları
2. **Saçılım Grafikleri:** In-out degree, degree-betweenness korelasyonları
3. **Top Paketler:** En yüksek in-degree, out-degree bar charts
4. **Risk Haritası:** En riskli 20 paket

### Gephi Görselleştirme (Ağ Haritası)

**Detaylı kılavuz:** [`GEPHI_GUIDE.md`](GEPHI_GUIDE.md)

```python
# Notebook'ta otomatik üretilir
result = run_pipeline(top_n=1000)
# → results/gephi_edges.csv ⭐
# → results/gephi_nodes.csv
```

**Gephi'de Açma:**
1. File → Import spreadsheet → `gephi_edges.csv` (Edges table, Directed)
2. File → Import spreadsheet → `gephi_nodes.csv` (Nodes table, Append)
3. Layout → Force Atlas 2
4. Ranking → `risk_score` (renk/boyut)

## 💡 İpuçları ve Optimizasyon

### Büyük Graflar için
- **Betweenness örnekleme:** `sample_k=200` (1000+ düğüm için)
- **Genişletme limiti:** `max_packages_to_expand=500` (rate limit için)
- **Plot devre dışı:** `compute_plots=False` (daha hızlı)

### Önbellek Yönetimi
```python
# Önbelleği temizle (yeni veri çekmek için)
import os
os.remove("results/cache_deps.json")
```

### API Kota Sorunları
- **ecosyste.ms:** Kota yok, ama rate limit var → Yavaşlat
- **Libraries.io:** ~60/dakika → `max_dependents_per_package` düşür
- **NPM registry:** Çok toleranslı, ama 3 deneme koy

### Tekrarlanabilirlik
```python
# Rastgele tohum sabit
np.random.seed(42)
nx.betweenness_centrality(G, k=200, seed=42)
```

## 🔧 Modül Yapısı

```
analysis/
├── analysis.ipynb              # Ana notebook (tek giriş noktası)
├── run_pipeline.py             # Orchestrator (tek fonksiyon: run_pipeline)
├── analysis_helpers.py         # Core fonksiyonlar
│   ├── fetch_top_packages()    # Top N listesi çek
│   ├── fetch_dependencies()    # Dependencies çek
│   ├── fetch_dependents()      # Dependents çek (genişletme)
│   ├── build_dependency_graph()# Graf kur
│   ├── compute_metrics()       # Metrikler hesapla
│   ├── compute_risk_scores()   # Risk skorları
│   ├── estimate_cascade_impact() # Kaskad analizi
│   ├── plot_*()                # Görselleştirmeler
│   └── save_*()                # Dosya yazma
├── exporter.py                 # Gephi export
│   ├── export_gephi_from_graph() # NetworkX → Gephi CSV
│   └── write_nodes(), write_edges_csv()
├── make_tables.py              # LaTeX tablo üreticileri
├── GEPHI_GUIDE.md              # Gephi kullanım kılavuzu
├── requirements.txt            # Python bağımlılıkları
└── Readme.md                   # Bu dosya
```

## 📚 Teorik Arka Plan

### Kompleks Ağ Teorisi
- **Düğüm (Node):** Paket
- **Kenar (Edge):** Bağımlılık ilişkisi (yönlü)
- **Derece (Degree):** Bağlantı sayısı
- **Merkeziyet (Centrality):** Ağdaki önem

### Metrik Seçimi Gerekçeleri

#### 1. In-Degree (Ağırlık: 0.5)
**Neden önemli?**
- Çok pakete hizmet eden paketler kritik altyapı
- Tek başarısızlık noktası (single point of failure)
- Örnek: lodash, react (yüzlerce pakete bağımlı)

#### 2. Betweenness (Ağırlık: 0.3)
**Neden önemli?**
- Ağın köprüsü olan paketler
- Kaldırılınca graf parçalanır
- Transitif bağımlılık riski

#### 3. Out-Degree (Ağırlık: 0.2)
**Neden daha düşük?**
- Çok bağımlılık = Kararsızlık
- Ama direkt etki daha düşük
- Örnek: webpack (12 bağımlılık ama kritik değil)

### Literatür Referansları
Detaylı akademik bağlam için:
- `../academic/topolojik-risk-degerlendirmesi.md`
- `../academic/literature.md`
- `../references/Readme.md`

## 🚨 Sınırlamalar ve Gelecek Çalışmalar

### Mevcut Sınırlamalar
1. **Veri kaynağı:** ecosyste.ms max 2000 paket (npmleaderboard limiti)
2. **Rate limit:** Libraries.io ~60/dakika → Genişletme yavaş
3. **Statik analiz:** Zamanla değişimi göz ardı eder
4. **Sürüm:** Sadece latest version (eski sürümleri yok sayar)

### Gelecek İyileştirmeler
- [ ] Zamansal analiz (temporal network)
- [ ] Sürüm bazlı risk skoru
- [ ] Güvenlik açığı entegrasyonu (CVE database)
- [ ] Alternatif veri kaynakları (npm downloads API)
- [ ] Paralel API çağrıları (async)
- [ ] Grafik veritabanı (Neo4j) entegrasyonu

## 📞 Destek ve Katkı

**Sorun bildirimi:** GitHub Issues
**Dokümantasyon:** Bu README + `GEPHI_GUIDE.md` + akademik raporlar
**Kod stili:** Black formatter, type hints

---

## 📖 Hızlı Referans

### Tek Komutla Çalıştırma
```python
from analysis.run_pipeline import run_pipeline
result = run_pipeline(top_n=1000)
```

### Genişletme ile Çalıştırma
```python
result = run_pipeline(
    top_n=2000,
    expand_with_dependents=True,
    max_packages_to_expand=500,
    max_dependents_per_package=20
)
```

### Çıktı Dosyaları
```
results/
├── gephi_edges.csv       ⭐ Ana çıktı (Gephi)
├── gephi_nodes.csv       ⭐ Metriklerle
├── edges.csv             Ham kenar listesi
├── metrics.csv           Tüm metrikler
├── risk_scores.csv       Risk skorları
├── graph_stats.json      Genel istatistikler
└── plots/                Görselleştirmeler
```

### Önemli Parametreler
- `top_n`: Kaç paket (max 2000)
- `expand_with_dependents`: Genişletme modu (bool)
- `max_packages_to_expand`: İlk kaç paket için dependent çek
- `max_dependents_per_package`: Her paket için max dependent
- `sample_k`: Betweenness örnekleme (>1000 düğüm için)
- `compute_plots`: Görselleştirmeleri üret (bool)

---

**NOT:** CLI kullanımı artık desteklenmiyor. Tüm işlemler Jupyter Notebook içinden yapılmalıdır.
# 🎨 Gephi Kullanım Kılavuzu

## 📦 Otomatik Üretilen Dosyalar

**Jupyter Notebook'tan tek tıkla üretilir!**

Notebook'u açın ve ilk kod hücresini çalıştırın:
```python
from analysis.run_pipeline import run_pipeline
result = run_pipeline(top_n=1000)
```

`results/` dizininde otomatik olarak oluşturulur:

### ✅ Ana Çıktılar (Gephi için hazır)

1. **`gephi_nodes.csv`** - Düğüm listesi
   - `Id` - Numerik ID (deterministik, alfabetik sıralı)
   - `Label` - Paket adı (görünür etiket)
   - `package` - Paket adı (yedek)
   - `in_degree` - Kaç paket buna bağımlı
   - `out_degree` - Kaç bağımlılığı var
   - `betweenness` - Ağ köprü skoru
   - `risk_score` - Bileşik risk değeri
   - `is_topN` - Top N'de mi?

2. **`gephi_edges.csv`** - Kenar listesi ⭐ **ANA ÇIKTI**
   - `Source` - Kaynak düğüm ID'si
   - `Target` - Hedef düğüm ID'si
   - `Type` - "Directed" (yönlü)
   - `Weight` - 1 (varsayılan ağırlık)

### 📌 Kenar Yönü
```
Dependent → Dependency
(Kullanan) → (Kullanılan)
```

Örnek: Eğer `react-dom` paketi `react`'e bağımlıysa:
```csv
Source,Target,Type,Weight
1234,5678,Directed,1
```
Burada 1234=react-dom, 5678=react ID'leridir.

## 🚀 Gephi'de Kullanım

### 1️⃣ Import Adımları

1. **Gephi'yi aç** (https://gephi.org/)
2. **File → Import spreadsheet**
3. **`gephi_edges.csv` seç** ✅
4. Import as: **Edges table**
5. ✅ Directed graph olarak işaretle
6. Import

7. **File → Import spreadsheet** (tekrar)
8. **`gephi_nodes.csv` seç**
9. Import as: **Nodes table**
10. Append to existing workspace

### 2️⃣ Görselleştirme Önerileri

#### Layout Algoritmaları:
- **Force Atlas 2** - Ağ yapısını görmek için ideal
  - Scaling: 2.0
  - Gravity: 1.0
  - DissuadeHubs: ✅
  
- **Fruchterman Reingold** - Simetrik görünüm
- **OpenORD** - Büyük graflar için

#### Düğüm Boyutları:
- **Ranking** → `in_degree` → Min: 10, Max: 100
- Veya `risk_score` kullan

#### Renkler:
- **Partition** → `is_topN` 
  - True: Turuncu/Kırmızı (Top paketler)
  - False: Mavi (Bağımlılıklar)

#### Kenarlar:
- Opaklık: %30-50
- Genişlik: Sabit veya `Weight` bazlı

### 3️⃣ İstatistikler (Statistics Panel)

Çalıştırmadan önce mevcut:
- ✅ In-Degree (zaten var)
- ✅ Out-Degree (zaten var)
- ✅ Betweenness Centrality (zaten var)

Ek olarak hesaplayabilirsiniz:
- PageRank - Etki analizi
- Modularity - Topluluk tespiti
- Connected Components - Bağlı bileşenler

### 4️⃣ Filtreleme

**Filters** panelinden:
- `in_degree > 10` - Popüler paketleri göster
- `risk_score > 0.5` - Yüksek riskli düğümler
- `is_topN = True` - Sadece Top N kohort

## 📊 Örnek Analiz Senaryoları

### Senaryo 1: En Kritik Paketleri Bul
1. Statistics → Betweenness Centrality (hesapla)
2. Ranking → Betweenness → Düğüm boyutu
3. Layout → Force Atlas 2
4. **Sonuç:** Merkezdeki büyük düğümler en kritik paketler

### Senaryo 2: Risk Odaklı Harita
1. Ranking → `risk_score` → Düğüm rengi (kırmızı gradyan)
2. Filter → `risk_score > 0.7`
3. Layout → Fruchterman Reingold
4. **Sonuç:** Kırmızı düğümler en riskli paketler

### Senaryo 3: Top N Bağımlılık Analizi
1. Partition → `is_topN`
2. Filter → `is_topN = True`
3. Layout → OpenORD
4. **Sonuç:** Top paketlerin iç bağımlılık ağı

### Senaryo 4: Hub Paketleri
1. Ranking → `in_degree` → Düğüm boyutu
2. Filter → `in_degree > 20`
3. **Sonuç:** Çok sayıda pakete hizmet eden "hub" paketler

## 🔧 Notebook'tan Üretim

**Önerilen Yöntem:** Tüm işlemler Jupyter Notebook içinden yapılır.

```python
# Notebook'ta bu hücreyi çalıştırın:
from analysis.run_pipeline import run_pipeline

# Tam pipeline (Gephi dosyaları otomatik üretilir)
result = run_pipeline(
    top_n=1000,              # Top 1000 paket
    results_dir="../results", # Çıktı klasörü
    compute_plots=True,       # Grafikleri de üret
    export_gexf=False         # GEXF formatı (opsiyonel)
)

# Sonuç:
# ✓ results/gephi_nodes.csv
# ✓ results/gephi_edges.csv  ← ANA ÇIKTI
```

**NOT:** Artık CLI kullanımı yok - tüm kontrol Jupyter Notebook'ta.

## 📁 Dosya Formatı Detayları

### gephi_edges.csv örnek:
```csv
Source,Target,Type,Weight
1,523,Directed,1
1,847,Directed,1
2,523,Directed,1
3,12,Directed,1
```

### gephi_nodes.csv örnek:
```csv
Id,Label,package,in_degree,out_degree,betweenness,risk_score,is_topN
1,react,react,823,0,0.156234,0.892341,True
2,react-dom,react-dom,421,2,0.089432,0.673221,True
523,lodash,lodash,1247,0,0.234567,0.956789,True
```

## 💡 İpuçları

- **ID'ler deterministik:** Aynı paket her zaman aynı ID'yi alır (alfabetik sıralı)
- **CSV formatı:** Excel/LibreOffice ile de açılabilir
- **Büyük graflar:** 1000+ düğüm için OpenORD layout kullanın
- **Export:** Gephi'den PNG/PDF/SVG export edebilirsiniz
- **GEXF alternatifi:** `export_gexf=True` ile XML format da üretilebilir

## 🎯 Sonuç

Bu pipeline sayesinde:
1. ✅ Tek komutla Gephi-ready dosyalar
2. ✅ ID bazlı edge CSV (ana çıktı)
3. ✅ Zengin metrik verileri
4. ✅ Risk skorları dahil
5. ✅ Deterministik ve tekrarlanabilir

**Gephi'de açmak için sadece `gephi_edges.csv` ve `gephi_nodes.csv` yeterli!**
