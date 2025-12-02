# Yazılım Tedarik Zinciri Güvenliği ve Saldırı Vektörleri

## 1. Giriş: NPM Neden Birincil Saldırı Yüzeyidir?

Node Package Manager (NPM), 3 milyondan fazla paketi barındıran ve haftalık milyarlarca indirme işlemi gerçekleştiren dünyanın en büyük yazılım kayıt defteridir. Modern yazılım geliştirme süreçleri, hızı artırmak amacıyla üçüncü taraf kod kütüphanelerine (bağımlılıklar) büyük ölçüde güvenir. Ancak, bir projeye tek bir NPM paketi eklendiğinde, ortalama 79 adet transitif (dolaylı) paket de dolaylı olarak güven zincirine dahil edilir.

Bu "örtük güven" (implicit trust) modeli, NPM'i saldırganlar için cazip bir hedef haline getirmiştir. Saldırganlar, tek bir popüler paketi veya onun derinliklerindeki bir bağımlılığı ele geçirerek, milyonlarca geliştiriciyi ve son kullanıcıyı etkileyebilecek "bire-çok" (one-to-many) dağıtım mekanizmasına sahip olurlar,. Bu belge, NPM ekosistemindeki aktif tehditleri ve bunlara karşı alınması gereken teknik savunma mekanizmalarını tanımlar.

---

## 2. Saldırı Türleri ve Teknik Taksonomi

Aşağıdaki saldırı vektörleri, modern yazılım tedarik zincirini hedef alan en yaygın ve kritik teknikleri temsil etmektedir.

### 2.1. Shrinkwrapped Clones (Paketlenmiş Klonlar)
**Risk Seviyesi:** Yüksek
**Tanım:** Bir saldırganın veya dikkatsiz bir geliştiricinin, meşru bir paketi kopyalayarak (klonlayarak) yeni bir isimle yayınlaması, ancak orijinal pakete atıfta bulunmaması durumudur.

*   **Nasıl Çalışır?** NPM ekosisteminde GitHub'daki gibi bir "fork" (çatallama) mekanizması yoktur. Bir paket kopyalandığında (clone), orijinal kaynakla (provenance) olan bağ kopar.
*   **Teknik Detay:**
    *   **Manifest Manipülasyonu:** Saldırgan, kopyaladığı paketin `package.json` dosyasını değiştirir ancak kodun tamamını veya bir kısmını korur.
    *   **Kilit Dosyası İstismarı:** `package-lock.json` veya `npm-shrinkwrap.json` dosyaları manipüle edilerek, bağımlılık ağacında bilinen güvenlik açıklarına sahip eski versiyonlar "sabitlenir" (pinned).
    *   **Güvenlik Riski:** Orijinal pakette bir güvenlik açığı bulunduğunda ve düzeltildiğinde (patch), bu düzeltme klonlanmış pakete (Shrinkwrapped Clone) yansımaz. `npm audit` gibi araçlar, klonun orijinal paketle ilişkisini bilmediği için bu güvenlik açığını tespit edemez,. Bu durum, bilinen zafiyetlerin "hayalet" sürümler aracılığıyla sistemde kalmasına neden olur.

### 2.2. Typosquatting (Yazım Hatası Avcılığı)
**Risk Seviyesi:** Orta-Yüksek
**Tanım:** Popüler paket isimlerine benzeyen isimlerle (örn. `react` yerine `raect` veya `colors` yerine `clolors`) zararlı paketlerin yayınlanmasıdır,.

*   **Nasıl Çalışır?** Geliştiricinin `npm install` komutunu yazarken yapacağı anlık bir dikkatsizlikten faydalanır.
*   **Teknik Detay:** Saldırganlar, Levenshtein mesafesi (iki kelime arasındaki karakter farkı) düşük olan isimleri seçer. Paket yüklendiğinde, `package.json` içindeki `preinstall` veya `postinstall` betikleri (scripts) aracılığıyla zararlı kod (malware) çalıştırılır ve sistemden ortam değişkenleri (ENV variables) veya SSH anahtarları çalınmaya çalışılır.

### 2.3. Dependency Confusion (Bağımlılık Karmaşası)
**Risk Seviyesi:** Kritik
**Tanım:** Şirketlerin iç ağlarında kullandığı özel (private) paket isimlerinin aynısının, genel (public) NPM kayıt defterinde daha yüksek bir versiyon numarasıyla yayınlanmasıdır.

*   **Nasıl Çalışır?** Paket yöneticileri (npm, pip vb.), varsayılan olarak hem özel hem de genel kayıt defterlerini kontrol eder. Eğer aynı isimde iki paket varsa, genellikle **daha yüksek versiyon numarasına** sahip olanı tercih eder.
*   **Teknik Detay:**
    *   *Private Package:* `@internal/auth-utils` (v1.0.0)
    *   *Malicious Public Package:* `@internal/auth-utils` (v99.0.0)
    *   Sistem otomatik güncelleme veya kurulum sırasında public registry'deki zararlı paketi çeker ve iç ağa sızma gerçekleşir,.

### 2.4. Account Takeover (ATO) & Worms (Hesap Ele Geçirme)
**Risk Seviyesi:** Kritik
**Tanım:** Güvenilir paket geliştiricilerinin hesaplarının (zayıf şifre, phishing veya sızdırılmış tokenlar nedeniyle) ele geçirilmesi ve paketlerine zararlı kod enjekte edilmesidir.

*   **Nasıl Çalışır?** Saldırgan, meşru geliştirici kimliğine bürünerek güvenilir bir paketin "yeni ve zararlı" bir versiyonunu yayınlar.
*   **Teknik Detay (Shai-Hulud Örneği):** Eylül 2025'te yaşanan bir olayda, saldırganlar oltalama (phishing) yoluyla geliştirici hesaplarını ele geçirmiştir. "Shai-Hulud" adı verilen zararlı yazılım, ele geçirdiği sistemdeki `.npmrc` dosyasındaki yayınlama tokenlarını (publishing tokens) çalarak kendini otomatik olarak diğer paketlere yaymış (worm-like behavior) ve yüzlerce paketi enfekte etmiştir,.

### 2.5. Protestware / Malicious Updates (Zararlı Güncellemeler)
**Risk Seviyesi:** Yüksek
**Tanım:** Meşru bir paket sahibinin, paketi kasıtlı olarak bozması (sabotaj) veya pakete zararlı işlevsellik eklemesidir.

*   **Nasıl Çalışır?** `node-ipc` veya `faker.js` olaylarında görüldüğü gibi, geliştirici politik veya kişisel nedenlerle popüler paketine, belirli IP adreslerindeki dosyaları silen veya sonsuz döngüye girerek sistemi kilitleyen kodlar ekler,.
*   **Teknik Detay:** Bu saldırılar, genellikle `minor` veya `patch` güncellemeleri (SemVer kurallarına göre güvenli olması beklenen) aracılığıyla dağıtılır ve otomatik güncelleme mekanizmalarını (örn. `^1.0.0`) hedef alır.

---

## 3. Teknik Savunma Stratejileri ve Önlemler

Saldırı yüzeyini daraltmak için savunma derinliği (defense-in-depth) ilkesi uygulanmalıdır.

### 3.1. Kurulum ve CI/CD Güvenliği

| Yöntem | Açıklama ve Uygulama |
| :--- | :--- |
| **`npm ci` Kullanımı** | CI/CD ortamlarında asla `npm install` kullanılmamalıdır. `npm ci` (clean install), `package-lock.json` dosyasındaki versiyonlara sadık kalır, `package.json`'ı güncellemez ve kurulumun tekrarlanabilirliğini (reproducibility) garanti eder. |
| **Lockfile Analizi** | Kilit dosyaları (lockfiles), paketlerin `integrity` (bütünlük) hash'lerini (SHA-512) ve `resolved` (kaynak) URL'lerini içerir. `lockfile-lint` gibi araçlarla, paketlerin güvenilir olmayan kaynaklardan (örn. saldırganın kendi sunucusu) indirilip indirilmediği kontrol edilmelidir. |
| **Script Devre Dışı Bırakma** | Mümkünse kurulum sırasında `npm install --ignore-scripts` parametresi kullanılarak, `preinstall` ve `postinstall` gibi saldırganların en çok kullandığı betiklerin çalışması engellenmelidir. |

### 3.2. Geliştirici ve Organizasyonel Önlemler

#### Scoped Packages (Kapsamlı Paketler)
Şirket içi paketler için mutlaka `@sirket/paket-adi` formatında **Scoped Packages** kullanılmalıdır. Bu, NPM registry'ye bu paketin bir kullanıcıya veya organizasyona ait olduğunu bildirir ve Dependency Confusion saldırılarını engellemek için `.npmrc` dosyasında bu kapsamın (scope) sadece özel registry'ye (örn. Artifactory, Verdaccio) yönlendirilmesini sağlar.

#### 2FA ve Token Güvenliği
NPM hesapları için **İki Faktörlü Kimlik Doğrulama (2FA)** zorunlu hale getirilmelidir (özellikle `publish` yetkisi olan hesaplar için). Otomasyon token'ları (Automation Tokens) kullanılırken, sadece gerekli paketlere ve IP adreslerine (CIDR whitelist) izin veren granüler yetkilendirmeler yapılmalıdır,.

#### Yazılım Bileşen Analizi (SCA) ve Güvenlik Araçları
*   **Socket.dev / OSSF Scorecard:** Geleneksel zafiyet tarayıcılarının aksine, bu araçlar paketin "davranışını" ve "sağlığını" analiz eder. Bir paketin aniden ağa erişim isteği göndermesi, dosya sistemine yazmaya çalışması veya `install` script eklemesi gibi anormallikleri tespit eder,.
*   **Snyk / npm audit:** Bilinen CVE (Common Vulnerabilities and Exposures) kayıtlarını taramak için kullanılır. Ancak, Shrinkwrapped Clones gibi gizli zafiyetleri her zaman yakalayamayacakları unutulmamalıdır,.

### 3.3. Manifest Dosyası İncelemesi
Geliştiriciler, `package.json` dosyasında özellikle şu alanlara dikkat etmelidir:
*   **`scripts`**: `preinstall`, `postinstall` alanlarında `curl`, `wget` veya şifrelenmiş (base64) komutlar var mı?
*   **`dependencies`**: İsimlerde yazım hatası (Typosquatting) var mı? Versiyon numaraları mantıklı mı?

---

## 4. Özet Tablo: Saldırı ve Önlem Matrisi

| Saldırı Türü | Birincil Vektör | Temel Önlem |
| :--- | :--- | :--- |
| **Shrinkwrapped Clones** | Klonlanmış/Değiştirilmiş Kod | Kaynak kod analizi, OSSF Scorecard (Bakım metrikleri) |
| **Typosquatting** | İsim Benzerliği | Paket isminin dikkatli kontrolü, Scoped packages kullanımı |
| **Dependency Confusion** | Versiyon Önceliği | `@scope` kullanımı, Private registry konfigürasyonu (.npmrc) |
| **Account Takeover** | Kimlik Hırsızlığı | Zorunlu 2FA, Granüler Tokenlar |
| **Malicious Updates** | Otomatik Güncelleme (`^`, `~`) | Dependency Pinning (Sürüm Sabitleme), `npm ci` |
| **Install Scripts** | `postinstall` Betikleri | `--ignore-scripts`, Socket.dev ile davranış analizi |
