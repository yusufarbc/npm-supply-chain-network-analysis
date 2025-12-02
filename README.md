# NPM Tedarik Zinciri Ağ Analizi ve Kritiklik Haritalaması


> **NPM ekosistemindeki sistemik risklerin, paket içeriğinden bağımsız topolojik analiz yöntemleriyle haritalandırılması.**

Bu proje, NPM paketleri arasındaki bağımlılık ilişkilerini yönlü bir ağ (directed graph) olarak modeller ve **Bileşik Risk Skoru (BRS)** ile yapısal riski ölçer. Amaç, klasik zafiyet taramalarının (CVE) ötesine geçerek, bir paketin ağ içindeki *konumundan* kaynaklanan sistemik tehditleri görünür kılmaktır.

🔗 **Canlı Önizleme:** [yusufarbc.github.io/npm-supply-chain-network-analysis](https://yusufarbc.github.io/npm-supply-chain-network-analysis/)

---

## 💡 Öne Çıkan Bulgular

Bu çalışma, NPM ekosisteminin topolojik yapısına dair kritik içgörüler sunmaktadır:

*   **Sistemik Kırılganlık:** Ağın %1'inden azını oluşturan "köprü" paketlerin (yüksek betweenness) çökmesi, ekosistemin %40'ından fazlasının erişilebilirliğini tehdit etmektedir.
*   **Gizli Riskler:** Popüler olmayan ancak kritik paketlere (low popularity, high centrality) yapılan saldırılar, tespit edilmesi en zor ve etkisi en yıkıcı olanlardır.
*   **Shai-Hulud Doğrulaması:** Geliştirilen BRS modeli, Shai-Hulud saldırısında hedef alınan paketlerin %85'ini "Yüksek Riskli" olarak sınıflandırmayı başarmıştır.

---

## 📚 Dokümantasyon ve Arka Plan

Projenin teorik zemini ve vaka analizleri için aşağıdaki belgeleri inceleyebilirsiniz:

*   **[🛡️ NPM Güvenlik Manzarası](npm_security_landscape.md):** Ekosistemdeki aktif tehditler (Typosquatting, Dependency Confusion vb.) ve neden topolojik analize ihtiyaç duyulduğu.
*   **[🐛 Vaka Analizi: Shai-Hulud](shai_hulud_incident.md):** Kendi kendini yayan (wormable) ilk büyük ölçekli NPM saldırısının teknik analizi ve projenin bu tür saldırıları nasıl öngörebileceği.
*   **[📚 Literatür Taraması](literature.md):** Akademik çalışmalar, boşluk analizi ve projenin literatürdeki konumu.
*   **[📐 Metodoloji ve BRS Modeli](methodology.md):** Ağ modellemesi, kullanılan merkeziyet metrikleri (In-Degree, Betweenness) ve risk skorunun matematiksel formülü.

---

## 🚀 Hızlı Başlangıç

### Önkoşullar
*   Python 3.11.x (Önerilen: 3.11.9)

### Kurulum

1.  **Depoyu klonlayın ve dizine gidin:**
    ```powershell
    git clone https://github.com/yusufarbc/npm-supply-chain-network-analysis.git
    cd npm-supply-chain-network-analysis
    ```

2.  **Sanal ortamı kurun ve etkinleştirin (Windows PowerShell):**
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3.  **Bağımlılıkları yükleyin:**
    ```powershell
    pip install -r analysis/requirements.txt
    python -m pip install notebook
    ```

4.  **Analizi başlatın:**
    ```powershell
    python -m notebook
    # analysis/analysis.ipynb dosyasını açın
    ```

---

## 📊 Kullanım (Pipeline)

Analiz motoru `analysis/run_pipeline.py` üzerinden çalışır. Notebook içerisindeki **ilk hücreyi** çalıştırarak tam analizi gerçekleştirebilirsiniz.

```python
from analysis.run_pipeline import run_pipeline

# Varsayılan: En kritik altyapı paketleri (Top 1000 Dependents + 7 Derinlik)
result = run_pipeline(
    top_n=1000,                    # Analiz edilecek paket sayısı
    leaderboard_mode="dependents",  # Mod: dependents, downloads, trending
    depth=7,                        # Tarama derinliği
    results_dir="../results",      # Çıktı dizini
    compute_plots=True              # Grafikleri oluştur
)
```

### Analiz Modları

| Mod | Parametre | Açıklama | Kullanım Senaryosu |
|-----|-----------|----------|---------------------|
| **Most Dependent** | `dependents` | En çok bağımlı olunan paketler | **Kritik Altyapı Analizi (Varsayılan)** |
| **Most Downloaded**| `downloads` | En çok indirilen paketler | Genel popülarite ve trafik analizi |
| **Trending** | `trending` | Hızla yükselen paketler | Erken uyarı ve anomali tespiti |

---

## 📂 Proje Yapısı

*   `academic/`: Akademik bildiri ve LaTeX kaynak dosyaları.
*   `analysis/`: Python analiz kodları, veri çekme ve işleme modülleri.
*   `results/`: Analiz çıktıları (CSV, JSON, GEXF) ve oluşturulan grafikler.
*   `media/`: Proje görselleri.

---

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.
