# PLAN — AIOS Platform İnşası (yürütme haritası)

| | |
|---|---|
| **Amaç** | Platformun tüm inşasının tek yetkili haritası — her adım işaretlenir, her oturum buradan devam eder |
| **Yaşam döngüsü** | Her adım sonrası işaretlenir; faz kapanışlarında önceki adımlar denetlenir |
| **Sahip** | Proje sahibi (yön onayları) · AIOS/Claude (yürütme) |
| **Okuma tetikleyicisi** | Her oturum açılışı — plan dosyasından devam edilir |

> **Ölçek beyanı:** bu platform "tüm AI araçlarının birleşimi" hedefindedir. Kapsam küçültülmez, acele edilmez; her faz tek başına değer üretir.

## Çalışma protokolü (sahibin talimatı 2026-08-25)

1. Her oturum bu dosyadan devam eder: ilk **☐** adımı bulunur, uygulanır. "Ne yapalım" sorulmaz.
2. **Her adım sonrası denetim:** önceki tüm adımlar + o adım detaylı analiz edilir (eksik / fazlalık / yanlışlık / hata) — bulgu anında düzeltilir, temizse not edilir.
3. **İyi fikir protokolü:** çalışma sırasında iyi fikir gelirse "önce şunu ekleyeyim" denir, plana işlenir, oradan devam edilir.
4. İşaretler: ✅ tamam · 🟡 kısmi · ☐ bekleyen · ⏸ ertelendi.
5. **Sahip Doğrulama Kapısı** ve **Araştırılabilirlik filtresi** her adımda geçerlidir.

## 0. Hedef, ilkeler ve mimari yasalar

**Tek cümle:** Hangi AI'yi, hangi arayüzden, hangi modelle kullanırsam kullanayım aynı davranan; unutmayan; beni tanıyan; token-verimli; kararlarını araştırmaya dayalı puanlamayla doğrulayan; fikirden sonuca beni yönlendiren kişisel AI platformu.

**Kuzey-yıldızı:** "tek cevap ve sıradan sohbet"ten "yıllarca sürecek proje"ye aynı sistem; API, CLI, chat, yerel model — hepsi bağlanabilir.

**Taşınan ilkeler:** kanıt etiketleri · T-A/B/C · tek-yazıcı · görünürlük ≠ onay · yanlışlanabilir test (eşik veri öncesi) · fren = sayı + takvim · append-only · dört-alanlı dosya · Topoloji C · markdown+git · dil kuralı · **asla acele yok.**

**Mimari yasalar:**
1. **Sözleşme-first** — her bileşenin yazılı sözleşmesi var (dosyalar: dört alan)
2. **Kayıt-defteri-güdümlü** — araçlar/yetenekler manifest'e kaydolur; yüzeyler kayıt defterinden okur
3. **Gevşek bağlı** — çekirdek hiçbir araca/arayüze/sağlayıcıya sıkı bağlı olamaz
4. **Yüzeyler istemcidir, beyin egemendir** — uygulama olmasa da sistem çalışır
5. **Append-only veri, idempotent araçlar**
6. **Tek sorumluluk** — her dosya/script tek iş
7. **Kanal Sözleşmesi** — her kaynak `{tür, parametreler[], girdiler[], limitler{}, yetenekler[], enforcement, dosya-erişimi}` bildirir; UI/yönlendirici/zorlama bundan çizer

**Katmanlar:** BEYİN (sözleşmeli dosyalar) · ZORLAMA (araçlar) · **GÖZLEMCİ** (zamanlayıcı+izleyiciler: manuel → Task Scheduler → uygulama) · YÜZEY (istemciler) · YÜK (yönetilen projeler).

## 1. Sıfırlama kuralı

- Aktif kök yalnızca yeni sistemin dosyalarını içerir; `arsiv/` referanstır (girdi değil).
- git geçmişi korunur. İstisnalar: PLAN.md, DECISIONS.md (v3), kalıcı CLAUDE.md.
- Yönetilen projelere (KB, ledger, PDF360, DC, DNS) dokunulmaz.
- **Geri dönüş = git** (her faz commit'li). Eski geri-dönüş scripti emekli edildi (2026-08-25).

## 2. Gizlilik mimarisi (hibrit)

| Bölge | İçerik |
|---|---|
| **Public (git)** | PLAN, vision, REQUIREMENTS, CLAUDE.md, PROJECT-INSTRUCTIONS, tools/, hooks/, adapters/, tests/, LICENSE, DECISIONS, STATE (kişisel detaysız) |
| **Yerel (gitignored + backup)** | PROFILE, LEDGER, vault/, sağlayıcı envanteri, logs/, backups/ |

## 3. Faz haritası

Fren semantiği: inşaat fazlarında duraklama dedektörü (2 hafta sessizlik → sahip kararır); yalnız F8 pilotu katı frenle kapanmıştı.

### ✅ F0 · Sıfırlama (6/6) — 2026-08-23, commit 76e1b9d
- [x] arsiv/ taşıma + yeni DECISIONS + geri-dönüş scripti (sonradan emekli) + geçici CLAUDE.md + bazal ölçüm (892 satır) + hook temiz kaldırma

### ✅ F1 · Vision v2 (5/5) — 2026-08-24
- [x] ders taraması · [x] taslak · [x] sunum · [x] **sahip onayı** · [x] vision.md kökte (17 bölüm + 4 ekleme)

### ✅ F2 · REQUIREMENTS v2 (4/4) — 2026-08-25
- [x] G1–G44 türetimi · [x] çelişki tablosu · [x] başarı ölçütü (ölçüm 2026-11-30, **sahip onayı**) · [x] REQUIREMENTS + LICENSE (MIT) + README
- [x] G45–G53 eki (revizyon 3 hizalaması)

### ✅ F3 · Beyin v1 (12/12) — 2026-08-24
- [x] dosya mimarisi (T-B) · [x] STATE v1 · [x] LEDGER şeması · [x] PROFILE v1 (yerel) · [x] gitignore hibrit · [x] özet üreticisi · [x] token sayacı · [x] eşzamanlılık v1 · [x] oturum türleri · [x] kalıcı CLAUDE.md · [x] sohbet talimatı v2 · [x] test: açılış 83 satır (hedef ≤446)

### ✅ F4 · Zorlama v1 (12/12) — 2026-08-25
- [x] aioslog standardı · [x] opencode spike (bloke yüzeyi yok → tespit+log) · [x] davranış envanteri · [x]–[x] kapı çekirdeği (test 11/11 · 0/12) · [x] Claude Code adaptörü · [x] opencode adaptörü · [x] review v2 · [x] decide v2 + ledger · [x] why.py · [x] test: canlı FIRED + BLOCKED L-002

### ✅ F5 · Süreklilik + kartlar (9/9) — 2026-08-25
- [x] handoff disiplini · [x] uzun-oturum uyarısı · [x] GitHub kanalı + bundle v3 · [x] yerel-katman yedekleme · [x] oturum sihirbazı satırı · [x] EMERGENCY.md · [x] beyin kilometre taşları · [x] kuru koşu 6/6 · [x] **tatbikat: 11 saniye** (ms/f5-tamam)

### ✅ F6 · Tanıma (8/8) — 2026-08-25
- [x] kuyruk şeması (S-1..S-5) · [x] soru disiplini (CLAUDE.md, iki kez incelti) · [x] tekrar-yasak · [x] cevap→PROFILE · [x] kişilik üslup kuralı · [x] G42 verim · [x] öğrenme denetimi (audit.py) · **kapanış kanıtı:** sonraki yeni oturumda (S-1 zinciri sorulmaz + audit temiz)

### ✅ F6b · Interview Tur 1 (kampanya sürüyor) — 2026-08-25
- [x] kapsam haritası (alan başına yüzde) · [x] Tur 1: tasarım zevki + araçlar + vault ilişkisi (~%40) · [x] F7 girdisi: AIOS vault kararı · [ ] Tur 2+ (öznel kuyruk — "beni tanı" tetiklemeli)

### ✅ F7 · Kişisel bilgi deposu v1 (4/6) — 2026-08-25
- [x] vault/ kurulumu (AIOS/ içinde, gitignored) · [x] iki-vault disiplini (Documents/All salt-okunur) · [x] backup kapsamı · [x] sorgu kuralı · [ ] v2: MCP semantik arama (yalnız v1 yetmezse) · [ ] açık soru: öğrenmeler vault'a yansıssın mı (**sahip kararı**)

### ✅ F8 · Pilot (10/10) — 2026-08-25
- [x] ritüel aracı (newproject.py) · [x] pilot=ledger onayı · [x] P1–P4 eşikleri kilitli · [x] teknik kararlar (SQLite+Typer, araştırmalı, G43) · [x] ilk çalışan dilim (test 5/5) · [x] export (BRIEF #4) · [x] delete · [x] README örnekleri · [x] kapsam opt-in (.aios) · [x] kapanış: P1/P2/P3 ✅ · **P4 ⏸ ölçülemedi (kullanıcı yüzü yok) → görünürlük sonrası**

### ✅ F9 · Karar sistemi (10/10) — 2026-08-25
- [x] ADR/MCDA literatür taraması (bulgu: mevcut DECISIONS formatı uyumlu; +2 alan)
- [x] iki-katmanlı şema taslağı → **sahip onayı** (evrensel sabitler filtresi + proje ağırlıkları, 0–1)
- [x] decide.py entegrasyonu (--scores kanıt-atıf zorunlu + --sonuc-izle + --ilgili)
- [x] sentetik yanlışlama testi (atıfsız puan REDDEDİLDİ exit 1; atıflı kabul; sonuç alanı eklendi)
- [x] **sonuç-izleme** (`sonuç:` alanı + 4 hafta revisit → ağırlık kalibrasyonu)
- [x] **kademeli otonom** (CLAUDE.md kuralı + PROFILE seviyeleri)
- [x] **tartışma protokolü** (CLAUDE.md: ≥2 AI, ≤3 tur, çıktı = öneri)
- [x] **karar geri-çağırma** (CLAUDE.md prosedür: why.py → zincir → etki → plan)
- [x] DECISIONS formatına `sonuçlar:` + `ilgili:` alanları (ADR taraması bulgusu)
- [x] test: 3/3 sentetik vaka — implementasyon raporu bu commit

### 🟡 F9.5 · HTML Panosu (4/4 inşa) — fren: 1 oturum — **sahibin seçimi (a)**
- [x] üretici script: brain'den (STATE/DECISIONS/LEDGER/kapsam/ölçümler) statik HTML (pano.py, 7.6KB)
- [x] şablon: koyu/minimal modern (design-taste.md'den)
- [x] otomatik tazeleme: CLAUDE.md oturum-sonu adımı eklendi
- [x] üretim testi: Türkçe doğru, tüm bölümler, None kalıntısı yok
- [ ] **sahip testi:** tarayıcıda açılır + tasarım onayı (öznel — sahibin yargısı)

### ☐ F10 · Araştırma motoru v1 (10 adım) — fren: 3 oturum
- [ ] yöntem seçimi (G17) · [ ] araştırma hattı (soru→yöntem→kaynak→sentez→kanıt-etiketli rapor) · [ ] araştırma önbelleği · [ ] puan girdileri raporlara atıfta zorunlu · [ ] kaynak kütüğü · [ ] araştırma planı formatı (kanal önerileri + kota notu + çoklu-getiri) · [ ] sindir.py (web çıktısı: LEDGER + istek eşleşmesi + verdict) · [ ] provenance rozeti · [ ] **ilk gerçek iş: model-benchmark araştırması** (sahibin düzeltmesi) · [ ] test

### ☐ F11 · Beceri kütüphanesi (6 adım) — fren: 2 oturum
- [ ] skills/ şeması · [ ] ilk beceriler (haftalık-review, yeni-proje, derle-doğrula) · [ ] dönemsel özet (opt-in) · [ ] çağırma kuralı · [ ] test · [ ] sahip kontrolü

### ☐ F12a · Kayıt defteri + yönlendirici v1 (16 adım) — fren: 4 oturum
- [ ] model kartı şeması (Kanal Sözleşmesi) · [ ] OpenWebUI/LM Studio öncül araştırması · [ ] üretici script · [ ] **senin envanter oturumun** · [ ] limit doğrulama araştırmaları · [ ] gizlilik bölgesi · [ ]–[ ] yönlendirici v1 · [ ] registry.py --update (sözlü bildirim) · [ ] yetenek sağlayıcılar · [ ] bağımlılık grafiği · [ ] araç-yönlendirme · [ ] test

### ☐ F12b · Keşif + doğrulama hattı (8 adım) — fren: 3 oturum
- [ ] OpenRouter poller · [ ] RSS/araştırma periyodu · [ ] tetikleme merdiveni · [ ]–[ ] diff raporları · [ ] doğrulama · [ ] test

### ☐ F12c · Kota takipçisi (7 adım) — fren: 3 oturum
- [ ] kullanım defteri · [ ] yenileme pencere modeli · [ ] bildirim/düğme · [ ] Task Scheduler · [ ] yönlendirici entegrasyonu · [ ] test · [ ] devreye alma (onayın)

### ☐ F12d · Empirik zeka (8 adım) — fren: 3 oturum
- [ ] kanal sicili · [ ] tahminci · [ ] arena · [ ]–[ ] maliyet defteri · [ ] test · [ ] sahip kontrolü

### ☐ F13 · Failover (12 adım) — fren: 4 oturum
- [ ] sinyaller · [ ] geçiş kuralı (görev sınırında) · [ ] API otomatik / web öneri · [ ] test · [ ] devreye alma (onayın)

### ☐ F14 · Bağlantı (15 adım) — fren: 6 oturum
- [ ] zarf formatı · [ ] tek-yazıcı çoklu-AI'da · [ ] yürütücü=entegratör · [ ] dosya-kilit araştırması · [ ] CLI envanteri · [ ] adaptörler (subagent/Gemini CLI/API/Ollama) · [ ] delegasyon desenleri · [ ] bütçe tavanı · [ ] test

### ☐ F15 · Windows GUI uygulaması (kaba — yaklaştıkça ayrışır)
Gerçek pencere uygulaması · tasarım referansı opencode · teknoloji araştırması (S3/S4) · registry-driven paneller · parametre panelleri (kanal sözleşmesinden) · kota panosu · model matrisi · olay akışı · sohbet modu · kum havuzu/diff · deneysel: tarayıcı otomasyonu · **P4 gerçek ölçümü burada**

### ☐ F16 · Self-improvement + hata öğrenme kütüğü (kaba)
Log analizinden öğrenme (kapıya bağlı) · AI-atıf (desen/kaynak/bağlam/düzeltme) · sinyal taksonomisi işletimi · G31 döngüsü · periyodik tatbikat · çoklu-cihaz senkron · offline degrade

## 4. Token sözleşmesi

- Oturum açılışı = STATE (≤900 kelime) + PROFILE (≤400) + aktif-karar özeti. Başka hiçbir dosya varsayılan yüklenmez; **logs/ ve vault/ asla**.
- Birincil metrik: açılışta yüklenen dosya hacmi. Hedef: ≤446 satır (bazal 892'nin %50'si altı) — güncel ~92 ✅.
- Proje oturumları proje STATE + beyin özeti yükler; diğer projeler asla (G16).

## 5. Taşınanlar / arşive gidenler

**Taşınır:** kanıt etiketleri · T-A/B/C · tek-yazıcı · görünürlük≠onay · yanlışlanabilir test · fren · append-only · dört-alan · Topoloji C · markdown+git · dil kuralı · kapı dersleri · PROFILE içeriği · arşivdeki açık sorular.
**Arşive gidenler:** eski dosya yapısı · eski başarı ölçütü (F2 yenisini yazdı) · eski O-testleri · VISION-ANALYSIS · eski araç implementasyonları (davranış envanteriyle dersler taşındı).

## 6. Riskler

| Risk | Erken sinyal | Önlem |
|---|---|---|
| Canlı test yapılmadan güven | hook kuruldu, restart testi yok | sahibin restart testleri (F4 kapanış koşulu) |
| Meta-döngü | PLAN dışı plan dosyası | yasak; §8 yeter |
| Arşiv unutulması | dersler v2'lere girmedi | F1 açık adımı + why.py |
| Açılış bağlamı büyür | >446 satır | digest kalitesi + budama (eşik değişmez) |
| opencode plugin çalışmaz | session.idle gelmez | plugin revize veya tek-kanal belgelenir |
| Tempo kayması (öğrenci ritmi değişken) | 2 hafta sessizlik | duraklama sinyali → sahip kararır |
| Yerel katman kaybı | backup yok | F5 yedekleme rutini |
| Eşzamanlı yazım | iki oturum aynı dosyada | v1 tek-oturum, F14 kilidi |
| GUI inşası şişer | F15 çekirdeği geciktirir | uygulama son fazda; istemci ilkesi |
| Log gürültüsü | logs/ büyür | rotasyon + review örnekler |
| Ölçek çekimi | çekirdek fazları platform detayına yenik düşer | pilot-önce + her fazın tek-başına-değer kuralı |
| İzleme maliyeti | gözlemci koşuları pahalı kanallarda | ücretsiz/boş kanallara (dogfooding) + merdiven |
| Web otomasyon kırılganlığı | otomasyon sık kırılır | manuel-first + sindir.py |
| Bayat model kartı | son-doğrulanma eski | review uyarısı + sözlü bildirim + keşif hattı |
| P4 ölçümü yine ertelenir | görünürlük sonrası da algı oluşmuyorsa | F15 sonrası zorunlu ölçüm noktası |

## 7. Faz kapanış formatı ve kapılar

**Sahip Doğrulama Kapısı:** komutla doğrulanabilen her şey Claude'da; sahibe yalnız (1) erişilemez ortamlar, (2) kararı/beyanı gerekenler, (3) öznel yargı verilir.
**Araştırılabilirlik filtresi:** objektif sorular sahibe sorulmaz — F10 hattına gider.

`F<n>: bitti/kısmi | test: <sonuç> | fren: <durum> | kanıt: <çıktı> | sahip testi: <geçti/yok/bekliyor> | sonraki: F<n+1>`

## 8. İlerleme günlüğü

| Tarih | Olay | Durum |
|---|---|---|
| 2026-08-23 | F0–F2 + PLAN v1 | ✅ |
| 2026-08-24 | F3–F5 inşaları + F4 canlı testler | ✅ |
| 2026-08-24 | PLAN revizyon 3 (platform genişlemesi) | ✅ |
| 2026-08-25 | F6 canlı döngü + F6b Tur 1 + F7 v1 + F8 pilot (P1–P3 ✅, P4 ⏸) | ✅ |
| 2026-08-25 | PLAN revizyon 4 (yürütme haritası, checkbox'lı) | ✅ bu dosya |

## 9. İzlenebilirlik — sahibin istekleri ↔ plan (2026-08-24 denetimi + ekler)

**Özet:** 61+ ayrı istek → 50+ tam karşılık · 7 belirli faza ertelenmiş (G9) · 4 fiziksel sınır + çözüm · **0 görmezden gelinen, 0 basitleştirilen.**

| Alan | İstek | Karşılık |
|---|---|---|
| Kimlik | Platform; tüm AI araçları; normal sohbet | vision §1; oturum türleri (F3); F15 |
| Beyin | Unutma yok; onay/red/erteleme; gerekçe | G5/G6; LEDGER (çalışıyor) |
| Tanıma | Karakter/tercih; sohbet sinyalleri; **derin interview** | PROFILE; F6; F6b kampanya (sürüyor) |
| Kaynak zekası | Otomatik seçim; ücretsiz önce; keşif; kota; sözlü bildirim; matris; Grok/Kimi/MiniMax; yerel | G10–G13; F12a/b/c/d |
| Karar | 0–1 puanlama; araştırma beslemesi; evrensel sabitler; proje ağırlıkları; devri senaryosu; tartışma; sonuç-izleme; geri-çağırma | G15–G22; F9 |
| Araştırma | Özel motor; önbellek; sindir; benchmark işleri | G14; F10 |
| Arayüz | Windows GUI; opencode tasarım; kaynak-türü panelleri; sohbet modu; kum havuzu | G23–G25; F15 |
| Süreklilik | Handoff; tatbikat (11 sn kanıt); kurtarma; km taşları | G36/G37/G42; F5 |
| Modülerlik | Ekle/çıkar basit; kayıt defteri; bağımlılık grafiği; açık kaynak | Yasalar; G24/G29/G30/G35 |
| Loglama | Tek standard; 3-satırlı hata; öğrenmeye dönüşüm | G32–G34; F4 (çalışıyor) |
| Token/dikkat | Açılış minimal; sayaç; dikkat kriteri | G26–G28 (90 satır ✅) |
| Süreç | Uzun plan; asla acele yok; her adımda test; sor; birlikte doğrula | 17 faz ~168 adım; SDK; frenler |
| **Tanıma derinliği** (itiraz) | "3 soruyla neremi anladın" | **F6b kampanya** (sürüyor, kapsam %40→%80) |
| **Mekanizma≠değer** (sistemik ders) | içerik kampanyası adımları | F8 pilot · F12a envanter · F12b koşular · F10 benchmark |
| **Empirik zeka + güven** | sicil/tahminci/arena/provenance/denetim/kum havuzu | F12d/F9/F10/F15 |
| **Dayanıklılık** | km taşları/bağımlılık/çoklu-cihaz/offline | F5/F12a/F16 |

## 10. Karar noktaları (açık sahibin kararları)

| Karar | Ne zaman |
|---|---|
| Öğrenmeler vault'a yansıssın mı? | F7 kapanışında |
| P4 gerçek ölçümü | F15 sonrası (veya görünürlük yeterli olursa erken) |
| Analitik Sistemi → AIOS yönetimine dönüş | F8 pilot sonrası sahibin çağrısıyla |
| GUI teknolojisi (S3/S4) | F15 başlangıcında |
