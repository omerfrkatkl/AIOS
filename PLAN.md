# PLAN — AIOS sıfırdan yeniden inşa

| | |
|---|---|
| **Amaç** | Restukturizasyonun tek yetkili haritası: kalıcı beyin + çoklu-AI senkronu + tanıma + kaynak zekası + puanlamalı karar sistemi + Windows uygulama yüzeyi |
| **Yaşam döngüsü** | Fazlar ilerledikçe yerinde güncellenir; §8 İlerleme tablosu her oturum sonunda tazelenir |
| **Sahip** | Proje sahibi (yön onayları) · Claude (yürütme) |
| **Okuma tetikleyicisi** | Her oturum açılışı + her faz başı + haftalık kontrol |

> Bu dosya onaylı planın kendisidir; dışında plan dosyası açılmaz (meta-döngü koruması).
> **Ölçek beyanı (sahip 2026-08-24):** bu platform "tüm AI araçlarının birleşimi" hedefindedir — Open WebUI / LM Studio / router / araç-birleştirici sınıfı araçların kesişimi tek çatıda. Kapsam küçültülmez, acele edilmez; her faz tek başına değer üretir.

## 0. Hedef, ilkeler ve mimari yasalar

**Tek cümle:** Hangi AI'yi, hangi arayüzden, hangi modelle kullanırsam kullanayım aynı davranan; unutmayan; beni tanıyan; token-verimli; kararlarını araştırmaya dayalı puanlamayla doğrulayan; fikirden sonuca beni yönlendiren kişisel AI platformu.

**Kuzey-yıldızı ölçeği:** "tek cevap ve sıradan sohbet"ten "yıllarca sürecek proje"ye aynı sistem; API, CLI, chat arayüzü, yerel model — hepsi bağlanabilir.

**Taşınan ilkeler:** kanıt etiketleri `[gözlendi]/[üretildi]/[varsayıldı]` · T-A/B/C karar katmanları · tek-yazıcı · görünürlük ≠ onay · yanlışlanabilir test (eşik veri öncesi sabit) · fren = sayı + takvim · append-only kayıtlar · dört-alanlı dosya kuralı · Topoloji C · markdown+git kaynak-of-truth · dil kuralı (makine İngilizce, kayıt Türkçe, eşleştirme anahtarları iki dilli) · **asla acele yok.**

**Mimari yasalar (modülerlik — F1'den F15'e her yere işlenir):**
1. **Sözleşme-first:** her bileşenin girdi/çıktı sözleşmesi yazılıdır (dosyalar için dört alan).
2. **Kayıt-defteri-güdümlü:** araçlar/yetenekler kendini manifest'e kaydeder; yüzeyler koddan değil kayıt defterinden okur — yeni araç otomatik görünür, çıkarmak bir satırdır.
3. **Gevşek bağlı:** çekirdek hiçbir araca, arayüze veya sağlayıcıya sıkı bağlı olamaz.
4. **Yüzeyler istemcidir, beyin egemendir:** uygulama olmasa da sistem çalışır.
5. **Append-only veri, idempotent araçlar:** aynı komut iki kez koşarsa zarar vermez.
6. **Tek sorumluluk:** her dosya/script tek iş yapar.
7. **Kanal Sözleşmesi:** her kaynak (lokal/API/router/web-chat) aynı sözleşmeyi imzalar — `{tür, parametreler[], girdiler[], limitler{}, yetenekler[], enforcement: block|post-hoc|none, dosya-erişimi}`. UI bu sözleşmeden çizer (web'de sahte slider yok), yönlendirici bundan seçer, zorlama buna göre davranır. Yeni kaynak = yeni sözleşme dosyası.

**Katmanlar (mimari karar kaydının güncel hali):** BEYİN (sözleşmeli dosyalar) · ZORLAMA (bağımsız araçlar) · **GÖZLEMCİ (zamanlayıcı + izleyiciler: keşif, doğrulama, kota takibi; merdiven: manuel → Task Scheduler → uygulama içi)** · YÜZEY (istemciler) · YÜK (yönetilen projeler).

## 1. Sıfırlama kuralı

- Aktif kök yalnızca yeni sistemin dosyalarını içerir; eski hiçbir kural/state yüklenmez.
- `arsiv/`: eski sistemin tamamı — **girdi değil, referans**.
- git geçmişi aynen korunur (aynı repo).
- Beyanlı istisnalar: PLAN.md kendisi + geçici bootstrap CLAUDE.md (F3'te yenisiyle değişir) + yeni DECISIONS.md (F0'da başladı).
- Yönetilen projelere (KB, ledger, PDF360, DC, DNS) dokunulmaz.
- **Kabul edilmiş risk:** F0–F4 arasında zorlama yok. Erken sinyal: kapısız yoğun günlük kullanım → F4 öne çekilir.
- **Geri dönüş:** `arsivden-geri-don.ps1` (v3 log'u arsiv/DECISIONS-v3.md'ye güvene alır).

## 2. Gizlilik mimarisi (hibrit — sahip kararı 2026-08-23)

| Bölge | İçerik |
|---|---|
| **Public (git)** | PLAN, vision, REQUIREMENTS, CLAUDE.md, PROJECT-INSTRUCTIONS, tools/, hooks/, adapters/, tests/, LICENSE (MIT), DECISIONS (sistem kararları), STATE (kişisel-detay-yazmama disipliniyle) |
| **Yerel (gitignored + bundle senkronu)** | PROFILE, LEDGER (kişisel kayıtlar), sağlayıcı envanteri, kişisel state detayları, logs/ |

Sonuçları: yerel katmanın git yedeği yok → F5'te bundle-tabanlı yedekleme; sohbet PROFILE'ı raw'dan çekemez → sihirbaz diskten okur, sohbette bundle. Obsidian vault (F7) yereldir, asla repo'ya girmez.

## 3. Yol haritası — 17 faz (F12 dört alt dilimli), ~155 adım

Fren semantiği: **inşaat fazlarında** fren = duraklama dedektörü (2 hafta oturum yok → sahip devam/ara/terk karar verir); **yalnız F8 pilotu** katı yanlışlanabilir frenle kapanır.

### F0 · Sıfırlama (6 adım) — ✅ BİTTİ (2026-08-23, commit 76e1b9d)
Arşiv + yeni DECISIONS + geri-dönüş scripti + geçici CLAUDE.md + bazal ölçüm (892 satır / 77.447 bayt) + hook'un temiz kaldırılması.

### F1 · Vision v2 (5 adım) — fren: 2 oturum
1. Arşiv ders taraması → ders listesi · 2. Taslak (tüm netleşmelerle) · 3. Sahibe sunum → revizyon · 4. **Sahip onayı (T-A kapısı)** · 5. `vision.md` köke + kapanış kaydı.
**Test:** sahibin açık onayı.

### F2 · REQUIREMENTS v2 (4 adım) — fren: 2 oturum
1. G-türetimi: limit envanteri · failover · puanlama-nesnelliği · 3-durum hafıza · token sözleşmesi · yönlendirilmiş akış · açık-kaynak standartları · kademeli otonom · **modülerlik yasası** · **loglama/hata standardı** · **yetenek sağlayıcılar** · **teslim biçimi: Windows GUI uygulaması (opencode tasarım referansı)** · araştırma motoru
2. Çelişki tablosu: platform↔token · otonom↔sahiplik · açık-kaynak↔gizlilik (hibrit ile çözüldü)
3. **Yeni başarı ölçütü → sahip onayı** (yanlışlanabilir + ölçüm tarihli)
4. `REQUIREMENTS.md` + `LICENSE` (MIT) + `README` köke
**Test:** her yeni G yanlışlanabilir formda.

### F3 · Beyin v1 (11 adım) — fren: 3 oturum
1. Dosya mimarisi kararı (T-B) + **mimari karar kaydı** (katmanlar + sözleşmeler) · 2. STATE v1 + tavan · 3. LEDGER şeması (`approved|rejected|deferred` + `revisit:` + PENDING→insan onayı + iki dilli anahtarlar) · 4. PROFILE v1 (çalışma + kişilik + soru kuyruğu; arşivdeki açık sorular taşınır) — **yerel** · 5. .gitignore tasarımı (hibrit) · 6. Aktif-karar özeti üreticisi · 7. Token sayacı (birincil: açılışta yüklenen dosya hacmi) · 8. Eşzamanlılık kuralı v1 (tek aktif oturum) · 8b. **Oturum türleri:** proje / sohbet / araştırma — sohbet oturumu STATE/DECISIONS'a varsayılan yazmaz; yalnız yapılandırılmış sinyaller akar (tercih / hata / düzeltme / onay / erteleme — F16 taksonomisi) · 9. **Kalıcı CLAUDE.md** (geçicinin yerine) · 10. **Sohbet talimat dosyası v2** · 11. **Test:** açılış bağlamı ≤ bazalın %50'si

### F4 · Zorlama v1 (12 adım) — fren: 3 oturum
1. **Log/hata standardı** (JSONL şeması + "ne oldu/neden/ne yapmalısın" kullanıcı formatı; logs/ yerel, bağlamaya asla yüklenmez) · 2. **opencode fizibilite spike'ı** (≤ yarım gün; yoksa zayıf-zorlama sınırı belgelenir) · 3. Kapı davranış envanteri arşivden (sidechain atlama, `stop_hook_active` koruması, UTF-8/BOM, uzun-oturum uyarısı, `--demo`, toleranslı eşleştirme) · 4–6. Kapı çekirdeği (taşınan test setiyle TDD) + üç-durum davranışı · 7. Claude Code adaptörü + install · 8. opencode adaptörü · 9. review v2 (kütük sağlığı, revisit, token trendi, tavan, işaretçi, **log sağlığı**) · 10. decide v2 + ledger aracı · 11. **why.py** (aktif + arşiv) · 12. **Test:** taşınan set %100 · R-002 bloke · deferred uyarı · çift-kurumsız install

### F5 · Süreklilik + kartlar (8 adım) — fren: 2 oturum
1. Handoff disiplini · 2. uzun-oturum uyarısı · 3. GitHub kanalı + bundle · 4. **yerel-katman yedekleme rutini** · 5. **oturum açılış sihirbazı** · 6. **acil durum kartı** · 7. **beyin kilometre taşları** (isimli anlık görüntü aracı: `aios tag` + diff — "bu tarihte beyin neydi?") · 8. **kuru koşu** (mini-işle tüm hat) · 9. **Test:** sıfır-bağlam devam + **süreklilik tatbikatı prototipi** (farklı araç, sıfır bağlam, ≤15 dk devam)

### F6 · Tanıma (8 adım) — fren: 3 oturum
Adaptif soru döngüsü: kuyruk şeması · tekrar-yasak · cevap→PROFILE (kanıt etiketli) · kişilik üslup kuralı · G42 verim ölçütü · **öğrenme denetimi** (öğrenme diff'i: "bu hafta bunları öğrendim — doğru mu?" → onay/düzelt/sil; yanlış-preferans sürüklenmesine karşı unlearning). **Test:** 2 ardışık oturum tekrarsız. Sahip kontrolü: soru kalitesi.

### F7 · Kişisel bilgi deposu (6 adım) — fren: 2 oturum
1. Vault kategori haritası (mevcut yapıdan) · 2. **v1: araç-bağımsız hedefli dosya erişimi** (tam-vault okuma yasak) · 3. v2: MCP semantik arama (yalnız v1 yetmezse) · 4. sorgu disiplini kuralı · 5. **Test:** 5 örnek soru vault'tan, sorgu başına ≤ hedef not · 6. sahip kontrolü

### F8 · Pilot (10 adım) — **KATI fren: 4 çalışma oturumu VEYA 6 hafta; dolursa negatif bulguyla kapanır**
1. **Yeni-proje ritüeli** (tek komut: BRIEF + git init + MIT + README/CHANGELOG + STATE iskeleti + işaretçi) · 2. pilot seçimi (ledger aday, onayınla) + P-ölçütleri · 3–9. dilimler AIOS sürer (G43 sınavı) · 10. değerlendirme raporu

### F9 · Karar protokolü v3 (14 adım) — fren: 3 oturum
Literatür taraması (ADR/MCDA) · **iki-katmanlı puanlama: (1) evrensel sabitler = geçiş filtresi (modülerlik, loglama, hata yönetimi, açık kaynak — ihlal ≈ eleme, ağırlık değil); (2) proje ağırlıkları = sahibin beyanı ("bu projede hız önce"), proje başına kayıtlı; ölçek 0–1 normalize** · boyut/ağırlık şeması → **onayın** · kapanış kuralı (G21) · kanıt-etiketli puan formatı (kafadan puan geçersiz) · decide entegrasyonu · **karar sonuç-izleme** (sonuç alanı + revisit → kalibrasyon) · **kademeli otonom** (alan-bazlı güven seviyesi) · **tartışma protokolü** (≥2 AI, ≤3 tur, farklı sağlayıcı tercih, çıktı = karar hattına giren öneri) · **karar geri-çağırma** (etki analizi + geri alma planı). **Test:** kafadan-puan vakası reddedilir.

### F10 · Araştırma motoru v1 (10 adım) — fren: 3 oturum
Yöntem seçimi (G17) · araştırma hattı (soru→yöntem→kaynak→sentez→**kanıt-etiketli rapor**) · **araştırma önbelleği** (aynı soru → önce geçmiş rapor + tazelik kontrolü) · **puan girdileri raporlara atıfta zorunlu** · kaynak kütüğü · **araştırma planı formatı** (sahibin senaryosu: görev → kanal önerileri + kota notu ["Claude limiti bitiyor, yarım saat kaldı"] + çoklu-getiri ["üçünü birden yaptır"]) · **sindir.py** (web çıktısı yapıştırılır → LEDGER taraması + istek eşleşmesi + verdict; web AI'ın dosya erişimi olmadan doğrulayamadığını sistem telafi eder) · **provenance rozeti** (artefakt üstverisi: hangi model/kanal/raporlar/kanıt). **Test:** örnek soruda rapor üretilir; önbellek isabeti; sindir örnek çıktıda verdict.

### F11 · Beceri kütüphanesi (6 adım) — fren: 2 oturum
skills/ şeması (dört-alanlı, sürümlü) · ilk beceriler (haftalık-review, yeni-proje, derle-doğrula) · **dönemsel özet (opt-in)** · çağırma kuralı. **Test:** tekrarlanan akış skill'den koşar.

### F12a · Kayıt defteri + yönlendirici v1 (16 adım) — fren: 4 oturum
1. **Model kartı şeması** — model başına bir dosya: `{tür: lokal/api/router/web-chat, parametreler[] (lokal: tam; api: kısmi; web: boş — dürüst UI), girdiler[] (metin/dosya/görsel/video), limitler{dosya_mb, karakter, istek_penceresi, yenileme}, yetenekler[] (web-arama, artifact, deep-research...), enforcement: block|post-hoc|none, dosya-erişimi, son-doğrulanma, kaynak}` · 2. **öncül araştırma: OpenWebUI/LM Studio yetenek seti** (referans) · 3. **üretici script** (scoop/uv/ollama taraması) · 4. **senin envanter oturumun** (Claude Pro, Gemini Pro, ChatGPT free, Qwen chat, Gemini API, Ollama, Grok/Kimi/MiniMax adayları) · 5. limit doğrulama araştırmaları · 6. gizlilik: kişisel kullanım verisi yerel bölgede; yetenek matrisi public olabilir · 7–10. yönlendirici v1 (görev→kabiliyet; aday sıralama: uygunluk+boş-kota+maliyet; "Flash medium yeter" tarzı öneri) · 11. **registry.py --update: sözlü bildirim kanalı** (sahip "artık 50 MB" der → anında merkezi kayıt, eski değer geçersiz, sonraki tüm yönlendirme güncel) · 12–13. **yetenek sağlayıcılar** (yeteneği olmayan kanala araç takma; MCP/CLI sarmalayıcı) · 14. **bağımlılık grafiği** (hangi skill/aracın hangi kanala bağlı — çıkarma öncesi etki raporu) · 15. araç-yönlendirme tek sorguda · 16. **Test:** 5 örnek görevde tutarlılık + sözlü güncelleme vakası + review bayatlık denetimi

### F12b · Keşif + doğrulama hattı (8 adım) — fren: 3 oturum (GÖZLEMCİ katmanı)
1. **OpenRouter model-API poller'ı** (ücretsiz/sınırsız modeller otomatik tespit) · 2. **RSS/araştırma periyodu** (yeni araçlar, ajan yapıları, model güncellemeleri) · 3. tetikleme merdiveni: v1 manuel komut/buton → F12c'de Task Scheduler → F15'te uygulama içi · 4–6. **diff raporları**: "yeni model X (ücretsiz)", "limit 20→50 MB", "eski model yerine artık bu" — olay akışına düşer, sahibe bildirilir · 7. doğrulama: API'de probe, web-chat'te araştırma + sahip onayı · 8. **Test:** sahte yeni-model vakası → diff raporu üretilir

### F12c · Kota takipçisi (7 adım) — fren: 3 oturum (GÖZLEMCİ katmanı)
1. **Kullanım defteri** (kanal başına tüketim kaydı) · 2. **yenileme pencere modeli** ("Claude doldu → 3 saat sonra yenilenir" — o sürede yönlendirmez) · 3. web-chat'te sahibin tek kelimelik bildirimi/düğmesi; API'de otomatik (429) · 4. Task Scheduler entegrasyonu (uygulama yokken de çalışır) · 5. yönlendirici entegrasyonu: tükenmiş/uyumsuz kanal elenir, doğrulanmamış hücre seçilmez · 6. **Test:** sahte tükenme → yönlendirici o kanalı atlar · 7. devreye alma: **onayın**

### F12d · Empirik zeka (8 adım) — fren: 3 oturum (F12c verisi birikince)
1. **Kanal sicili** (kanal × görev-türü başarı sicili; yönlendirici statik spec'ten empirik seçime evrilir) · 2. **tahminci** ("bu araştırma Gemini DR'de ~50k token ≈ bedava; Claude'da kotanın %8'i") · 3. **arena** (aynı görev 2–3 kanala; çıktılar yan yana kanıt-etiketli; hüküm sahibin; sonuçlar sicili besler) · 4–6. maliyet defteri (ücretli kanallarda aylık gerçek harcama) · 7. **Test:** sicil verisiyle yönlendirme önerisi değişimi gösterilir · 8. sahip kontrolü

### F13 · Failover (12 adım) — fren: 4 oturum
Sinyaller (429 / elle bildirim / tahmin) · geçiş kuralı (**görev sınırında**, bağlam beyinden tohumlanır) · API'de otomatik, web-chat'te öneri · **Test:** sahte 429 → geçiş · devreye alma: **onayın**

### F14 · Bağlantı (15 adım) — fren: 6 oturum
Zarf formatı (özet+kanıt+bağlantı) · tek-yazıcı çoklu-AI'da · **yürütücü = entegratör** (alt-AI yapılandırılmış çıktı üretir, beyne yalnız yürütücü yazar) · dosya-kilit araştırması · CLI çağrılabilirlik envanteri · adaptörler (subagent, Gemini CLI, API, Ollama) · delegasyon desenleri (**araştırma devri**, paralel keşif, çapraz review, iş-bölümü) · **görev başına bütçe tavanı** · **Test:** iki kanal tek state'te, çift-yazım yok

### F15 · Windows GUI uygulaması (kaba — yaklaştıkça ayrışır; fren o zaman sabitlenir)
**Gerçek pencere uygulaması** (terminal değil) · **tasarım referansı: opencode** (tasarım olduğu gibi/uyarlanarak alınır — tasarım emeği sıfıra yakın, sistem %100 bizim) · teknoloji seçimi araştırmayla (S3/S4; ölçütlerden biri: opencode tasarım-taşınabilirliği) · uygulama = istemci, araçları **kayıt defterinden** okur · **parametre panelleri kanal sözleşmesinden çizilir** (lokal: temperature/max_tokens tam kontrol; API: kısmi; web: dürüst-boş — sahte slider yok) · iç görünümler: model seçici, tartışma arayüzü, araştırma görünümü, **kota panosu**, **model matrisi**, **olay akışı**, durum panosu, log görüntüleyici, **sohbet modu**, **kum havuzu/diff önizleme** (kalıcı etkili işlemler diff'le onaylanır) · deneysel modül: tarayıcı otomasyonu (Playwright — kırılganlık/kullanım-şartları riski nedeniyle sonraya)

### F16 · Self-improvement + hata öğrenme kütüğü (kaba — yaklaştıkça ayrışır)
Log analizinden tekrarlanan-hata öğrenmesi (kapıya bağlı) · **hata kayıtlarında AI-atfı** (desen + kaynak AI + bağlam + sonuç + düzeltme; "kim suçlu" değil "ne tekrarlanmasın" odağı; web kaynaklılar sindir ile yakalanır) · sohbet sinyal taksonomisi işletimi (F3 oturum türleriyle) · G31 döngüsü · periyodik süreklilik tatbikatı · **çoklu-cihaz yerel-katman senkronu** (şifreli; yıllarca kullanım gelecek-güvencesi) · **offline degrade modu** (yerel modeller + önbellekteki raporlarla kısıtlı çalışma; çevrimdışı yetenekler envanterde işaretli)

## 4. Token sözleşmesi

- Oturum açılışı = STATE (≤900 kelime) + PROFILE (≤400) + aktif-karar özeti. Başka hiçbir dosya varsayılan yüklenmez; **logs/ asla**.
- Birincil metrik: açılışta yüklenen dosya hacmi; vekil: transcript boyutu. Hedef: F3 sonunda bazalın (892 satır) ≥%50 altı.
- Proje oturumları proje STATE + beyin özeti yükler; diğer projeler asla (G16).

## 5. Taşınanlar / arşive gidenler

**Taşınır:** kanıt etiketleri · T-A/B/C · tek-yazıcı · görünürlük≠onay · yanlışlanabilir test · fren · append-only · dört-alan · Topoloji C · markdown+git · dil kuralı · kapı tasarım dersleri · PROFILE içeriği · arşivdeki açık sorular.
**Arşive gider:** eski dosya yapısı · eski başarı ölçütü (F2 yenisini yazar) · eski O-testleri · VISION-ANALYSIS · eski araç implementasyonları (davranış envanteriyle dersleri taşınır).

## 6. Riskler

| Risk | Erken sinyal | Önlem |
|---|---|---|
| F0–F4 zorlama boşluğu | kapısız yoğun kullanım | F4 öne çekilir |
| Meta-döngü | PLAN dışı plan dosyası | yasak; §8 yeter |
| Arşiv unutulması | dersler v2'lere girmedi | F1 açık adımı + why.py |
| Token hedefi tutmaz | F3 testi kaldı | eşik değil yöntem gözden geçirilir |
| opencode plugin/hook yetmez | spike başarısız | tek kanal + sınır belgelenir |
| Tempo kayması | 2 hafta sessizlik | duraklama sinyali → sahip kararır |
| Yerel katman kaybı | bundle yok | F5 yedekleme rutini |
| Eşzamanlı yazım | iki oturum aynı dosyada | v1 tek-oturum, F14 kilidi |
| GUI inşası şişer | F15 kapsamı eriyip çekirdeği geciktirir | uygulama son fazda; istemci ilkesi |
| Log gürültüsü | logs/ büyür, faydasız | rotasyon + review yalnız örnekler |
| **Ölçek çekimi** (platform vizyonu her şeyi yutar) | çekirdek fazları platform detayına yenik düşer | pilot-önce sırası + her fazın tek-başına-değer kuralı |
| **İzleme maliyeti** (keşif/araştırma periyotları token yer) | gözlemci koşuları pahalı kanallarda | izleme ücretsiz/boş kanallara (dogfooding) + tetik merdiveni |
| **Web otomasyon kırılganlığı** (Playwright yolunda arayüz değişir) | otomasyon sık kırılır | manuel-first + sindir.py; otomasyon deneysel modül |
| **Bayat model kartı** (limit değişti, kayıt eski) | son-doğrulanma eski | review bayatlık uyarısı + sözlü bildirim kanalı + keşif hattı |

## 7. Faz kapanış formatı ve Sahip Doğrulama Kapısı

**Sahip Doğrulama Kapısı (revize 2026-08-23 — sahip isteği):** Claude, komutla doğrulanabilen **her şeyi kendisi** doğrular ve kanıtıyla raporlar. Sahibe yalnızca şu üç tür test verilir:
1. **Erişemediğim ortamlar:** canlı oturumlar (Claude Code restart, opencode), diğer uygulamalar (Obsidian, web-chat), başka makineler.
2. **Sahibin kararı/beyanı gerekenler:** onay tarihleri, envanter verisi, pilot seçimi, "yeterli mi" yargısı.
3. **Öznel değerlendirme:** tasarım beğenisi, çıktı kalitesi algısı, tempo yargısı.

`F<n>: bitti/kısmi | test: <sonuç> | fren: <durum> | kanıt: <çıktı/komut> | sahip testi: <geçti/yok/bekliyor> | sonraki: F<n+1>`

## 8. İlerleme

| Tarih | Faz/adım | Durum | Not |
|---|---|---|---|
| 2026-08-23 | PLAN yazıldı | ✅ | F0 ile birlikte |
| 2026-08-23 | F0 · adım 1–6 | ✅ bitti | arşiv + sigorta + bazal 892 satır/77.447 bayt; hook temiz kaldırıldı; commit 76e1b9d |
| 2026-08-23 | PLAN revizyon 2 | ✅ | 17 faz: +F10 Araştırma motoru, F15 Windows GUI (opencode tasarım ref.), modülerlik yasası, log standardı, yetenek sağlayıcılar, tartışma, geri-çağırma, tatbikat |
| 2026-08-23 | F1 · Vision v2 | ✅ bitti | ders listesi (10 kalem) + taslak sunuldu → **sahip onayı** → vision.md kökte (17 bölüm) · DECISIONS'a T-A kapanış girişi |
| 2026-08-23 | F2 · REQUIREMENTS v2 | ✅ bitti | 44 G (yanlışlanabilir) + T/H/S + çelişki tablosu + **başarı ölçütü (ölçüm 2026-11-30)** → **sahip onayı** · LICENSE (MIT) + README eklendi |
| 2026-08-23 | Kural: Sahip Doğrulama Kapısı | ✅ | her elle tutulur değişiklik sahibin testinden geçer; §7 güncellendi (sahip isteği) |
| 2026-08-24 | Kural revizesi (sahip isteği) | ✅ | Claude komutla doğrulanabilir her şeyi kendisi doğrular; sahibe yalnız erişilemez ortamlar / kararı-beyanı gerekenler / öznel yargı verilir |
| 2026-08-24 | F3 · Beyin v1 | ✅ bitti | TUR1: STATE v1 (282 kelime) + LEDGER şeması (active: alanı) + PROFILE v1 (296 kelime, yerel) + hibrit gitignore + kalıcı CLAUDE.md + sohbet talimatı v2 · TUR2: tools/summary.py (4-vakalı sentetik test geçti) + tools/context_cost.py · TUR3: mimari karar kaydı (T-B) · **açılış 83 satır / 4424 bayt — hedef ≤446 TUTTU** · commit a2daebc + F3 kapanışı |
| 2026-08-24 | F4 · Zorlama v1 | ✅ inşa bitti — **sahibin canlı testi bekliyor** | aioslog standardı · kapı v3 (3-durum, davranış envanteriyle) · test **11/11 + 0/12** · demo L-002 bloke · deferred 4-vaka · LEDGER göçü (L-001..L-006) · Claude Code adaptörü kuruldu · opencode adaptörü (spike: bloke yüzeyi yok → tespit+log) kuruldu · review/decide/ledger/why · **bekleyen: sahibin Claude Code + opencode restart testleri** |
| 2026-08-24 | PLAN revizyon 3 | ✅ | platform genişlemesi: Kanal Sözleşmesi (yasa #7), GÖZLEMCİ katmanı, F12a/b/c/d, oturum türleri, iki-katmanlı puanlama, sindir.py, araştırma planı, provenance, öğrenme denetimi, kilometre taşları, bağımlılık grafiği, arena/tahminci/sicil, GUI kapsamı, F16 atıf+senkron+offline; §9 izlenebilirlik eki (sahibin 58 isteği satır satır) |
| → | F4 canlı testleri | **sahipte** | Claude Code restart → FIRED; opencode restart → rejected ifade → BLOCKED (surface=opencode) |
| → | F5 · Süreklilik + kartlar | sıradaki | canlı testler sonrası başlar |

## 9. İzlenebilirlik — sahibin istekleri ↔ plan (2026-08-24 denetimi, sahip onaylı)

**Özet:** 58 ayrı istek → 47 tam karşılık · 7 belirli faza ertelenmiş (G9) · 4 fiziksel sınır + tasarlanmış çözüm · **0 görmezden gelinen, 0 basitleştirilen.**

| Alan | İstek | Karşılık |
|---|---|---|
| Kimlik | Uygulama değil platform; tüm AI araçları içinde; normal sohbet de | vision §1; oturum türleri (F3); F15 sohbet modu |
| Beyin | Unutma yok; onay/red/erteleme hafızası; gerekçe saklanır | G5/G6; LEDGER (F3/F4 — çalışıyor) |
| Tanıma | Karakter/tercih; sohbet sinyalleri kayda geçsin | PROFILE (F3); F6 adaptif + öğrenme denetimi; F16 sinyal taksonomisi |
| Kaynak zekası | Otomatik model/efort/sağlayıcı; ücretsiz önce; keşif; limit bitince geçiş; kısıt matrisi; canlı kota; sözlü bildirim; RSS/periyot/manuel; Grok/Kimi/MiniMax; yerel model | G10–G13; F12a/b/c/d; F13; Gözlemci katmanı |
| Karar | 0–1 puanlama; derin araştırma beslemesi; evrensel değişmezler; proje ağırlıkları; araştırma devri senaryosu; tartışma (≤3 tur); sonuç-izleme; geri-çağırma; kapanış kuralı; önerilerim de otomatik doğru değil | G15–G22; F9 iki-katman; F10 plan formatı + atıf zorunluluğu |
| Araştırma | Özel motor; yöntem seçimi; önbellek; sindir (web çıktısı doğrulama) | G14; F10 |
| Arayüz | Windows GUI; opencode tasarım ref.; kaynak-türü bazlı parametre panelleri; muazzam arayüz; sohbet modu; kum havuzu/diff | G23–G25; F15 |
| Süreklilik | Uzun oturum fark edilir; handoff; tatbikat; kurtarma; kilometre taşları | G36/G37/G42; F5 |
| Modülerlik | Ekle/çıkar basit; kayıt defteri; bağımlılık analizi; açık kaynak | Yasalar 2–3; G24/G29/G30/G35; F12a grafik |
| Loglama | Tek standard; 3-satırlı kullanıcı hatası; öğrenmeye dönüşüm | G32–G34; F4 (çalışıyor) |
| Token/dikkat | Açılış minimal; sayaç; dikkat kriteri | G26–G28 (açılış 82 satır) |
| Süreç | 100 aşamaya kadar plan; asla acele yok; her adımda test (ikimizin); sor; birlikte doğrula | 17 faz ~155 adım; SDK; frenler; yanlışlanabilir testler |
| Bilinçli sınırlar | Web-chat kotası dışarıdan okunamaz; opencode bloke yüzeyi yok; tartışma karar vermez; sohbet ham yazılmaz | Her biri için tasarlanmış çözüm (§3 ilgili faz + §6 risk) |
