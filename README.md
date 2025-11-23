# Yazılım Tedarik Zincirinde Kritiklik Haritalaması: NPM Ekosisteminde Topolojik Risk Analizi

Bu proje, NPM ekosistemindeki paketleri yönlü bir ağ olarak modelleyip merkeziyet metrikleriyle yapısal riski ölçer. Amaç, klasik zafiyet skorlarının ötesine geçerek bir paketin ağ içindeki konumundan doğan sistemik riski görünür kılmaktır.

Canlı önizleme: https://yusufarbc.github.io/npm-complex-network-analysis/

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

result = run_pipeline(
    top_n=1000,              # Kaç paket analiz edilecek
    results_dir="../results", # Çıktı klasörü
    compute_plots=True,       # Görselleştirmeler
    export_gexf=False         # GEXF format (opsiyonel)
)
```

### 🔄 Ağ Genişletme Modu (Dependent Paketler)

**Varsayılan:** Sadece Top N paketlerin dependencies'leri eklenir.

**Genişletme ile:** Top N'e bağımlı olan (dependent) paketler de network'e dahil edilir:

```python
result = run_pipeline(
    top_n=2000,                         # Top 2K paket (max limit)
    expand_with_dependents=True,        # 🆕 Dependent paketleri de ekle
    max_packages_to_expand=500,         # İlk 500 paket için dependent çek
    max_dependents_per_package=20,      # Her paket için max 20 dependent
    results_dir="../results"
)
```

**Ne değişir:**
- Top N → Dependencies (normal)
- **+** Top N'e bağımlı olanlar (dependents) → node olarak eklenir
- **+** Bu dependent paketlerin dependencies'i de çekilir

**Sonuç:** Ağ çok daha büyük olur (örn. Top 2K + genişletme → ~15K-30K düğüm)

⚠️ **Önemli Limitler:**
- **ecosyste.ms / npmleaderboard:** Max **2000** paket sağlar (`top_n` üst limit)
- **Libraries.io API:** Rate limit var (~60/dakika)
- **Öneri:** `max_packages_to_expand=500-1000`, `max_dependents_per_package=20`

**Bu tek hücre tüm pipeline'ı çalıştırır:**
1. ✅ Top N paket listesini çeker (max 2000 - ecosyste.ms limiti)
2. ✅ Bağımlılık grafını oluşturur
3. ✅ Metrikleri hesaplar
4. ✅ **Gephi dosyalarını otomatik üretir**
5. ✅ Görselleştirmeleri yapar
6. ✅ Raporları oluşturur

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

**Detaylı kılavuz:** [`analysis/GEPHI_GUIDE.md`](analysis/GEPHI_GUIDE.md)
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
