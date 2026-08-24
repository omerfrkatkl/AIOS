# AIOS — Gereksinim Kütüğü (v2)

| | |
|---|---|
| **Amaç** | vision.md v2'yi çalışılabilir listelere ayırmak: gereksinim, tercih, hipotez, açık soru |
| **Yaşam döngüsü** | Yerinde güncellenir; hipotezler hükme bağlandıkça taşınır |
| **Sahip** | Proje sahibi |
| **Okuma tetikleyicisi** | Her yeni fazın başında + bir kararın hangi gereksinime hizmet ettiği sorgulandığında |
| **Kaynak** | `vision.md` v2 (17 bölüm) |

> Bu kütük mimari değildir. Gereksinimler *ne doğru olmalı*yı söyler, *nasıl* sorusunu değil. Her gereksinim yanlışlanabilir formdadır; § = vision v2 bölümü.

---

## G — Gereksinimler

### Hat, akış ve sahiplik

| # | Gereksinim | § |
|---|---|---|
| **G1** | Hat çalışır: fikir → netleştirme → araştırma → karar → plan → dilimli uygulama → test → teslim → sürdürme; her adımın çıktısı sonrakine girdidir | 7 |
| **G2** | Yükün büyük kısmını AIOS taşır; pilot oturumunda kullanıcıya yöneltilen teknik soru = 0 | 7 |
| **G3** | Kullanıcı vizyonun ve önemli kararların sahibidir; **görünürlük ≠ onay** | 7 |
| **G4** | Karar sınırı işler: yüksek etkili / pahalı geri alınır / yön değiştiren → kullanıcı; yerel / ucuz / hızlı fark edilen → AIOS | 7 |

### Kalıcı beyin

| # | Gereksinim | § |
|---|---|---|
| **G5** | Beyin makinededir (markdown+git); sıfır bağlamla farklı araçta devam edilebilir (tatbikatla ölçülür) | 2 |
| **G6** | 3-durum hafıza: onay/red/erteleme; red tekrar sunulmaz (oturumlar arası), ertelenen revisit tarihinde hatırlatılır; kayıtlar insan onayıyla aktifleşir (PENDING) | 2 |
| **G7** | Kişisel derin bilgi Obsidian vault'tadır; erişim hedeflidir (sorgu başına ≤ hedef not), tam-vault okuma yasak; AI sorudan önce vault'a bakar | 2 |

### Tanıma

| # | Gereksinim | § |
|---|---|---|
| **G8** | Adaptif soru: önceki cevaba uyarlanır, tekrar etmez; cevaplar kanıt-etiketli profilde birikir | 4 |
| **G9** | Profil iki katmanlıdır (çalışma + kişilik/üslup), tavanlı; tazelik içerikten denetlenir | 4 |

### Kaynak zekası

| # | Gereksinim | § |
|---|---|---|
| **G10** | Kanal+araç envanteri: tür (API/web-chat/abonelik/yerel), limit, maliyet, yetenek, son-doğrulanma tarihi; **yerel bölgede** | 5 |
| **G11** | Görev→kanal/model/efort seçimi AIOS tarafından yapılır/önerilir; öneriler envanterle tutarlı ve gerekçelidir | 5 |
| **G12** | Limit bitince geçiş: API'de otomatik (429), web-chat'te öneri (bildirim + tahmin); geçiş görev sınırında olur, bağlam beyinden tohumlanır | 5 |
| **G13** | Yetenek sağlayıcılar: yeteneği olmayan kanala araç takılır (web-arama takviyesi vb.); takılı yetenekler envanterde görünür | 5 |

### Karar sistemi

| # | Gereksinim | § |
|---|---|---|
| **G14** | Araştırma motoru: yöntem seçimi probleme göre; raporlar kanıt-etiketli saklanır; aynı soru önce önbelleğe bakar | 6 |
| **G15** | Puanlama: boyutlar/ağırlıklar **puan görülmeden önce** sabitlenir; her puan kanıtlı rapora atıflıdır; kafadan puan geçersizdir | 6 |
| **G16** | Kapanış kuralı: alternatif üretimi sınırlıdır (max N + süre); sistem karar verir | 6 |
| **G17** | Karar izlenebilirliği: neden / alternatifler / kanıt / geri-alma maliyeti / yeniden-değerlendirme koşulu | 6 |
| **G18** | Sonuç-izleme: büyük kararların sonucu ölçülür; puanlama ağırlıkları gerçek sonuçlarla kalibre edilir | 6 |
| **G19** | Kademeli otonom: alan-bazlı güven seviyesi kayıtlı ve görünürdür; iyi sonuç yükseltir, hata düşürür | 6 |
| **G20** | Kullanıcının önerisi de, sistemin ilk önerisi de otomatik doğru değildir | 6 |
| **G21** | Geri-çağırma: "geri al" → bağımlılık zinciri + etki analizi + geri alma planı | 6 |
| **G22** | Tartışma protokolü: ≥2 AI, ≤3 tur, farklı sağlayıcı tercih; argümanlar kanıt-etiketli; çıktı = karar hattına giren öneri | 3 |

### Arayüz ve teslim

| # | Gereksinim | § |
|---|---|---|
| **G23** | Nihai yüzey **Windows GUI uygulamasıdır**; tasarım referansı opencode; uygulama istemcidir — sistem headless çalışır | 8 |
| **G24** | Uygulama araçları **kayıt defterinden** okur; ekleme/çıkarma manifest girişidir, kod değişikliği değildir | 10 |
| **G25** | İç görünümler: model seçici, tartışma arayüzü, araştırma görünümü, durum panosu, log görüntüleyici | 8 |

### Kaynak disiplini

| # | Gereksinim | § |
|---|---|---|
| **G26** | Oturum açılışı = STATE + PROFILE + aktif-karar özeti; başka hiçbir dosya varsayılan yüklenmez; **logs asla** | 9 |
| **G27** | Açılış bağlamı ≤ bazalın %50'si (892 satır → ≤446); sayaç ölçer, review trend verir | 9 |
| **G28** | Dikkat bağımsız kalite kriteridir: gereksiz soru/rapor/karar taşınmaz, önemli görünür kalır | 9 |

### Modülerlik ve loglama

| # | Gereksinim | § |
|---|---|---|
| **G29** | Her bileşenin yazılı sözleşmesi vardır (dosyalar: dört alan) | 10 |
| **G30** | Araçlar/yetenekler manifest'e kendini kaydeder; çekirdeğin bileşene sıkı bağımlılığı yasaktır | 10 |
| **G31** | Yüzeyler istemcidir; beyin arayüzden bağımsız doğrulanır | 8, 10 |
| **G32** | Tüm araçlar/olaylar tek JSONL standardında loglanır; logs/ yereldir, rotasyonludur | 11 |
| **G33** | Kullanıcıya hata üç satırdır: ne oldu / neden / ne yapmalı; teknik detay logdadır | 11 |
| **G34** | Tekrarlanan hatalar öğrenmeye dönüşür | 11 |

### Açık kaynak, süreklilik, doğrulama, kurtarma

| # | Gereksinim | § |
|---|---|---|
| **G35** | AIOS + yönetilen projeler: MIT + LICENSE/README/CHANGELOG/semver standartları | 12 |
| **G36** | Uzun oturum fark edilir, geçişte bilgi kaybı yok; handoff kompakt ve doğrulanabilirdir | 2 |
| **G37** | Periyodik süreklilik tatbikatı: farklı araç + sıfır bağlam ≤15 dk devam | 2, 15 |
| **G38** | Tek aktif yürütücü; paralel iş yürütücü kontrolündedir, beyne tek yazıcıyla işlenir | 3 |
| **G39** | Kanıt etiketleri zorunlu: [gözlendi]/[üretildi]/[varsayıldı]; [üretildi] T-A'ya dayanak olamaz | 6, 15 |
| **G40** | Yürütmeyle doğrulama (test/build/run/benchmark) tercih edilir | 15 |
| **G41** | Aynı modelin kendi çıktısını onaylaması yeterli değildir; gerektiğinde çapraz-model review | 3, 6 |
| **G42** | Kurtarma: git + yerel-katman bundle + geri-dönüş scripti + acil durum kartı | 15 |
| **G43** | Pilotun amacı AIOS hakkında kanıt üretmektir; pilot AIOS'un yerine geçmez | 16 |
| **G44** | Başarı ölçütü aşağıdadır — yanlışlanabilir + ölçüm tarihli | 16 |

---

## T — Tercihler

T1 · Tasarımsal konularda kullanıcıya seçenek sunulması
T2 · Windows araçları Scoop ile merkezî yönetilir
T3 · Claude ana çalışma ortağı *olabilir* (tek kanal asla değil)

## H — Hipotezler (taşınan hükümler)

| Hipotez | Hüküm | Not |
|---|---|---|
| markdown+git kaynak-of-truth | **Benimse** | Model/araç değişimine dayanan tek katman |
| Obsidian | **Benimse — kişisel depo** | Hedefli erişim; agent-kritik bağımlılık yok |
| SQLite | **Benimse — sonra** | İndeks/sorgu katmanı, panel adımında |
| Vektör store | **Test** | Yalnızca eşleştirme indeksi; eşik kırılgan |
| Knowledge graph birincil hafıza | **Red (arşiv kararı)** | Gerekçe geçerli; yeni kanıt çıkarsa yeniden değerlendirilir |

## S — Açık sorular

| # | Soru | Faz |
|---|---|---|
| S1 | GUI teknolojisi (Tauri/Electron/.NET/Avalonia); ölçüt: opencode tasarım-taşınabilirliği | F15 |
| S2 | opencode tasarımının GUI'ye taşıma biçimi | F15 |
| S3 | Web-chat limit algılama şeması (bildirim + tahmin) | F12/13 |
| S4 | Puanlama boyutları ve ağırlıkları (literatürle: ADR/MCDA) | F9 |
| S5 | Tartışma protokolü detayları (katılımcı seçimi, tur formatı) | F9 |
| S6 | Yetenek sağlayıcı mekanizması (MCP / CLI sarmalayıcı önceliği) | F12 |
| S7 | Konvansiyon paylaşımı yönetilen projelere (ritüel şablonu) | F8 |
| S8 | Profil yükü dengesi (§4 ↔ §9 gerilimi) | F6 |

## Çelişkiler ve çözümleri

| Gerilim | Çözüm |
|---|---|
| Platform genişliği ↔ token minimalizasyonu | Katmanlı yükleme sözleşmesi (varsayılan minimal, ihtiyaca göre derin) |
| Kademeli otonom ↔ sahiplik | Otonom alan-bazlı ve görünür; T-A her zaman kullanıcıda |
| Açık kaynak ↔ kişisel gizlilik | **Çözüldü:** hibrit bölünme (public yapısal / yerel kişisel) |
| Araştırma derinliği ↔ hız | Yöntem seçimi + önbellek + kapanış kuralı |

---

## Başarı Ölçütü `[sahip onaylı 2026-08-23]`

**Ölçüm tarihi: 2026-11-30**

### ÇALIŞIYOR — dördü birden doğruysa
1. Yeni sistemle en az bir gerçek proje plan aşamasını geçip **saklanacak çıktı** üretti — işi **AIOS sürdü**, sahip paralel yapmadı.
2. En az bir kez **≥3 hafta ara** sonrası **farklı araçta**, sıfır bağlamla **≤15 dakikada** devam edilebildi (tatbikat kaydıyla).
3. **Hiçbir önemli karar sonradan sürpriz olmadı** — tüm T-A'lar onaylı/görünür kayıtlı.
4. Ortalama oturum açılış bağlamı **≤446 satır** (bazal 892'nin yarısı) **ve** sahibin algısı: "öncekinden yavaş değil".

### ÇALIŞMIYOR — biri bile doğruysa
- Belgeler güncel ama üreten bir şey yok → **eski proje tekrarı**
- DECISIONS/LEDGER girişleri durdu → **terk sinyali**
- Protokolü atlamak daha hızlı geliyorsa ve sahip atlıyorsa → **ek yük değeri aştı**
- Aynı hata ikinci kez log'a düştü ve öğrenmeye dönüşmedi → **öğrenme vaadi başarısız**
