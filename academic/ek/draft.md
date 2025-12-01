Yazılım Tedarik Zincirinde Kritiklik Haritalaması: En Çok İndirilen 1000 NPM Paketinin Bağımlılığının Topolojik Risk Değerlendirmesi
Yusuf Talha ARABACI, Ekim 2025
--------------------------------------------------------------------------------
Özet
Modern yazılım tedarik zincirlerinin (SSC) temelini oluşturan NPM (Node Package Manager) ekosistemindeki yoğun transitif bağımlılıklar, tek bir paketteki zafiyetin yüzlerce projeye yayılması potansiyeli nedeniyle sistemik bir risk alanı yaratmaktadır. Bu bildiri, paket içeriğinden ziyade paketler arası ilişkilerin topolojik yapısına odaklanmaktadır. En çok indirilen 1000 NPM paketini baz alarak kurulan yönlü ağ üzerinde, in-degree, out-degree ve betweenness merkeziyetleri hesaplanmıştır. Bu topolojik ölçüler, min–max normalizasyonu ile tek bir Bileşik Risk Skoru (BRS) metriğine dönüştürülmüştür. Bulgular, ağın ağır kuyruklu, ölçekten bağımsız (scale-free) bir yapı sergilediğini ve az sayıda omurga düğümün ele geçirilmesinin ağın bağlanırlığını dramatik biçimde bozduğunu kanıtlamaktadır (Robustness analizi). Sonuç olarak, BRS, güvenlik kaynaklarını en yüksek yayılım potansiyeline sahip kritik paketlere yönlendiren operasyonel bir harita görevi görmektedir.
1. Giriş
Açık kaynak yazılım bileşenlerinin yaygın kullanımı, yazılım tedarik zinciri saldırılarına (SSCA) karşı ekosistemlerin kritik derecede kırılgan hale gelmesine neden olmuştur. NPM, 1.7 milyondan fazla pakete ev sahipliği yapan (2022 verilerine göre) ve sürekli güncellenen bir ortam olarak, bu riskin en yoğun yaşandığı alanlardan biridir. Bu kırılganlığın somut örnekleri, event-stream, ua-parser-js ve 2024'te gözlemlenen Shai-Hulud solucanı saldırısı gibi olaylarla açıkça ortaya konmuştur. Bu olaylar, kritik bir paketin zehirlenmesinin (source poisoning) veya kaldırılmasının, ekosistem içinde hızla yayılan bir basamaklı çöküşe (cascading failure) yol açabileceğini göstermiştir.
Literatür, NPM ağının doğasını incelemiştir. Zimmermann, Staicu ve Pradel'in (2019) öncü çalışması, NPM ekosisteminin küçük dünya (small world) davranışı ve yüksek riskler taşıdığını, az sayıda paketin (hub'ların) orantısız derecede fazla bağımlılığa sahip olduğunu göstermiştir. Benzer şekilde Oldnall ve ark. (2020) ile Hafner ve ark. (2018), bu ağın ölçekten bağımsız bir mimari sergilediğini, rastgele hatalara karşı dayanıklı olsa da, hedefli hub saldırılarına karşı son derece kırılgan olduğunu kanıtlamıştır.
Mevcut güvenlik tespit araçları (CVSS skorları veya SCA araçları), paket içeriğindeki zafiyetlere odaklanırken, bir paketin ağ içindeki konumsal etkisini ve potansiyel yayılım büyüklüğünü yeterince ölçmemektedir. Bu durum, güvenlik analistlerinin kısıtlı kapasitesini nereye yönlendirecekleri konusunda operasyonel bir önceliklendirme ölçütü eksikliğine yol açar.
Bu bildiri, NPM bağımlılıklarını yönlü bir ağ olarak modelleyerek, literatürde kanıtlanan ağın kırılgan yapısını hedeflemekte ve yapısal riski kullanım yoğunluğu ile birleştiren nicel bir metodoloji sunmaktadır.
2. İlgili Çalışmalar ve Kuramsal Çerçeve
2.1 NPM Ağının Yapısı ve Kırılganlığı
Yazılım paket yöneticileri (NPM, PyPI, Maven) üzerindeki bağımlılıklar, düğümlerin paketleri ve kenarların bağımlılık ilişkilerini temsil ettiği karmaşık ağlar olarak analiz edilir. Bu ağlarda, derece dağılımının genellikle güç yasasına (power law) uyduğu (P(k)∼k −γ) ve tercihli bağlanma (preferential attachment) mekanizmasıyla büyüdüğü gözlemlenmiştir. Hafner ve ark. (2018), NPM ağının bu topolojik özellikleri nedeniyle, rastgele düğüm çıkarımlarına karşı nispeten dayanıklı olduğunu, ancak PageRank veya hub'lar gibi kritik düğümlerin çıkarılması durumunda ağın hızla parçalandığını göstermiştir.
Decan, Mens ve Constantinou'nun (2018) çalışması, güvenlik zafiyetlerinin NPM paket bağımlılık ağındaki etkisini incelemiş, zafiyetlerin yayılımının teknik gecikmeyle (technical lag) ve bağımlılık yapısıyla ilişkili olduğunu belirtmiştir. Liu ve ark. (2022), zafiyet yayılımının dinamik değişimlerini incelemek için iç ve çapraz kütüphane ilişkilerini modelleyen DVGraph ve zafiyet giderme için DTResolver gibi araçlar geliştirmiştir.
2.2 Güvenlik Tespit Metotlarının Konumlandırılması
Geleneksel güvenlik yaklaşımları genellikle kötü niyetli davranışın içeriğine veya imzasına odaklanır:
1. Statik/Dinamik Analiz: Cerebro ve Amalfi gibi araçlar, kötü niyetli davranış sekanslarını veya statik özellikleri kullanarak zararlı paketleri tespit etmeye odaklanır. Cerebro, diller arası bilgi kaynaştırmayı (bi-lingual knowledge fusing) sağlayarak, statik özelliklere dayalı olarak NPM ve PyPI'da etkili sonuçlar almıştır (Cerebro RoBERTa NPM'de %98.5 hassasiyet ve %92.9 geri çağırma sunar). OSCAR ise dinamik analiz ile Düşük Yanlış Pozitif Oranı (FPR) elde ederek zehirleme tespitinde iyileşme sağlamıştır.
2. Topolojik Risk (BRS): Sunulan BRS metodolojisi, bu tespit araçlarının tamamlayıcısı olarak konumlanır. BRS, bir paketin kötü niyetli olup olmadığına değil, kötü niyetli olduğu varsayılırsa yaratacağı sistemik hasarın (Package Impact) büyüklüğüne odaklanır. Bu, güvenlik kaynaklarının (manuel kod incelemesi, daha yoğun SCA taraması) önceliklendirilmesi için hayati bir operasyonel ölçümdür.
3. Metodoloji: Bileşik Risk Skoru (BRS)
3.1 Ağ Modellemesi ve Veri Toplama
Çalışma, en çok indirilen ilk 1000 NPM paketinin (Top N) ve bunların bağımlılıklarının oluşturduğu ağ üzerinde yürütülmüştür.
• Veri Kaynağı: Paket listeleri ve bağımlılık verileri öncelikle ecosyste.ms API'lerinden ve yedek olarak npm registry'den alınmıştır.
• Ağ Yapısı: Ağ, yönlü bir graf (DiGraph) olarak modellenmiştir. Düğümler (Nodes) NPM paketlerini temsil ederken, yönlü kenarlar (Edges) Bağımlı (Dependent) → Bağımlılık (Dependency) ilişkisini gösterir. Analiz edilen ağ 1139 düğüm ve 2164 kenar içermektedir (Graf İstatistikleri Özet Tablosu).
3.2 Merkeziyet Metrikleri ve Normalizasyon
BRS'yi hesaplamak için üç merkeziyet metriği kullanılmıştır:
1. Gelen Derece (Cin / In-Degree): Bir pakete olan bağımlılık sayısını gösterir. Yüksek değeri, yayılım potansiyelini ve paketin ekosistemdeki omurga konumunu işaret eder.
2. Giden Derece (Cout / Out-Degree): Paketin dış bağımlılık sayısını gösterir. Yüksek değeri, paketin tedarik riskine maruziyetinin arttığını gösterir.
3. Aradalık Merkeziyeti (Cb / Betweenness): Ağdaki en kısa yollar üzerinde bir düğümün aracılık (köprü) rolünü ölçer. Betweenness, büyük graflarda pratik hesaplama zorlukları nedeniyle örnekleme (rastgele k≈200 kaynak düğüm) ile hızlandırılmıştır.
Tüm metrikler, skorlamadan önce eşitsiz etkilerini gidermek için aralığına min–max normalizasyonu ile ölçeklenir.
3.3 Bileşik Risk Skoru (BRS) Formülasyonu
BRS, normalize edilmiş merkeziyet metriklerinin ağırlıklı toplamı olarak yapısal etkiyi ölçer.
Burada C′ normalize edilmiş merkeziyet değerini temsil eder.
Ağırlıklar ve Gerekçe (GitHub referans):
Bu çalışmada kullanılan varsayılan ağırlıklar şunlardır:
• win=0.5
• wout=0.2
• wb=0.3
Gerekçe: win'in en yüksek ağırlığa (0.5) sahip olması, yüksek gelen dereceye sahip paketlerin "hub" olarak sistemik yayılım potansiyelinin en kritik risk göstergesi olduğu varsayımına dayanır. Bu, bir saldırının maksimum Basamaklanma Etkisini yaratma senaryosunu önceliklendirir.
3.4 Kaskad Etkisi ve Sağlamlık Analizi
Kaskad Etkisi (Basamaklanma): Bir paketteki sorunun, onu transitif olarak kullanan (dependents) paket sayısını ifade eder. Bu, yönlü grafiğin tersi (Grev) üzerinde BFS/DFS kullanılarak, tohum düğümden (saldırıya uğrayan paket) erişilebilen tüm düğümlerin sayılmasıyla nicel olarak ölçülür.
Sağlamlık (Robustness): BRS sıralamasına göre en kritik düğümlerin (k∈{1,3,5}) çıkarılmasının, ağın zayıf bileşen sayısı ve en büyük bileşen boyutu üzerindeki etkisini analiz eder (bkz. results/robustness_risk.json).
4. Bulgular ve Yorum
Bulgular, proje GitHub sayfasındaki (https://yusufarbc.github.io/npm-complex-network-analysis/) ve rapor taslaklarındaki verilere dayanmaktadır.
4.1 Ağ Yapısı ve Merkeziyet Dağılımları
NPM bağımlılık ağı, ağır kuyruklu (heavy-tailed) bir derece dağılımı sergiler. Bu, az sayıda paketin çok yüksek dereceye sahip olduğunu (hub'lar), büyük çoğunluğun ise düşük derecelerde kaldığını, yani sistemik riskin bu az sayıdaki hub'da toplandığını gösterir.
Korelasyonlar: In-degree ile Betweenness Merkeziyeti arasında güçlü pozitif bir korelasyon olduğu gözlemlenmiştir. Bu, yüksek popülerliğe (yayılım potansiyeli) sahip omurga paketlerinin, aynı zamanda ağdaki bilgi akışının geçtiği kritik köprü (boğaz noktası) rolünü de üstlendiğini gösterir.
4.2 Bileşik Risk Skoru (BRS) Liderleri
BRS'nin hesaplanmasıyla elde edilen Top 20 Risk Skoru listesi (Tablo 1), tekil metriklerin ötesinde operasyonel önceliklendirme için güçlü bir ayrım gücü sağlar.
Yorum: En yüksek BRS'ye sahip paketler, JavaScript/TypeScript'in altyapı katmanında veya popüler geliştirme araçlarının çekirdeğinde yer alır. Örneğin:
• tslib: Yüksek In-Degree ile kritik bir omurga düğümüdür, TypeScript'in çalışma zamanı yardımcı işlevlerini sağlar ve yaygın kullanımı nedeniyle tedarik zinciri açısından kritik öneme sahiptir.
• es-abstract: ECMAScript spesifikasyonundaki soyut işlemleri uygulayan, küçük, alt katman bir kütüphane olup, yüksek Out-Degree ve Betweenness ile hem geniş bağımlılık yüzeyine hem de köprü rolüne sahiptir.
• @babel/helper-plugin-utils: Yüksek In-Degree ile Babel eklentilerinin temel yardımcı işlevlerini sunar; ele geçirilmesi durumunda geniş bir eklenti ekosistemini etkileyebilir.
4.3 Kaskad Etkisi (Basamaklanma) Analizi
Kaskad etkisi sonuçları, BRS'nin potansiyel yayılımı öngörmede başarılı olduğunu gösterir. Ancak, Risk Skoru ile Kaskad Etkisi arasındaki ilişki doğrusal değildir. Bu doğrusal olmama durumu, basit In-Degree gibi tekil metriklerin, ağın karmaşık yerel bağlantı yapısından kaynaklanan tüm yayılım dinamiğini açıklamada yetersiz kaldığını gösterir.
4.4 Ağın Sağlamlığı Üzerindeki Dramatik Etki
Sağlamlık analizine dayalı sonuçlar (results/robustness_risk.json), en yüksek BRS'ye sahip düğümlerin hedeflenerek çıkarılmasının ağın bütünlüğünü anlamlı ölçüde bozduğunu kanıtlar.
5. Tartışma ve Sonuç
Bu çalışma, NPM ekosistemindeki sistemik riskin aciliyetine, transitif bağımlılıkların oluşturduğu yapısal tehlikeye karşı topolojik bir çözüm sunmaktadır. Literatürde halihazırda bulunan NPM ağının kırılganlığına dair bulguları destekleyerek, bu yapısal bilgiyi operasyonel bir önceliklendirme ölçütü olan Bileşik Risk Skoru'nda (BRS) birleştirmiştir.
Sınırlamalar
Betweenness merkeziyeti, büyük graflarda hesaplama maliyetini azaltmak amacıyla örnekleme (k≈200) ile hesaplanmıştır; bu, mutlak doğruluğu etkileyebilir. Ayrıca, min–max normalizasyonu kullanılan veri setine bağımlı olup, skorun yorumu bağlama özeldir.
Gelecek Çalışmalar
Gelecekteki araştırmalar, BRS skorunu PageRank merkeziyeti ve zaman serisi dinamikleri (temporal ağlar) ile zenginleştirebilir. Ayrıca, yüksek riskli paketler etrafında oluşan topluluk yapılarının incelenmesi, risk yayılım mekanizmalarını daha derinlemesine anlamamıza yardımcı olabilir.
--------------------------------------------------------------------------------
BRS metodolojisi, tıpkı bir karayolu ağındaki harita gibi çalışır. Standart güvenlik denetimleri, her bir aracın (paketin) frenlerinin (kodu) sağlamlığını kontrol ederken; BRS, kaynakları, otoyolların kesişim noktalarında (yüksek Betweenness) ve en çok trafiğin geçtiği ana arterlerde (yüksek In-Degree) yoğunlaştırmamız gerektiğini söyleyen stratejik bir plana karşılık gelir. Bu noktaların güvenliği, tüm sistemin sağlamlığını garanti etmenin anahtarıdır.

---

# 📘 KARMAŞIK AĞ ANALİZİ — TAM DERS NOTU (Ek)

Bu bölüm, temel ağ bilimi kavramlarını ve Python ile pratiklerini kapsayan kısa bir ders notudur. (İçerik: ağ türleri, ölçüler, modeller, topluluk tespiti, Python kod örnekleri.)

