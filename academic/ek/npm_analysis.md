# npm Bağımlılık Ağı ve Yapısal Risk Analizi  
**Çalışma Konusu:** Top 1000 en çok indirilen npm paketinin bağımlılık ağı üzerindeki yapısal risklerinin analizi

---

## 1. Araştırma Problemi  
npm ekosistemindeki bağımlılıkların ağ yapısal analizine dayalı olarak güvenlik risklerini değerlendirmek ve kritik düğümlerin yapısal etkilerini ölçmek.  
Bağımlılıkların ağ içindeki konumları, güvenlik tehditlerine karşı nasıl savunmasızlık oluşturur?  
Özellikle, npm‑leaderboard verilerine göre top 1000 en çok indirilen paketler üzerinden bu analiz gerçekleştirilmektedir.

---

## 2. Alt Problemler  
### Alt Problem 1: npm Bağımlılık Ağı ve Topolojik Özellikler  
Top 1000 en çok indirilen npm paket verisi kullanılarak, bağımlılık ağı modellenebilir mi ve ağın temel topolojik özellikleri (düğüm sayısı, bağlı bileşenler, düğüm dereceleri) nelerdir?

### Alt Problem 2: Yapısal Risk Analizi İçin Metrikler  
Bu ağ modeli içerisinde her paket için **in‑degree**, **out‑degree** ve **betweenness merkeziyeti** gibi metrikler hesaplanabilir mi? Bu metriklerin dağılımı nasıldır?

### Alt Problem 3: Bileşik Risk Skoru Hesaplama  
Söz konusu metriklerin min‑max normalizasyonu ile birleştirilmesiyle “bileşik risk skoru” üretilebilir mi ve bu skor, ağdaki top 1000 paket için risk sıralaması sunabilir mi?

### Alt Problem 4: Ağın Sağlamlığı ve Kırılganlık Analizi  
Top 1000 en çok indirilen paketlerden yüksek risk skoruna sahip olanlar çıkarıldığında, ağın yapısı ve bağımlılık zincirleri nasıl etkilenir? Ağın sağlamlığı nasıl değişir?

---

## 3. Hipotezler  
### H1 (Yönlü Hipotez)  
Top 1000 en çok indirilen npm paketleri arasında, **in‑degree** değeri yüksek olan paketler, diğer paketlere göre **daha yüksek yapısal risk** taşıyacaktır.

### H2 (Yönlü Hipotez)  
Bu paketler arasında, **out‑degree** değeri yüksek olan paketler, bağımlılık yüzeyi geniş olduğu için **daha büyük güvenlik riski** taşır.

### H3 (Yönlü Hipotez)  
Ayrıca, **betweenness merkeziyeti** yüksek olan paketler, ağda köprü rolü üstlendikleri için **daha yüksek risk** taşımaktadır.

### H4 (Null Hipotez)  
Top 1000 en çok indirilen npm paketlerinden kritik düğümler çıkarıldığında, ağın güvenlik riski anlamlı şekilde artmaz — yani çıkarımın ağ üzerindeki etkisi **anlamlı değildir**.

---

## 4. Literatür Taraması  
### npm Ekosisteminde Bağımlılık Ağı ve Yapısal Riskler  
- npm ekosisteminde bağımlılık ağlarının karmaşıklığı ve büyüklüğü, yazılım tedarik zinciri saldırılarına karşı önemli bir güvenlik açığı oluşturabilir.  
- Ağ teorisi temelli analizler, bağımlılık ağlarının kırılganlık düzeyini bağlantı yapısı üzerinden ele almaktadır.  
  :contentReference[oaicite:3]{index=3}

### Ağ Teorisi ve Yapısal Risk Analizzi  
- Yönlü ağ modelleri üzerinde in‑degree, out‑degree ve betweenness merkeziyeti gibi ölçütler, kritik düğümlerin belirlenmesinde kullanılmıştır.  
  :contentReference[oaicite:4]{index=4}  
- Ayrıca, popüler paketlerin “indirilmeleri” ve “bağımlılık durumları” kullanım yönünden bir risk göstergesi olabilmektedir. :contentReference[oaicite:5]{index=5}

### İndirilmeye Dayalı Popülerlik ve Risk  
- npm‑leaderboard gibi araçlar top indirilen paketleri, büyüme oranlarını ve bağımlılıklarını izlemektedir. Bu sayede “popülarite” ile “risk” arasındaki olası ilişki incelenebilir. :contentReference[oaicite:7]{index=7}  
- Ancak indirilmelerin doğrudan aktif kullanım ya da güncelleme durumu ile eş olmadığı; çok indirilen ama güncel olmayan paketlerin de olabileceği vurgulanmıştır. :contentReference[oaicite:8]{index=8}

---

## 5. Özgün Katkılar  
- Top 1000 en çok indirilen npm paketleri bağlamında **yönlü ağ** modeli uygulanarak, bağımlılık ilişkileri temelden incelenmiştir.  
- Paketler için ağ metriklerine dayalı **bileşik risk skoru** geliştirilmiş ve bu skor ile paketlerin yapısal risk sıralaması yapılmıştır.  
- Ağın sağlamlık testleri (kritik düğüm çıkarımı) ile bağımlılık zincirlerinde kırılganlık analizi gerçekleştirilmiştir.  
- Popülerlik (indirilmeler) ile yapısal risk ölçütleri arasındaki ilişki, literatürde nadiren top‑1000 düzeyinde incelenmişken bu çalışma ile ele alınmıştır.

---

## 6. Diğer Gerekli Bilgiler  
- **Veri Kaynağı:** npm‑leaderboard (top 1000 en çok indirilen npm paketleri)  
- **Ağ Modeli:** Bağımlı → bağımlılık yönlü ağ  
- **Kullanılan Metrikler:** in‑degree, out‑degree, betweenness merkeziyeti  
- **Risk Skoru Hesaplama:** Metrikler min‑max normalizasyonu → ağırlıklı toplama → sıralama  
- **Sağlamlık Analizi:** Yüksek risk skorlu paketlerin çıkarılması → ağın bileşen yapısı, bağlılık zinciri bozulma ölçütleri  
- **Sınırlılıklar ve Dikkat Edilecek Hususlar:** İndirilmeler paketlerin aktif kullanımını tam olarak göstermeyebilir; bağımlılık verileri zamanla değişebilir; güncel olmayan paketler popüler olabilir ancak riskli olabilir.

---

## 7. Sonuç ve Değerlendirme  
Bu çalışma, npm ekosistemindeki bağımlılık ağlarının güvenlik açısından değerlendirilmesini sağlayacak yapıların oluşturulmasına öncülük etmektedir. Özellikle, popülerliği yüksek paketlerin ağ içindeki konumlarının, potansiyel yayılma ve kırılma etkilerinin analiz edilmesi, yazılım tedarik zincirindeki potansiyel tehlikelerin daha net ortaya konmasını sağlar. Gelecekteki araştırmalarda bu yaklaşım, diğer paket gruplarına ya da farklı ekosistemlere genişletilebilir.

