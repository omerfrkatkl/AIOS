# PLAN — AIOS sıfırdan yeniden inşa

| | |
|---|---|
| **Amaç** | Restukturizasyonun tek yetkili haritası: kalıcı beyin + çoklu-AI senkronu + tanıma + kaynak zekası + puanlamalı karar sistemi |
| **Yaşam döngüsü** | Fazlar ilerledikçe yerinde güncellenir; §8 İlerleme tablosu her oturum sonunda tazelenir |
| **Sahip** | Proje sahibi (yön onayları) · Claude (yürütme) |
| **Okuma tetikleyicisi** | Her oturum açılışı + her faz başı + haftalık kontrol |

> Bu dosya onaylı planın kendisidir; dışında plan dosyası açılmaz (meta-döngü koruması).

## 0. Hedef ve ilkeler

**Tek cümle:** Hangi AI'yi, hangi arayüzden, hangi modelle kullanırsam kullanayım aynı davranan; unutmayan; beni tanıyan; token-verimli; kararlarını araştırmaya dayalı puanlamayla doğrulayan; fikirden sonuca beni yönlendiren kişisel AI platformu.

**Kuzey-yıldızı ölçeği:** "tek cevap"dan "yıllarca süren proje"ye aynı sistem; istenen yerde API, CLI, chat arayüzü, yerel model — hepsi bağlanabilir.

**Taşınan ilkeler (kanıtlanmış disiplinler):** kanıt etiketleri `[gözlendi]/[üretildi]/[varsayıldı]` · T-A/B/C karar katmanları · tek-yazıcı · görünürlük ≠ onay · yanlışlanabilir test (eşik veri öncesi sabit) · fren = sayı + takvim · append-only kayıtlar · dört-alanlı dosya kuralı · Topoloji C · markdown+git kaynak-of-truth · dil kuralı (makine İngilizce, kayıt Türkçe, eşleştirme anahtarları iki dilli) · **asla acele yok:** her faz kendi frenini faz başında alır; çok zor olan çıkarılmaz, yolu bulunur.

## 1. Sıfırlama kuralı

- Aktif kök yalnızca yeni sistemin dosyalarını içerir; eski hiçbir kural/state yüklenmez.
- `arsiv/`: eski DECISIONS, REJECTED, PROFILE, REQUIREMENTS, STATE, vision, VISION-ANALYSIS, CLAUDE.md, PROJECT-INSTRUCTIONS, tools/, hooks/, tests/, adapters/, canary log — **girdi değil, referans**.
- git geçmişi aynen korunur (aynı repo).
- Beyanlı istisnalar: PLAN.md kendisi + geçici bootstrap CLAUDE.md (F0'da yazılır, F3'te yenisiyle değişir) + yeni DECISIONS.md (F0'da başlar).
- Yönetilen projelere (KB, ledger, PDF360, DC, DNS) dokunulmaz.
- **Kabul edilmiş risk:** F0–F4 arasında zorlama yok (sahip onaylı). Erken sinyal: kapısız yoğun günlük kullanım başlarsa F4 öne çekilir.
- **Geri dönüş:** `arsivden-geri-don.ps1` (F0'da yazılır) — tek komutla eski düzene dönüş.

## 2. Gizlilik mimarisi (hibrit — sahip kararı 2026-08-23)

| Bölge | İçerik |
|---|---|
| **Public (git)** | PLAN, vision, REQUIREMENTS, CLAUDE.md, PROJECT-INSTRUCTIONS, tools/, hooks/, adapters/, tests/, LICENSE (MIT), DECISIONS (sistem kararları), STATE (kişisel-detay-yazmama disipliniyle) |
| **Yerel (gitignored + bundle senkronu)** | PROFILE, LEDGER (kişisel kayıtlar), sağlayıcı envanteri, kişisel state detayları |

Sonuçları: yerel katmanın git yedeği yok → F5'te bundle-tabanlı yedekleme rutini; sohbet PROFILE'ı raw'dan çekemez → sihirbaz diskten okur, sohbette bundle. "Açık kaynak ↔ gizlilik" gerilimi bu kararla çözülür. Obsidian vault (F7) yereldir, asla repo'ya girmez.

## 3. Yol haritası — 15 faz, ~128 adım

Fren semantiği: **inşaat fazlarında** fren = duraklama dedektörü (2 hafta oturum yok → sahip devam/ara/terk karar verir); **yalnız F8 pilotu** katı yanlışlanabilir frenle kapanır.

### F0 · Sıfırlama (6 adım) — fren: 1 oturum
1. `arsiv/` oluşturma + eski dosyaların taşıması (git mv) + hook'un temiz kaldırılması (`install.py --uninstall`)
2. Yeni `DECISIONS.md` başlar (sıfırdan; arşive işaretçi; ilk giriş = restrukturizasyon kararı)
3. `arsivden-geri-don.ps1` yazılır
4. Geçici `CLAUDE.md` (tek kural: PLAN.md oku, §8'i güncelle)
5. **Bazal ölçüm**: mevcut açılış bağlam hacmi (CLAUDE+STATE+PROFILE+DECISIONS satır/bayt) kayda geçer
6. Commit + push

**Test:** kökte yalnız PLAN.md, CLAUDE.md, DECISIONS.md, arsivden-geri-don.ps1, arsiv/, .gitignore.

### F1 · Vision v2 (5 adım) — fren: 2 oturum
1. Arşiv taraması → ders listesi (16-revizyon dersi, kapı hata dersleri, bayatlık vakaları)
2. Taslak: platform kuzey-yıldızı · kalıcı beyin · senkron = önce beyin, sonra bağlantı · tanıma (çalışma+kişilik+adaptif) · 3-durum hafıza · yürütücü-rolü (kalıcı ana-AI yok, rol takaslanabilir) · kaynak zekası · puanlama · yönlendirilmiş akış · açık kaynak · token disiplini · kalite standardı + güncel başarısızlık modları
3. Sahibe sunum → revizyon
4. **Sahip onayı (T-A kapısı)**
5. `vision.md` köke + kapanış kaydı

**Test:** sahibin açık onayı.

### F2 · REQUIREMENTS v2 (4 adım) — fren: 2 oturum
1. G-türetimi; yeniler: limit envanteri · failover · puanlama-nesnelliği (boyut/ağırlık veri öncesi + kanıt-etiketli girdi + kapanış kuralı) · 3-durum hafıza · token sözleşmesi · yönlendirilmiş akış · açık-kaynak standartları · kademeli otonom
2. Çelişki tablosu: platform↔token · otonom↔sahiplik · açık-kaynak↔gizlilik (hibrit ile çözüldü)
3. **Yeni başarı ölçütü → sahip onayı** (yanlışlanabilir + ölçüm tarihli)
4. `REQUIREMENTS.md` + `LICENSE` (MIT) köke

**Test:** her yeni G yanlışlanabilir formda.

### F3 · Beyin v1 (9 adım) — fren: 3 oturum
1. Dosya mimarisi kararı (T-B): STATE / DECISIONS / LEDGER / PROFILE + dört alan
2. STATE v1 + tavan (~900 kelime)
3. LEDGER şeması: `approved|rejected|deferred` + `revisit:` + PENDING→insan onayı + iki dilli anahtarlar + append-only
4. PROFILE v1: çalışma + kişilik katmanı + soru kuyruğu (arşivdeki açık sorular taşınır) — **yerel bölge**
5. .gitignore tasarımı (hibrit bölünme)
6. Aktif-karar özeti üreticisi (DECISIONS+LEDGER'dan bağlayıcı görünüm)
7. Token sayacı (birincil: açılışta yüklenen dosya hacmi; vekil: transcript)
8. Eşzamanlılık kuralı v1: tek aktif oturum
9. **Test:** açılış bağlamı ≤ bazalın %50'si

### F4 · Zorlama v1 (11 adım) — fren: 3 oturum
1. **opencode fizibilite spike'ı (ilk adım, ≤ yarım gün)** — Stop-eşlenir mekanizma var mı; yoksa zayıf-zorlama sınırı belgelenir
2. Kapı davranış envanteri arşivden (sidechain atlama, `stop_hook_active` koruması, UTF-8/BOM, uzun-oturum uyarısı, `--demo`, toleranslı eşleştirme dersleri)
3–5. Kapı çekirdeği (taşınan test setiyle TDD) + üç-durum davranışı (rejected→bloke / deferred→revisit'e dek uyarı / approved→sessiz)
6. Claude Code adaptörü + install (birleştirmeli, yedekli)
7. opencode adaptörü (spike sonucuna göre)
8. review v2 (kütük sağlığı, revisit, token trendi, tavan, işaretçi)
9. decide v2 + ledger aracı (add/approve/defer/status)
10. **why.py** ("Neden?" — aktif + arşiv taraması)
11. **Test:** taşınan set %100 · R-002 demo bloke · deferred uyarı vakası · çift-kurumsız install

### F5 · Süreklilik + kartlar (8 adım) — fren: 2 oturum
1. Handoff disiplini · 2. uzun-oturum uyarısı · 3. GitHub kanalı + bundle · 4. **yerel-katman yedekleme rutini** · 5. **oturum açılış sihirbazı** · 6. **acil durum kartı** (~10 satır manuel mod) · 7. **kuru koşu** (atılabilir mini-işle tüm hat) · 8. **Test:** sıfır-bağlam devam · sihirbaz ≤N kelime · kuru koşu hatasız

### F6 · Tanıma (8 adım) — fren: 3 oturum
Adaptif soru döngüsü: kuyruk şeması · tekrar-yasak · cevap→PROFILE (kanıt etiketli) · kişilik üslup kuralı · G42 verim ölçütü. **Test:** 2 ardışık oturum tekrarsız; PROFILE tavana uyar. Sahip kontrolü: soru kalitesi.

### F7 · Kişisel bilgi deposu (6 adım) — fren: 2 oturum
1. Vault kategori haritası (mevcut yapıdan) · 2. **v1: araç-bağımsız hedefli dosya erişimi** (sorgu deseni: not adı/klasör/etiket; tam-vault okuma yasak) · 3. v2: MCP semantik arama (yalnız v1 yetmezse) · 4. sorgu disiplini kuralı (önce PROFILE kompakt → vault hedefli → bilemeyeceksen sor) · 5. **Test:** 5 örnek soru vault'tan, sorgu başına ≤ hedef not · 6. sahip kontrolü

### F8 · Pilot (10 adım) — **KATI fren: 4 çalışma oturumu VEYA 6 hafta; dolursa negatif bulguyla kapanır**
1. **Yeni-proje ritüeli** (tek komut: BRIEF + git init + MIT + README/CHANGELOG + STATE iskeleti + işaretçi) · 2. pilot seçimi (ledger aday, onayınla) + P-ölçütleri sabitleme · 3–9. dilimler AIOS sürer (G43 sınavı) · 10. değerlendirme raporu

### F9 · Karar protokolü v3 (12 adım) — fren: 3 oturum
Literatür taraması (ADR/MCDA) · boyut/ağırlık şeması → **onayın** · kapanış kuralı (G21) · kanıt-etiketli puan formatı · decide entegrasyonu · **karar sonuç-izleme** (sonuç alanı + revisit → ağırlık kalibrasyonu) · **kademeli otonom** (alan-bazlı güven seviyesi + kanıt bağlantıları). **Test:** kafadan-puan vakası reddedilir.

### F10 · Beceri kütüphanesi (6 adım) — fren: 2 oturum
skills/ şeması (dört-alanlı, sürümlü) · ilk beceriler (haftalık-review, yeni-proje, derle-doğrula) · **dönemsel özet (opt-in)** · çağırma kuralı. **Test:** tekrarlanan akış skill'den koşar.

### F11 · Envanter + yönlendirici v1 (13 adım) — fren: 4 oturum
Şema: kanal (API/web-chat/abonelik/yerel) + araç; limit, maliyet, yetenek, son-dogrulama · **üretici script** (scoop/uv/ollama taraması) · **senin envanter oturumun** · limit doğrulama araştırmaları · gizlilik: yerel bölge · yönlendirici v1 (görev→kabiliyet, aday sıralama: uygunluk+boş-kota+maliyet, "Gemini Flash medium yeter" tarzı öneri) · araç-yönlendirme tek sorguda · **Test:** 5 örnek görevde tutarlılık · review bayatlık denetimi

### F12 · Failover (12 adım) — fren: 4 oturum
Sinyaller (429 / elle bildirim / tahmin) · geçiş kuralı (**görev sınırında**, bağlam beyinden tohumlanır) · API'de otomatik, web-chat'te öneri · **Test:** sahte 429 → geçiş · devreye alma: **onayın**

### F13 · Bağlantı (15 adım) — fren: 6 oturum
Zarf formatı (özet+kanıt+bağlantı) · tek-yazıcı çoklu-AI'da · dosya-kilit araştırması · CLI çağrılabilirlik envanteri · adaptörler (subagent, Gemini CLI, API, Ollama) · desenler (paralel keşif, çapraz review, iş-bölümü) · **görev başına bütçe tavanı** · **Test:** iki kanal tek state'te, çift-yazım yok

### F14 · Panel + self-improvement (kaba — yaklaşınca ayrışır)
S3/S4 panel seçimi · hata öğrenme kütüğü (kapıya bağlı) · G31 öğrenme döngüsü

## 4. Token sözleşmesi

- Oturum açılışı = STATE (≤900 kelime) + PROFILE (≤400) + aktif-karar özeti. Başka hiçbir dosya varsayılan yüklenmez.
- Birincil metrik: açılışta yüklenen dosya hacmi; vekil: transcript boyutu. Hedef: F3 sonunda bazalın ≥%50 altı.
- Proje oturumları proje STATE + beyin özeti yükler; diğer projeler asla (G16).

## 5. Taşınanlar / arşive gidenler

**Taşınır:** kanıt etiketleri · T-A/B/C · tek-yazıcı · görünürlük≠onay · yanlışlanabilir test · fren · append-only · dört-alan · Topoloji C · markdown+git · dil kuralı · kapı tasarım dersleri (deterministik tetik, insan onayı, toleranslı eşleştirme, PENDING akışı, iki dilli anahtarlar) · PROFILE içeriği · arşivdeki açık sorular.
**Arşive gider:** eski dosya yapısı/adları · eski başarı ölçütü (F2 yenisini yazar) · eski O-testleri · VISION-ANALYSIS · eski araç implementasyonları (davranış envanteriyle dersleri taşınır).

## 6. Riskler

| Risk | Erken sinyal | Önlem |
|---|---|---|
| F0–F4 zorlama boşluğu | kapısız yoğun kullanım | F4 öne çekilir |
| Meta-döngü | PLAN dışı plan dosyası | yasak; §8 yeter |
| Arşiv unutulması | dersler v2'lere girmedi | F1/F2 açık adımı + why.py |
| Token hedefi tutmaz | F3 testi kaldı | eşik değil yöntem gözden geçirilir |
| opencode plugin yetmez | spike başarısız | tek kanal + sınır belgelenir |
| Tempo kayması | 2 hafta sessizlik | duraklama sinyali → sahip kararır |
| Yerel katman kaybı | bundle yok | F5 yedekleme rutini |
| Eşzamanlı yazım | iki oturum aynı dosyada | v1 tek-oturum, F13 kilidi |

## 7. Faz kapanış formatı

`F<n>: bitti/kısmi | test: <sonuç> | fren: <durum> | kanıt: <çıktı/komut> | sahip onayı: var/gerekmez | sonraki: F<n+1>`

## 8. İlerleme

| Tarih | Faz/adım | Durum | Not |
|---|---|---|---|
| 2026-08-23 | PLAN yazıldı | ✅ sahip onaylı | uygulama başladı |
| 2026-08-23 | F0 · adım 1–6 | ✅ bitti | arşiv + geri-dönüş scripti + bazal 892 satır/77.447 bayt + yeni DECISIONS + geçici CLAUDE.md; hook temiz kaldırıldı. Test: kök = PLAN, CLAUDE, DECISIONS, geri-dönüş, arsiv/, .gitignore `[gözlendi]` |
| → | F1 · Vision v2 | sıradaki | arşiv dersi taraması + taslak → sahip onayı |
