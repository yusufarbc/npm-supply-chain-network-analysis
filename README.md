# NPM Complex Network Analysis

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
- `analysis/analysis.ipynb` dosyasını açın, hücreleri sırayla çalıştırın; tüm çıktılar `results/` içine yazılır.

## Üretilen Çıktılar
- `results/edges.csv` — Kenar listesi (source=dependent, target=dependency)
- `results/metrics.csv` — `package,in_degree,out_degree,betweenness,is_topN`
- `results/risk_scores.csv` — Bileşik risk skoru + metrikler
- `results/graph_stats.json` — Genel ağ istatistikleri
- `results/edge_betweenness_top10.csv` — En yüksek köprü kenarlar
- `results/cascade_impact_top20.csv` — Ters yön (dependents) kaskad etkisi
- `results/classification.csv` — (ops.) Low/Medium/High risk sınıfları
- Görseller (PNG+SVG): histogramlar, saçılımlar, top10, top20 risk, (ops.) ağ görselleri
- Tablolar: `*.tex` (bkz. `analysis/make_tables.py`)

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

## Gephi Dışa Aktarım

Bu repodaki `results/` dizininden Gephi ile açılabilecek dosyalar üretebilirsiniz. Her paket için deterministik bir `id` atanır.

- Komut:
```
python analysis/export_for_gephi.py --results results
```
- Çıktılar (`results/`):
	- `gephi_nodes.csv` — `id,label,package,in_degree,out_degree,betweenness,risk_score,is_topN`
	- `gephi_edges.csv` — `source,target,weight,directed` (source/target = id)
	- Opsiyonel `graph.gexf` — `--gexf` ile oluşturulur (networkx mevcutsa)

Gephi'de CSV'yi açarken `gephi_nodes.csv`'i Nodes olarak, `gephi_edges.csv`'i Edges olarak içe aktarın; `id` alanı node id olarak kullanılmalıdır.
