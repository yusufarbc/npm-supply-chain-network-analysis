# 📘 **KARMAŞIK AĞ ANALİZİ — TAM DERS NOTU**

---

## 🔹 1. GİRİŞ: AĞ BİLİMİ VE KAVRAMSAL TEMELLER

**Ağ bilimi (Network Science)**, karmaşık sistemlerdeki bileşenlerin ve etkileşimlerinin yapısını anlamaya çalışan disiplinler arası bir alandır.
Ağlar, **düğümler (nodes)** ve **bağlantılardan (edges)** oluşur.
Bu yapı; sosyal medya, biyoloji, ekonomi, internet gibi birçok alanda kullanılır.

📘 **Örnek:**

* Facebook’ta düğümler kullanıcılar, bağlantılar arkadaşlıklardır.
* Protein etkileşim ağlarında düğümler proteinler, bağlantılar etkileşimlerdir.

---

## 🔹 2. KARMAŞIK SİSTEMLER VE SİSTEM DÜŞÜNCESİ

**Karmaşık sistemler**, çok sayıda birbirine bağlı elemandan oluşur ve sistemin toplam davranışı, parçalarının basit toplamından farklıdır.

**Başlıca Özellikler:**

* **Büyüklük:** Çok sayıda bileşen içerir.
* **Çok boyutluluk:** Farklı türde bileşenler bulunur.
* **Kestirilemezlik:** Küçük değişiklikler büyük etkiler doğurabilir.
* **Etkileşim:** Öğeler birbirini karşılıklı etkiler.

📘 **Örnek:**
Bir virüsün topluma yayılması veya bir tweet’in viral hale gelmesi karmaşık sistem davranışıdır.

---

## 🔹 3. GRAF (ÇİZGE) KURAMI TEMELLERİ

Bir ağ matematiksel olarak **graf (graph)** ile temsil edilir.

[
G = (V, E)
]
Burada:

* (V): düğüm kümesi
* (E): bağlantı kümesi

### ➤ Graf Türleri

| Tür               | Açıklama                                | Örnek                    |
| ----------------- | --------------------------------------- | ------------------------ |
| **Yönsüz Graf**   | Bağlantılar çift yönlüdür.              | Facebook arkadaşlık ağı  |
| **Yönlü Graf**    | Bağlantıların yönü vardır.              | Twitter takip ağı        |
| **Tartılı Graf**  | Kenarlara ağırlık atanmıştır.           | Mesafe, etkileşim sayısı |
| **Tartısız Graf** | Sadece bağlantı var/yok bilgisi vardır. | Arkadaşlık ilişkisi      |

---

## 🔹 4. MATEMATİKSEL TEMSİLLER

### ➤ Komşuluk Matrisi

[
A_{ij} =
\begin{cases}
1, & (i,j) \in E \
0, & \text{aksi halde}
\end{cases}
]

* Yönsüz ağlarda simetriktir.
* Yönlü ağlarda asimetriktir.

### ➤ İnsidans Matrisi

Satırlar düğümleri, sütunlar bağlantıları gösterir.
Düğüm bağlantıya dahilse +1, -1 ile işaretlenir.

---

## 🔹 5. AĞLARDA TEMEL ÖLÇÜLER

### ➤ Derece (Degree)

Bir düğümün bağlantı sayısı:
[
k_i = \sum_j A_{ij}
]

### ➤ Ortalama Derece

[
\langle k \rangle = \frac{2L}{N}
]

### ➤ Derece Dağılımı

[
P(k) = \frac{\text{derecesi } k \text{ olan düğüm sayısı}}{N}
]

Gerçek ağlarda genellikle **güç yasasına (power law)** uyar:
[
P(k) \sim k^{-\gamma}
]

---

## 🔹 6. AĞ YOĞUNLUĞU VE SEYREKLİK

Maksimum bağlantı:
[
L_{max} = \frac{N(N-1)}{2}
]

Yoğunluk:
[
D = \frac{2L}{N(N-1)}
]

Gerçek dünyadaki ağlar genelde **seyrek (sparse)** yapılardır:
( L \ll L_{max} )

---

## 🔹 7. YOL VE UZAKLIK KAVRAMLARI

* **Yol (Path):** İki düğüm arasındaki bağlantı dizisi.

* **En kısa yol (Shortest Path):** En az kenarla ulaşım.

* **Ortalama yol uzunluğu:**
  [
  L = \frac{1}{N(N-1)}\sum_{i \neq j} d(i,j)
  ]

* **Kümeleşme katsayısı:**
  [
  C_i = \frac{2E_i}{k_i(k_i-1)}
  ]
  (E_i): düğümün komşuları arasındaki bağlantı sayısı.

---

## 🔹 8. AĞ TÜRLERİ VE MODELLERİ

### ➤ Erdős–Rényi (Rassal Ağ)

Her iki düğüm, olasılıkla (p) bağlıdır.
[
P(k) = \binom{N-1}{k}p^k(1-p)^{N-1-k}
]

### ➤ Watts–Strogatz (Küçük Dünya)

* Yüksek kümeleşme
* Kısa ortalama yol uzunluğu
  [
  L \approx \frac{\ln N}{\ln k}
  ]

### ➤ Barabási–Albert (Ölçekten Bağımsız)

* Güç yasası dağılımı: (P(k) \sim k^{-\gamma})
* **Tercihli bağlanma:** yeni düğümler yüksek derecelilere bağlanır.

---

## 🔹 9. MERKEZÎLİK ÖLÇÜLERİ

| Tür             | Formül                                                                 | Açıklama                              |
| --------------- | ---------------------------------------------------------------------- | ------------------------------------- |
| **Derece**      | ( C_D(i) = \frac{k_i}{N-1} )                                           | En fazla bağlantısı olan düğüm        |
| **Yakınlık**    | ( C_C(i) = \frac{N-1}{\sum_j d(i,j)} )                                 | En kısa ortalama mesafeye sahip düğüm |
| **Arasındalık** | ( C_B(i) = \sum_{s \neq i \neq t} \frac{\sigma_{st}(i)}{\sigma_{st}} ) | Bilgi akışını yöneten düğümler        |
| **Eigenvector** | ( C_E(i) = \frac{1}{\lambda}\sum_j A_{ij}C_E(j) )                      | Önemli düğümlere bağlı düğümler       |
| **PageRank**    | ( PR(i) = \frac{1-d}{N} + d\sum_j \frac{PR(j)}{k_j^{out}} )            | Web sayfalarının önem ölçüsü          |

---

## 🔹 10. TOĞLULUK (COMMUNITY) ANALİZİ

**Topluluk:** İç bağlantısı yüksek, dış bağlantısı zayıf düğüm kümeleri.

### ➤ Modülerlik

[
Q = \frac{1}{2m}\sum_{ij}\left[A_{ij} - \frac{k_i k_j}{2m}\right]\delta(c_i, c_j)
]

### ➤ Algoritmalar

* **Girvan–Newman:** Kenar betweenness’e göre.
* **Louvain:** Modülerliği maksimize eder.
* **Hiyerarşik Kümeleme:** Single, Complete, Average linkage yöntemleri.

---

## 🔹 11. DİNAMİK AĞLAR VE YAYILIM MODELLERİ

**Temporal ağlar:** Zaman içinde düğüm/bağlantı değiştirir.
**Yayılım modelleri:** Bilgi, hastalık, fikir gibi süreçlerin ağ üzerinde yayılmasını simüle eder.

📘 **Modeller:**

* **SI:** Sürekli bulaşma
* **SIR:** Bulaşma + iyileşme
* **SIS:** Tekrar bulaşma

---

## 🔹 12. AĞLARIN UYGULAMA ALANLARI

* Sosyal medya analizi (Facebook, X, Instagram)
* Protein–protein etkileşim ağları
* Ekonomik ağlar (finansal ilişkiler)
* Beyin bağlantı ağları (Human Connectome Project)
* Terör örgütü çözümlemeleri
* Web sayfası sıralama (PageRank)

---

# 🧩 **13. PYTHON UYGULAMALARI**

---

## 🔸 13.1. Ağ Oluşturma ve Görselleştirme

```python
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edges_from([("A","B"),("A","C"),("B","D"),("C","D"),("C","E"),("E","F")])
nx.draw(G, with_labels=True, node_color="lightblue", node_size=800)
plt.title("Basit Sosyal Ağ")
plt.show()
```

---

## 🔸 13.2. Derece Dağılımı

```python
import numpy as np
degrees = [val for (node, val) in G.degree()]
plt.hist(degrees, bins=range(1, max(degrees)+2))
plt.xlabel("Derece (k)")
plt.ylabel("Düğüm Sayısı")
plt.title("Derece Dağılımı")
plt.show()
```

---

## 🔸 13.3. Kümeleşme ve Ortalama Mesafe

```python
print("Kümeleşme Katsayıları:", nx.clustering(G))
print("Ortalama Kümeleşme:", nx.average_clustering(G))
print("Ortalama Yol Uzunluğu:", nx.average_shortest_path_length(G))
```

---

## 🔸 13.4. Merkezîlik Ölçümleri

```python
deg = nx.degree_centrality(G)
bet = nx.betweenness_centrality(G)
clo = nx.closeness_centrality(G)
eig = nx.eigenvector_centrality(G)
print("Derece:", deg)
print("Arasındalık:", bet)
print("Yakınlık:", clo)
print("Eigenvector:", eig)
```

---

## 🔸 13.5. Louvain Topluluk Analizi

```python
import community.community_louvain as community_louvain

partition = community_louvain.best_partition(G)
colors = [partition[node] for node in G.nodes()]
nx.draw(G, node_color=colors, with_labels=True, cmap=plt.cm.Set3)
plt.title("Topluluk Yapısı (Louvain)")
plt.show()
```

---

## 🔸 13.6. Rastgele ve Ölçekten Bağımsız Ağ Karşılaştırması

```python
ER = nx.erdos_renyi_graph(100, 0.05)
BA = nx.barabasi_albert_graph(100, 3)

print("ER Kümeleşme:", nx.average_clustering(ER))
print("BA Kümeleşme:", nx.average_clustering(BA))
```

---

## 🔸 13.7. Basit SIR Yayılım Modeli

```python
import random
def sir_simulation(G, beta=0.3, gamma=0.1, steps=10):
    status = {n: "S" for n in G.nodes()}
    infected = random.choice(list(G.nodes()))
    status[infected] = "I"
    results = []

    for _ in range(steps):
        new_status = status.copy()
        for node in G.nodes():
            if status[node] == "I":
                for n in G.neighbors(node):
                    if status[n] == "S" and random.random() < beta:
                        new_status[n] = "I"
                if random.random() < gamma:
                    new_status[node] = "R"
        status = new_status
        results.append(sum(1 for s in status.values() if s == "I"))
    return results
```

---

## 🔸 13.8. Gerçek Veri ile Çalışma (CSV)

```python
import pandas as pd
edges = pd.read_csv("edges.csv")
G = nx.from_pandas_edgelist(edges, "source", "target")
print("Düğüm Sayısı:", G.number_of_nodes())
print("Bağlantı Sayısı:", G.number_of_edges())
```

---

## 🔸 13.9. Görselleştirme — Merkezîliğe Göre Renklendirme

```python
bet = nx.betweenness_centrality(G)
colors = [bet[n]*1000 for n in G.nodes()]
nx.draw(G, node_color=colors, cmap=plt.cm.viridis, with_labels=True)
plt.title("Arasındalık Merkezîliğine Göre Düğüm Renkleri")
plt.show()
```

---

# 🔁 **14. TEKRAR ÖZETİ**

1. Ağlar düğümler + bağlantılardan oluşur.
2. Derece dağılımı çoğu zaman güç yasasına uyar.
3. Küçük dünya ve ölçekten bağımsız modeller doğada sık görülür.
4. Merkezîlik ölçüleri düğüm önemini belirler.
5. Topluluk analizi, ağın iç yapısını ortaya çıkarır.
6. Python kütüphaneleri (NetworkX, community, matplotlib) sosyal ağ analizi için güçlü araçlardır.