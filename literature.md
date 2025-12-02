# 📚 Literatür Taraması ve Akademik Arka Plan

> **Bağlam:** Bu belge, NPM ekosistemi ve yazılım tedarik zinciri güvenliği üzerine yapılan akademik çalışmaları, temel bulguları ve projemizin bu literatürdeki konumunu özetler.
>
> 🏠 [Ana Sayfaya Dön](./README.md)

## 1. Genel Arka Plan ve Boşluk Analizi

Bu çalışma, açık kaynak paket ekosistemlerinde (özellikle NPM) yazılım tedarik zinciri saldırıları (SSCA) alanındaki temel çalışmaları, bulguları ve boşlukları derleyip sentezler. Amaç, ekosistem düzeyinde “önce hangi düğümlere yatırım yapılmalı?” sorusuna giden yolu aydınlatmak ve topolojik risk çerçevesini literatürle ilişkilendirerek güçlendirmektir.

- **Tehdit Taksonomileri:** Tehdit taksonomileri ve vaka derlemeleri, ekosistemler‑arası kurulum/çalışma zamanı tekniklerini iyi sınıflandırır: *Backstabber’s Knife Collection* (2015–2019, 174 vaka) ve *Hitchhiker’s Guide* referans çizgiyi verir.
- **NPM Odaklı Riskler:** NPM odaklı pratik riskler ve fenomenler (Wyss; Kang Yip) detaylandırılmıştır. Ancak bu literatür, “ekosistem düzeyinde hangi düğümlere önce yatırım yapılmalı?” sorusunu doğrudan operasyonel bir önceliklendirmeye dönüştürmez.
- **Ağ Bilimi:** Ağ bilimi cephesinde NPM’nin küçük‑dünya/ölçekten‑bağımsız yapısı ve tekil bakımcı/paketlerin orantısız etkisi açıkça gösterilmiştir (Zimmermann; Hafner; Oldnall). Buna karşın, yapısal/topolojik merkeziyet ile kullanım yoğunluğunu tek bir bileşik “kritiklik” metriğinde birleştiren yaklaşım eksik kalmıştır.

**Bizim Katkımız:** Son 12 ay indirime dayalı çekirdekte (Top 1000) resmi çözümleme kurallarıyla kurulan yönlendirilmiş graf üzerinde, topolojik ölçüler + kullanım yoğunluğu + bakım/güncellik sinyallerini kaynaştıran **Bileşik Kritiklik Skoru (BKS/BRS)** ve ona dayalı operasyonel öncelik listeleridir.

## 2. NPM Ağ Topolojisi ve Kırılganlık

- **Zimmermann (2019):** Az sayıda bakımcı hesabının çoğunluğu etkileyecek kapasitede olduğu; SPOF (tek hata noktası) ve bakım eksikliği etkisi.
- **Hafner (2021):** Hedefli düğüm çıkarımlarında ağın kırılgan; rastgele hatalarda görece dayanıklı olduğunu niceller; topluluk oluşumları.
- **Oldnall (2017):** Sürüm düzeyinde beş yıllık NPM topolojisi; küçük dünya + ölçekten bağımsız mimari; 200.000’e varan ters geçişli bağımlılıklar örneği.

> **Ana Mesaj:** Hub/omurga düğümlerinin ele geçirilmesi sistemik riski dramatik artırır; bu nedenle ağ‑temelli önceliklendirme gereklidir.

## 3. Bağımlılık Çözümleme ve Yayılım

- **Liu ve ark. (ICSE 2022):** DVGraph/DTResolver — NPM’nin resmî çözümleme kurallarına sadık, geniş ölçekli (10M+ sürüm, 60M+ ilişki) bilgi grafiği ve geçişli yayılım yolları.
- **Duan ve ark. (2020):** Yorumlanan dillerde kayıt istismarı ölçümü; niteliksel çerçeve + meta/statik/dinamik analizle 339 yeni kötü amaçlı paket bildirimi.

> **Ana Mesaj:** Doğru çözümleme kuralları, geçişli yayılımı ve etkilerini doğru ölçmek için önkoşuldur.

## 4. Tespit Hattı: ML/Dinamik Analiz ve İmzalar

- **Amalfi (2022):** ML + reprodüksiyon + klon tespiti; 95 yeni örnek; hafif ve hızlı boru hattı.
- **Cerebro (2023):** Davranış dizileri ile diller‑arası tespit; NPM/PyPI’de toplam 196+ yeni örnek.
- **OSCAR (2024):** Sandbox + fuzz + kancalı izlemede güçlü F1; endüstriyel dağıtımda 10.404 NPM, 1.235 PyPI kötü paket.
- **ACME (2021):** AST kümeleriyle imza üretimi; kümelerden imza çıkarıp kayıt tarama.

> **Ana Mesaj:** Tespit hatları olgunlaşıyor; ancak sınırlı analist kapasitesi için **topolojik bir ön‑filtre** (BRS) ile öncelikli tarama kuyruğu üretmek kritik.

## 5. Bakım/Güncellik ve Operasyonel Sinyaller

- **TOOD/PFET (Rahman ve ark., 2024):** 2.9M paket, 66.8M sürüm; PyPI genel güncellemede hızlı; Cargo güvenlik düzeltmesi benimsemede önde.
- **Cogo (2020):** Downgrade, aynı gün sürümler, deprecation madenciliği; bakım fenomenleri.
- **Ahlstrom (2025):** Bağımlılık budaması ile lisans/güvenlik risklerinin dramatik azaltımı (%86–94, %57–91).

> **Ana Mesaj:** Güncellik ve bakım sinyalleri BRS ile birlikte kullanıldığında eyleme dönük **yatırım planları** üretir.

## 6. Politika, İmza ve Bütünlük

- **in‑toto (Torres‑Arias, 2020):** Uçtan uca bütünlük; zincir adımlarının politikaya uygun kriptografik bağlanması.
- **Schorlemmer (2024):** İmza benimsemesi; politika etkisi; araçlandırmanın kaliteyi artırması.
- **Vaidya (2022):** Depo bütünlüğü, commit imzalama, yazılım sertifikasyon hizmeti (SCS).

> **Ana Mesaj:** Politika/bütünlük hattı, kayıt yöneticilerinin ve imzalama altyapısının rolünü vurgular; BRS ile **hedef listeleri** bu hattı besler.

## 7. Sentez: Boşluk → Katkı Haritalaması

| Alan | Mevcut Boşluk | Projenin Katkısı |
|------|---------------|------------------|
| **Önceliklendirme** | Ekosistem düzeyinde operasyonel önceliklendirme ölçütü eksik. | **Bileşik Risk Skoru (BRS)** = 0.5·in' + 0.2·out' + 0.3·btw' |
| **Tespit** | Geçişli yayılım/yüksek hassas çözümleme ile tespit hattı bağlanmıyor. | Resmî kurallarla kurulan yönlü graf + BRS ön‑filtre → **Öncelikli tarama kuyruğu** |
| **Politika** | Politika/bütünlük ve topluluk sağlığı sinyalleri operasyonelleştirilmiyor. | BRS hedef listeleri + TOOD/PFET → **Hedefli müdahale planları** |

---

## 8. Seçilmiş Kaynaklar (Özet)

### Temel Eserler
1. **Backstabber’s Knife Collection (Ohm ve ark., 2020):** 174 gerçek vaka, saldırı ağaçları.
2. **Hitchhiker’s Guide (Ladisa ve ark., 2023):** 7 ekosistem, 3 kurulum, 5 çalışma zamanı tekniği.
3. **Small World with High Risks (Zimmermann, 2019):** SPOF ve bakımcı merkeziyeti.
4. **The Web of Dependencies (Oldnall, 2017):** NPM ağının evrimi, 200K ters bağımlılık örneği.

### Tespit ve Analiz
5. **DVGraph/DTResolver (Liu, 2022):** Hassas bağımlılık çözümleme.
6. **Amalfi (2022), Cerebro (2023), OSCAR (2024):** Otomatik tespit sistemleri.

### Bakım ve Güvenlik
7. **Dependency Update Practice (Rahman, 2024):** Güncellik metrikleri (TOOD/PFET).
8. **in-toto (Torres-Arias, 2020):** Tedarik zinciri bütünlüğü.

---
*Bu belge, `academic/Readme.md` dosyasındaki literatür taraması bölümünden derlenmiştir.*
