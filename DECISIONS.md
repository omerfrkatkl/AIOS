# DECISIONS — karar geçmişi (v3)

| | |
|---|---|
| **Amaç** | Ne olduğunu ve neden olduğunu kaydetmek |
| **Yaşam döngüsü** | **Yalnızca eklenir.** Hiçbir giriş düzenlenmez veya silinmez. Yanlışsa yeni giriş yazılır. |
| **Sahip** | Proje sahibi (tek yazıcı; Claude yazar, sahip diff'i onaylar) |
| **Okuma tetikleyicisi** | Haftalık kontrol + bir kararın nedeni sorgulandığında |

> **Eski log:** `arsiv/DECISIONS.md` (2026-08-15 → 2026-08-23). Gerekçe ararken doğrudan arşiv taranır (F4'te why.py gelecek).

---

## 2026-08-23 · Sıfırdan yeniden inşa: eski sistem arşive, PLAN.md yürürlükte · T-A · onaylandı

- **Karar:** Aktif kök sıfırlandı; eski belgeler ve araçlar `arsiv/` altına **referans** olarak taşındı. Yeni sistem `PLAN.md`'deki 15 fazlık haritaya göre inşa edilir. Gizlilik mimarisi hibrit: PROFILE/LEDGER/envanter yerel (gitignored + bundle), yapısal dosyalar public.
- **Gerekçe:** Sahibin vizyonu netleşti (kalıcı beyin, çoklu-AI senkronu — önce beyin sonra bağlantı, onay/red/erteleme hafızası, tanıma, kaynak zekası, puanlamalı kararlar, platform kuzey-yıldızı) ve organik büyümüş yapı bunu taşımak yerine temiz temelden kurmayı hak etti. Karar geçmişi korunur: arşiv referans, git geçmişi tam.
- **Alternatifler:** Mevcut yapının üzerine ekleme (elendi: eski varsayımlar yeni tasarımı bağlardı) · yalnızca belge yenileme (elendi: sahip "her şey sıfırdan" dedi) · arşivsiz tam silme (elendi: arşiv bedava sigorta, git geçmişi zaten korur)
- **Geri alma:** `arsivden-geri-don.ps1` tek komut. Hook `install.py --uninstall` ile temiz kaldırıldı (8→7 anahtar, yedek alındı); geri dönüşte arşivden yeniden kurulur.
- **Kanıt:** `[gözlendi]` — kök: PLAN.md, CLAUDE.md, DECISIONS.md, arsivden-geri-don.ps1, arsiv/, .gitignore. **Bazal ölçüm:** 892 satır / 77.447 bayt (CLAUDE+STATE+PROFILE+DECISIONS). Sohbet kanalı (raw STATE/PROFILE) F3/F5'e dek duraklatıldı.

## 2026-08-23 · Vision v2 onaylandi; koke yazildi · T-A · onaylandi

- **Karar:** vision.md v2 koke yazildi - 17 bolum: kisisel AI platformu kimligi, kalici beyin (3-durum hafiza + Obsidian), coklu-AI senkronu (once beyin sonra baglanti; yurutucu-rolu; tartisma protokolu), tanima, kaynak zekasi (envanter+yönlendirici+failover+yetenek saglayicilar), arastirmaya dayali puanlama, yonlendirilmis akis, Windows GUI yuzeyi (opencode tasarim referansi), kaynak disiplini, modulerlik, loglama, acik kaynak, kalite standardi, basarisizlik modlari, arsiv dersleri, basari tanimi.
- **Gerekce:** Sahibin bu oturumdaki tum netlesmeleri tek belgede toplandi; taslak sunuldu, sahip onayladi ("daha cok detay gerekmiyor"). Detayin yeri gereksinimlerdir (F2) - vizyonda mekanizma yoktur, kuzey-yildiz bulaniklasmamali.
- **Alternatifler:** Eski vizyonu yerinde yamamak (elendi: yeni istekler eski yapiya sigmiyordu) · daha uzun taslak (elendi: detay F2'nin isi, vizyon siserse north-star kaybolur)
- **Geri alma:** Ucuz - arsiv/vision.md (v1) + git gecmisi; v2 yerinde revize edilebilir.
- **Kanit:** `[gözlendi]` - sahibin acik onayi 2026-08-23.

## 2026-08-23 · REQUIREMENTS v2 turetildi; yeni basari olcutu kilitlendi · T-A · onaylandi

- **Karar:** vision v2'den 44 gereksinim turetildi (G1-G44): hat/akis, kalici beyin (3-durum hafiza + vault), tanima, kaynak zekasi (envanter+yönlendirici+failover+yetenek saglayicilar), karar sistemi (arastirma motoru + puanlama + sonuc-izleme + kademeli otonom + geri-cagirma + tartisma), Windows GUI yuzeyi, token sozlesmesi, modulerlik, log standardi, acik kaynak, sureklilik tatbikati, kurtarma. Ayarici: LICENSE (MIT) + README eklendi.
- **Gerekce:** Her G yanlislanabilir formda yazildi (olculebilir ifadeler: teknik soru=0, acilis <=446 satir, tatbikat <=15 dk). Celiski tablosu dört gerilimi cozmus durumda. Yeni basari olcutu esikleri veri gorulmeden sabitlendi, olcum tarihi 2026-11-30.
- **Alternatifler:** Eski G1-G43'u tasimak (elendi: eski numaralar eski mimariye bagliydi; taze turetim kaynakla hizali) · olcutu vizyonda tutmak (elendi: vizyon kuzey-yildizdir, olcut gereksinimdir)
- **Geri alma:** Ucuz - REQUIREMENTS yerinde revize edilir; olcut esigi veri gelmeden degistirilmez, degistirilirse bu bir girisle kayda gecer.
- **Kanit:** `[gözlendi]` - sahibin acik onayi 2026-08-23.

## 2026-08-24 · Beyin mimarisi: dort katman + sozlesmeler · T-B · kapanista

- **Karar:** Sistem dort katmana ayrildi: (1) BEYIN - sozlesmeli dosyalar (STATE/DECISIONS/LEDGER/PROFILE/vault), (2) ZORLAMA - bagimsiz araclari (gate/review/decide/ledger/why/install), (3) YUZEY - istemciler (Claude Code/opencode/sohbet/gelecek GUI), (4) YUK - yonetilen projeler. Katmanlar arasi tek baglanti sozlesmelerdir (dort-alanli dosyalar, JSONL log standardi, manifest - F12). Beyin egemendir; yuzey olmadan sistem calisir.
- **Gerekce:** Sahibin modulerlik isteğinin mimari karsiligi: bilesen ekleme/cikarma sozlesme+manifest isidir, cekirdek ameliyati degil. Yuzey-istemci kurali "ana arac yok" ilkesini korur.
- **Alternatifler:** Tek MEMORY.md monoliti (elendi: sozlesmesiz siser, turler karisir) · veritabani merkezli depolama (elendi: markdown+git karari ve lock-in direnci) · arayüzle bütünleşik sistem (elendi: arayüz kilidi başarısız modu)
- **Geri alma:** Ucuz simdi - dosyalar zaten ayri; birlestirme sonradan da mumkun ama gereksiz.
- **Kanit:** `[gözlendi]` - F3 TUR1+TUR2: dosyalar uretildi; summary.py dort-vakali sentetik kutuk testini gecti (aktif/deferred/revisit-gemis/PENDING); context_cost.py acilis 83 satir / 4424 bayt (hedef <=446, bazal 892). Sahip Dogrulama Kapisi revize edildi: komutla dogrulanabilir her sey Claude tarafindan dogrulanir.

## 2026-08-24 · F4 zorlama v1: kapi yeniden insa edildi, opencode siniri belgelendi · T-B

- **Karar:** Kapi v3 hooks/gate.py: LEDGER uc-durum (rejected bloke / deferred uyar / approved sessiz / PENDING etkisiz), tasinan 23-vakali test seti, aioslog JSONL standardi, --scan-file tespit modu, uzun-oturum uyarisi, fail-open. Claude Code adaptoru kuruldu (settings.json 8 anahtar, yedekli). opencode adaptoru: SPIKE sonucu - opencode'da yaniti bloke eden Stop-hook karsiligi YOK (yuzey: event/tool.execute.before/permission.ask); v1 = tespit+log (zayif zorlama), plugin session.idle'da son yaniti tarar. R-001..R-006 -> L-001..L-006 goctu (aktif tarihler arsivden).
- **Gerekçe:** Davranis envanteri arsivden tasindi (sidechain atlama, stop_hook_active korumasi, UTF-8/BOM, flush-yarisi retry, toleransli eslestirme) - sifirdan yazarken kazanilan dersler silinmedi. opencode siniri kabul edildi: tespit edilemeyen degil, bloke edilemeyen; tam blok kanali Claude Code'da kaliyor (adaptör deseni 2026-08-15).
- **Alternatifler:** opencode'u tam zorlama ile kurcalamak (elendi: bloke yuzeyi yok, yamaya girisir) · opencode adaptörünü yazmamak (elendi: sahibin gunluk araci orada, G32 orada olmezse sessiz devre disi) · eski gate.py'yi kopyalamak (elendi: sahip 'sifirdan' karari; davranis envanteriyle turetim ayni kaliteyi tasidi)
- **Geri alma:** Ucuz - install.py --uninstall + arsivden-geri-don.ps1
- **Kanıt:** `[gözlendi]` — test 11/11 + 0/12; demo L-002 bloke; deferred 4-vakali sentetik test; kurulumlar idempotent; gate FIRED log'da

## 2026-08-24 · Platform genislemesi: Kanal Sozlesmesi, Gozlemci katmani, F12a/b/c/d · T-B

- **Karar:** Mimari genisletildi: (1) Yasa #7 Kanal Sozlesmesi - her kaynak (lokal/api/router/web-chat) tur/parametre/girdi/limit/yetenek/enforcement/dosya-erisimi bildirir; UI+yönlendirici+zorlama bundan cizer. (2) GÖZLEMCİ katmani - zamanlayici+izleyiciler (kesif/dogrulama/kota); merdiven manuel->Task Scheduler->uygulama. (3) F12 dort alt dilime bolundu: F12a kayit defteri+parametre yuzeyi+sozlu bildirim araci, F12b kesif/dogrulama hatti (OpenRouter poller+RSS), F12c kota takipcisi+yenileme pencere modeli, F12d empirik zeka (kanal sicili+tahminci+arena). (4) F9 puanlama iki-katman: evrensel sabitler (gecis filtresi: modulerlik/loglama/hata yonetimi/acik kaynak) + proje agirliklari (sahibin beyani), olcek 0-1. (5) F10 +sindir.py (web ciktisi dogrulama) + arastirma plani formati + provenance rozeti. (6) F3 +oturum turleri (sohbet -> yalniz yapilandirilmis sinyal). (7) F16 +AI-atifli hata kutugu. (8) F15 kapsam buyudu. (9) PLAN'a izlenebilirlik eki: sahibin 58 istegi satir satir (47 tam / 7 ertelenmis / 4 sinirli-cozumlu / 0 gormezden gelinen).
- **Gerekçe:** Sahibin vizyonu netlesti: uygulama degil, tum AI araclarinin birligi olan bir platform. Analiz sonucu mevcut dort-katmanli mimari bu genislemeyi modul olarak tasiyor - tek yeni mimari ogren GOZLEMCI katmani (arka plan surecleri). Sifirdan baslama gerekmedi; modulerlik yasasi tam bu senaryo icin yazilmisti. Pilot-once sirasi korundu (sahibin onayi): cekirdek kanitlanmadan platform zekasi insa edilmez.
- **Alternatifler:** Sifirdan yeni mimari (elendi: mevcut yasa ve katmanlar genislemeyi tasiyor, yeniden insa kayip) · Platform zekasini pilot oncesine almak (elendi: sahibin onayiyla cekirdek once kanitlanir) · Web-chat otomasyonunu simdi insa etmek (elendi: kirilganlik; manuel-first + sindir.py yeterli v1)
- **Geri alma:** Ucuz - katman/alan eklemeleri; pilot sirasi korunuyor
- **Kanıt:** `[gözlendi]` — Sahibin platform dokumu 2026-08-24 + izlenebilirlik tablosu onayi
