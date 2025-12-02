# Metodoloji: Topolojik Risk Analizi ve BRS Modeli

Bu belge, NPM tedarik zinciri ağının nasıl modellendiğini, kullanılan merkeziyet metriklerini ve **Bileşik Risk Skoru (BRS)** hesaplama yöntemini detaylandırır.

## 1. Veri Toplama ve Ağ Modellemesi

Proje, NPM ekosistemini yönlü bir graf (directed graph) olarak modeller:
- **Düğümler (Nodes):** NPM paketleri.
- **Kenarlar (Edges):** Paketler arası bağımlılıklar (dependency).

### Örneklem Stratejisi
Tüm NPM ekosistemini (3M+ paket) analiz etmek yerine, sistemik etkiyi merkeze alan bir örneklem stratejisi izlenmiştir:
1.  **Başlangıç Kümesi (Seed):** `ecosyste.ms` verilerine göre en çok bağımlıya (*dependents*) sahip ilk 1.000 paket.
2.  **Derinlik Taraması:** Bu paketlerin bağımlılık ağacı 7. derinlik seviyesine kadar taranmıştır.
3.  **Ön İşleme:** Döngüsel referanslar (circular dependencies) temizlenmiş ve izole düğümler ayıklanmıştır.

Sonuç olarak, yaklaşık **1.506 düğüm** ve **3.058 kenardan** oluşan, ekosistemin omurgasını temsil eden bir ağ elde edilmiştir.

## 2. Merkeziyet Metrikleri

Paketlerin ağ içindeki önemini belirlemek için üç temel metrik kullanılmıştır:

| Metrik | Tanım | Risk Bağlamındaki Anlamı |
| :--- | :--- | :--- |
| **In-Degree** | Bir pakete doğrudan bağımlı olan paket sayısı. | **Popülarite ve Etki Alanı:** Bir zafiyet durumunda kaç projenin doğrudan etkileneceğini gösterir. |
| **Out-Degree** | Bir paketin bağımlı olduğu dış paket sayısı. | **Saldırı Yüzeyi:** Paketin dışarıdan gelebilecek tehditlere ne kadar açık olduğunu gösterir. |
| **Betweenness** | Paketin, ağdaki diğer düğümler arasındaki en kısa yollar üzerinde bulunma sıklığı. | **Köprü Rolü:** Paketin ağ trafiğini kontrol etme ve riski yayma potansiyelini (stratejik konumunu) gösterir. |

## 3. Bileşik Risk Skoru (BRS)

Tek bir metrik, karmaşık tedarik zinciri risklerini ifade etmekte yetersiz kalır. Bu nedenle, metriklerin ağırlıklı kombinasyonu ile **Bileşik Risk Skoru (Composite Risk Score)** geliştirilmiştir.

### Normalizasyon
Her metrik, hesaplamaya girmeden önce Min-Max yöntemiyle $[0,1]$ aralığına normalize edilir:

$$ x' = \frac{x - \min(x)}{\max(x) - \min(x)} $$

### Formül
$$ \text{BRS} = 0.5 \cdot \text{In-Degree}' + 0.2 \cdot \text{Out-Degree}' + 0.3 \cdot \text{Betweenness}' $$

### Ağırlıkların Mantığı
*   **In-Degree ($0.5$):** En yüksek ağırlık. Tedarik zinciri saldırılarında "etki alanı" (impact radius), en kritik risk faktörüdür.
*   **Betweenness ($0.3$):** İkinci faktör. Popüler olmasa bile ağın akışını kontrol eden "köprü" paketleri yakalamak için kritiktir.
*   **Out-Degree ($0.2$):** Saldırı yüzeyini temsil eder.

## 4. Sağlamlık ve Kaskad Analizi

Modelin geçerliliği, **hedefli saldırı simülasyonları** ile test edilmiştir:
*   Yüksek BRS skoruna sahip paketler sırasıyla ağdan çıkarılır.
*   Her adımda ağın **En Büyük Bağlı Bileşen (Largest Connected Component - LCC)** boyutu ve erişilebilirliği ölçülür.
*   Sonuçlar, BRS skorunun sistemik çöküşü tahmin etmede başarılı olduğunu göstermektedir.
