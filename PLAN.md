# PLAN — AIOS sıfırdan yeniden inşa

| | |
|---|---|
| **Amaç** | Restukturizasyonun tek yetkili haritası: kalıcı beyin + çoklu-AI senkronu + tanıma + kaynak zekası + puanlamalı karar sistemi + Windows uygulama yüzeyi |
| **Yaşam döngüsü** | Fazlar ilerledikçe yerinde güncellenir; §8 İlerleme tablosu her oturum sonunda tazelenir |
| **Sahip** | Proje sahibi (yön onayları) · Claude (yürütme) |
| **Okuma tetikleyicisi** | Her oturum açılışı + her faz başı + haftalık kontrol |

> Bu dosya onaylı planın kendisidir; dışında plan dosyası açılmaz (meta-döngü koruması).

## 0. Hedef, ilkeler ve mimari yasalar

**Tek cümle:** Hangi AI'yi, hangi arayüzden, hangi modelle kullanırsam kullanayım aynı davranan; unutmayan; beni tanıyan; token-verimli; kararlarını araştırmaya dayalı puanlamayla doğrulayan; fikirden sonuca beni yönlendiren kişisel AI platformu.

**Kuzey-yıldızı ölçeği:** "tek cevap"dan "yıllarca süren proje"ye aynı sistem; API, CLI, chat arayüzü, yerel model — hepsi bağlanabilir.

**Taşınan ilkeler:** kanıt etiketleri `[gözlendi]/[üretildi]/[varsayıldı]` · T-A/B/C karar katmanları · tek-yazıcı · görünürlük ≠ onay · yanlışlanabilir test (eşik veri öncesi sabit) · fren = sayı + takvim · append-only kayıtlar · dört-alanlı dosya kuralı · Topoloji C · markdown+git kaynak-of-truth · dil kuralı (makine İngilizce, kayıt Türkçe, eşleştirme anahtarları iki dilli) · **asla acele yok.**

**Mimari yasalar (modülerlik — F1'den F15'e her yere işlenir):**
1. **Sözleşme-first:** her bileşenin girdi/çıktı sözleşmesi yazılıdır (dosyalar için dört alan).
2. **Kayıt-defteri-güdümlü:** araçlar/yetenekler kendini manifest'e kaydeder; yüzeyler koddan değil kayıt defterinden okur — yeni araç otomatik görünür, çıkarmak bir satırdır.
3. **Gevşek bağlı:** çekirdek hiçbir araca, arayüze veya sağlayıcıya sıkı bağlı olamaz.
4. **Yüzeyler istemcidir, beyin egemendir:** uygulama olmasa da sistem çalışır.
5. **Append-only veri, idempotent araçlar:** aynı komut iki kez koşarsa zarar vermez.
6. **Tek sorumluluk:** her dosya/script tek iş yapar.

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

## 3. Yol haritası — 17 faz, ~140 adım

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
1. Dosya mimarisi kararı (T-B) + **mimari karar kaydı** (katmanlar + sözleşmeler) · 2. STATE v1 + tavan · 3. LEDGER şeması (`approved|rejected|deferred` + `revisit:` + PENDING→insan onayı + iki dilli anahtarlar) · 4. PROFILE v1 (çalışma + kişilik + soru kuyruğu; arşivdeki açık sorular taşınır) — **yerel** · 5. .gitignore tasarımı (hibrit) · 6. Aktif-karar özeti üreticisi · 7. Token sayacı (birincil: açılışta yüklenen dosya hacmi) · 8. Eşzamanlılık kuralı v1 (tek aktif oturum) · 9. **Kalıcı CLAUDE.md** (geçicinin yerine) · 10. **Sohbet talimat dosyası v2** · 11. **Test:** açılış bağlamı ≤ bazalın %50'si

### F4 · Zorlama v1 (12 adım) — fren: 3 oturum
1. **Log/hata standardı** (JSONL şeması + "ne oldu/neden/ne yapmalısın" kullanıcı formatı; logs/ yerel, bağlamaya asla yüklenmez) · 2. **opencode fizibilite spike'ı** (≤ yarım gün; yoksa zayıf-zorlama sınırı belgelenir) · 3. Kapı davranış envanteri arşivden (sidechain atlama, `stop_hook_active` koruması, UTF-8/BOM, uzun-oturum uyarısı, `--demo`, toleranslı eşleştirme) · 4–6. Kapı çekirdeği (taşınan test setiyle TDD) + üç-durum davranışı · 7. Claude Code adaptörü + install · 8. opencode adaptörü · 9. review v2 (kütük sağlığı, revisit, token trendi, tavan, işaretçi, **log sağlığı**) · 10. decide v2 + ledger aracı · 11. **why.py** (aktif + arşiv) · 12. **Test:** taşınan set %100 · R-002 bloke · deferred uyarı · çift-kurumsız install

### F5 · Süreklilik + kartlar (8 adım) — fren: 2 oturum
1. Handoff disiplini · 2. uzun-oturum uyarısı · 3. GitHub kanalı + bundle · 4. **yerel-katman yedekleme rutini** · 5. **oturum açılış sihirbazı** · 6. **acil durum kartı** · 7. **kuru koşu** (mini-işle tüm hat) · 8. **Test:** sıfır-bağlam devam + **süreklilik tatbikatı prototipi** (farklı araç, sıfır bağlam, ≤15 dk devam)

### F6 · Tanıma (8 adım) — fren: 3 oturum
Adaptif soru döngüsü: kuyruk şeması · tekrar-yasak · cevap→PROFILE (kanıt etiketli) · kişilik üslup kuralı · G42 verim ölçütü. **Test:** 2 ardışık oturum tekrarsız. Sahip kontrolü: soru kalitesi.

### F7 · Kişisel bilgi deposu (6 adım) — fren: 2 oturum
1. Vault kategori haritası (mevcut yapıdan) · 2. **v1: araç-bağımsız hedefli dosya erişimi** (tam-vault okuma yasak) · 3. v2: MCP semantik arama (yalnız v1 yetmezse) · 4. sorgu disiplini kuralı · 5. **Test:** 5 örnek soru vault'tan, sorgu başına ≤ hedef not · 6. sahip kontrolü

### F8 · Pilot (10 adım) — **KATI fren: 4 çalışma oturumu VEYA 6 hafta; dolursa negatif bulguyla kapanır**
1. **Yeni-proje ritüeli** (tek komut: BRIEF + git init + MIT + README/CHANGELOG + STATE iskeleti + işaretçi) · 2. pilot seçimi (ledger aday, onayınla) + P-ölçütleri · 3–9. dilimler AIOS sürer (G43 sınavı) · 10. değerlendirme raporu

### F9 · Karar protokolü v3 (14 adım) — fren: 3 oturum
Literatür taraması (ADR/MCDA) · boyut/ağırlık şeması → **onayın** · kapanış kuralı (G21) · kanıt-etiketli puan formatı (kafadan puan geçersiz) · decide entegrasyonu · **karar sonuç-izleme** (sonuç alanı + revisit → kalibrasyon) · **kademeli otonom** (alan-bazlı güven seviyesi) · **tartışma protokolü** (≤3 tur, farklı sağlayıcı tercih, çıktı = karar hattına giren öneri) · **karar geri-çağırma** (etki analizi + geri alma planı). **Test:** kafadan-puan vakası reddedilir.

### F10 · Araştırma motoru v1 (8 adım) — fren: 3 oturum
Yöntem seçimi (G17) · araştırma hattı (soru→yöntem→kaynak→sentez→**kanıt-etiketli rapor**) · **araştırma önbelleği** (aynı soru → önce geçmiş rapor + tazelik kontrolü) · **puan girdileri raporlara atıfta zorunlu** (kafadan değerlendirme yasağının teknik uygulaması) · kaynak kütüğü. **Test:** örnek soruda rapor üretilir; önbellek isabeti çalışır.

### F11 · Beceri kütüphanesi (6 adım) — fren: 2 oturum
skills/ şeması (dört-alanlı, sürümlü) · ilk beceriler (haftalık-review, yeni-proje, derle-doğrula) · **dönemsel özet (opt-in)** · çağırma kuralı. **Test:** tekrarlanan akış skill'den koşar.

### F12 · Envanter + yönlendirici v1 (15 adım) — fren: 4 oturum
1. Şema: kanal (API/web-chat/abonelik/yerel) + araç; limit, maliyet, yetenek, son-dogrulama · 2. **öncül araştırma: OpenWebUI/LM Studio yetenek seti** (referans) · 3. **üretici script** (scoop/uv/ollama taraması) · 4. **senin envanter oturumun** · 5. limit doğrulama araştırmaları · 6. gizlilik: yerel bölge · 7–11. yönlendirici v1 (görev→kabiliyet; aday sıralama: uygunluk+boş-kota+maliyet; "Flash medium yeter" tarzı öneri) · 12–13. **yetenek sağlayıcılar:** yeteneği olmayan kanala araç takma (web-arama takviyesi vb.; MCP/CLI sarmalayıcı) · 14. araç-yönlendirme tek sorguda · 15. **Test:** 5 örnek görevde tutarlılık + review bayatlık denetimi

### F13 · Failover (12 adım) — fren: 4 oturum
Sinyaller (429 / elle bildirim / tahmin) · geçiş kuralı (**görev sınırında**, bağlam beyinden tohumlanır) · API'de otomatik, web-chat'te öneri · **Test:** sahte 429 → geçiş · devreye alma: **onayın**

### F14 · Bağlantı (15 adım) — fren: 6 oturum
Zarf formatı (özet+kanıt+bağlantı) · tek-yazıcı çoklu-AI'da · **yürütücü = entegratör** (alt-AI yapılandırılmış çıktı üretir, beyne yalnız yürütücü yazar) · dosya-kilit araştırması · CLI çağrılabilirlik envanteri · adaptörler (subagent, Gemini CLI, API, Ollama) · delegasyon desenleri (**araştırma devri**, paralel keşif, çapraz review, iş-bölümü) · **görev başına bütçe tavanı** · **Test:** iki kanal tek state'te, çift-yazım yok

### F15 · Windows GUI uygulaması (kaba — yaklaştıkça ayrışır; fren o zaman sabitlenir)
**Gerçek pencere uygulaması** (terminal değil) · **tasarım referansı: opencode** (tasarım olduğu gibi/uyarlanarak alınır — tasarım emeği sıfıra yakın, sistem %100 bizim) · teknoloji seçimi araştırmayla (S3/S4; ölçütlerden biri: opencode tasarım-taşınabilirliği) · uygulama = istemci, araçları **kayıt defterinden** okur · iç görünümler: model seçici, tartışma arayüzü, araştırma görünümü, durum panosu, log görüntüleyici · GUI önce TUI yok — doğrudan Windows uygulaması

### F16 · Self-improvement + hata öğrenme kütüğü (kaba — yaklaşınca ayrışır)
Log analizinden tekrarlanan-hata öğrenmesi (kapıya bağlı) · G31 döngüsü · periyodik süreklilik tatbikatı

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

## 7. Faz kapanış formatı

`F<n>: bitti/kısmi | test: <sonuç> | fren: <durum> | kanıt: <çıktı/komut> | sahip onayı: var/gerekmez | sonraki: F<n+1>`

## 8. İlerleme

| Tarih | Faz/adım | Durum | Not |
|---|---|---|---|
| 2026-08-23 | PLAN yazıldı | ✅ | F0 ile birlikte |
| 2026-08-23 | F0 · adım 1–6 | ✅ bitti | arşiv + sigorta + bazal 892 satır/77.447 bayt; hook temiz kaldırıldı; commit 76e1b9d |
| 2026-08-23 | PLAN revizyon 2 | ✅ | 17 faz: +F10 Araştırma motoru, F15 Windows GUI (opencode tasarım ref.), modülerlik yasası, log standardı, yetenek sağlayıcılar, tartışma, geri-çağırma, tatbikat |
| 2026-08-23 | F1 · Vision v2 | ✅ bitti | ders listesi (10 kalem) + taslak sunuldu → **sahip onayı** → vision.md kökte (17 bölüm) · DECISIONS'a T-A kapanış girişi |
| 2026-08-23 | F2 · REQUIREMENTS v2 | ✅ bitti | 44 G (yanlışlanabilir) + T/H/S + çelişki tablosu + **başarı ölçütü (ölçüm 2026-11-30)** → **sahip onayı** · LICENSE (MIT) + README eklendi |
| → | F3 · Beyin v1 | sıradaki | 11 adım: dosya mimarisi + LEDGER + PROFILE + gitignore + özet üretici + sayaç + kalıcı CLAUDE.md + sohbet talimatı · test: açılış ≤446 satır |
