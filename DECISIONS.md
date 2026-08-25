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

## 2026-08-24 · Arsiv kalici referans; geri-donus scripti emekli edildi · T-C

- **Karar:** arsiv/ kalici referans olarak tutuldu (sifir calisma maliyeti; why.py'nin derinligi; gelecek fazlarin ders kaynagi; silmek zaten hicbir sey silmiyor - git gecmisi). arsivden-geri-don.ps1 silindi: F0'da yazildiginda yeni sistem yoktu; simdi kosulsa arsivdeki eski dosyalar yeni beyin dosyalarinin uzerine yazardi - sigorta tehlikeye donustu. Geri donusun gercek mekanizmasi git'tir (her faz commit'li).
- **Gerekçe:** Sahibin olcutu: 'tutmak isimizi zorlastiriyorsa sil'. Arsiv zorlastirmiyor; script zorlastiriyor (kazara tetiklenme riski). Ayrica eski sistem artik ustun yazilmis durumda - geri donus senaryosu kalmadi.
- **Kanıt:** `[gözlendi]` — Yeni zorlama calisiyor (test 11/11, gate FIRED log'da); git gecmisi tam

## 2026-08-24 · REQUIREMENTS'a G45-G53 eklendi (platform genislemesi hizalandi) · T-C

- **Karar:** Revizyon 3 ile onaylanan platform ozellikleri gereksinim kutugune formalize edildi: G45 otomatik model kesfi, G46 canli kota+yenileme penceresi, G47 Kanal Sozlesmesi, G48 web ciktisi sindirme, G49 oturum turleri, G50 ogrenme denetimi (unlearning), G51 provenance, G52 empirik zeka (sicil/tahminci/arena), G53 bagimlilik grafigi.
- **Gerekçe:** PLAN ve vision revizyon 3 ile genisledi; gereksinim kutugu geride kaldi - uc belge hizali olmali (G-kaynak izlenebilirligi). Icerik sahibin onayladigi ozelliklerin formalizasyonu; yeni karer icermez.
- **Kanıt:** `[gözlendi]` — Sahibin izlenebilirlik tablosu onayi 2026-08-24

## 2026-08-24 · Kapi kapsami: yalniz AIOS dizini (paralel oturum korumasi) · T-B

- **Karar:** Kullanici seviyesindeki hook/plugin her oturumda atesliyor; kapsam filtresi eklendi - zorlama yalnizca AIOS dizinindeki oturumlarda uygulanir. Dis oturumlar SESSIZ atlanir (log girdisi yok, gecikme yok). Yonetilen projeler F8 ritüelinin yazacagi isaretciyle opt-in olacak. opencode plugin ayni directory kontroluyle korunur.
- **Gerekçe:** Sahibin paralel is oturumlari var (baska dizinlerde opencode + Claude Code). AIOS redlerinin baska isin akisini bloklamasi = karisim; ayrica diger oturumlarin yanit metadata'sinin AIOS log'una yazilmasi gizlilik ihlali. Topoloji C ilkesi: konvansiyonlar yonetilen projelere uygulanir, dis alanlara degil.
- **Alternatifler:** Tum makinede zorlama (elendi: sahibin diger isini AIOS redleriyle bloklar - karisim) · Her projeye manuel config (elendi: surtunme; F8 ritueli opt-in isaretciyle otomatik halleder) · Kapsami Documents/Projects yapmak (elendi: DC gibi oncesi projeler de icine girer)
- **Geri alma:** Ucuz - tek kosul satiri
- **Kanıt:** `[gözlendi]` — Dis cwd sessiz (log girdisi yok), AIOS cwd FIRED - komutla dogrulandi

## 2026-08-24 · opencode plugin cikarim hatasi kok nedeni: SDK parametre sekli · T-C

- **Karar:** client.session.messages dogru cagri: { path: { id: sessionID } } (types.gen.d.ts'ten dogrulandi; { sessionID } gonderimi sessiz 422 uretiyordu). Cikarim cok-sekalli (S1 dizi / S2 info+parts / S3 fallback) + tanisal log (diag alani) + aiosLog ctx destegi. aioslog zaman damgalari UTC'ye birlestirildi (JS ile ayni).
- **Gerekçe:** Test B'de tetikleyici calisti ama cikarim bos dondu; tahmin yerine SDK tip tanimlarindan kok neden okundu.
- **Kanıt:** `[gözlendi]` — Sentetik 4-vaka testi + tur sonu dogrulamasi sahibin restart testiyle

## 2026-08-24 · F4 canli testler gecti; kapsam filtresinin gunesi F8'de · T-B

- **Karar:** F4 canli dogrulama tamam: (A) Claude Code restart sonrasi FIRED clean x2 (19:57) - tam-blok kanali canli. (B) opencode restart sonrasi extract ok (S1) + BLOCKED L-002,L-003 (surface=opencode) - tespit kanali canli. Kapsam filtresi karan: su an yalniz AIOS dizini (insa donemi); F8 ritüeli yonetilen proje isaretcisini yazdiginda kapsam o projeye genisler; butun yonetilen projeler kapsama alininca yalniz-AIOS kisiti kalkar (sahibin beyani: 'sonra iptal edelim, mantiken olmasi gereken'). spawn timeout 15s->30s (bir ETIMEDOUT gozlendi).
- **Gerekçe:** Her iki kanalin canli kaniti log'da (aios.jsonl): Claude Code tam blok, opencode tespit+log. Kapsam kisiti insa donemi icin gecici korumadir; kalici hedef Topoloji C uyumu - yonetilen projelerde AIOS zorlamasi isaretciyle acilir.
- **Alternatifler:** Kisiti kalici birakmak (elendi: yonetilen projelerde zorlama olmaz - G32'nin platform versiyonu bos kalir) · Hemen tum makineye acmak (elendi: sahibin paralel is oturumlari etkilenir; kapsam projeye-girmeyle genisler)
- **Geri alma:** Ucuz - kapsam kosulu tek satir
- **Kanıt:** `[gözlendi]` — aios.jsonl 18:10-18:14 kayitlari + sahibin iki restart testi

## 2026-08-24 · F5 kuru kosu: tum hat dogrulandi · T-C

- **Karar:** Kuru kosu zinciri kosuldu: milestone tag (ms/f5-sonrasi) -> decide girdisi -> summary sihirbaz satiri -> context_cost olcumu -> gate demo (zorlama) -> bundle (handoff) -> backup (yerel katman) -> review (saglik). Butun halkalar cikti uretti.
- **Gerekçe:** F5 testinin yarisi (kuru kosu) sahibin mudahalesi olmadan kanitlanabilir; diger yarisi (sifir-baglam tatbikat) sahibin canli testidir.
- **Kanıt:** `[gözlendi]` — Bu giriin kendisi zincirin 1. halkasi

## 2026-08-24 · F5 kapatildi: sureklilik tatbikati 11 saniyede gecti · T-B

- **Karar:** Sifir-baglam tatbikat sahibin kendisi tarafindan yapildi: YENI bir Claude Code oturumu (farkli arac), tek istem ('STATE.md ve PLAN.md §8'i oku; nerede olduğumuzu ve sıradaki işi söyle') -> 11 SANIYEDE dogru yanit: F0-F5 durumu, F5 icerigi (bundle/backup/milestone/sihirbaz/EMERGENCY/kuru kosu), siradaki is (F6), acik risk notu (ETIMEDOUT) - hepsi dogru. Esik <=15 dakika idi; gerceklesen 11 saniye. Not: olcut-2'nin tam kosulu (>=3 hafta ara) 2026-11-30 olcumunde degerlendirilecek; bu tatbikat mekanizmayi kanitladi.
- **Gerekçe:** F5'in testi 'farkli arac + sifir baglam + hizli devam' idi; dosya mimarisi baglami tasidi - arsiv donemindeki 'sureklilik testiyle kanitlandi' iddiasinin v3 versiyonu, simdi daha zengin beyinle. Yanitin dogrulugu sahibin yapistirdigi icerikten dogrulandi (yalnizca dosyalari okuyan uretebilir).
- **Alternatifler:** Tatbikati 3 hafta sonraya birakmak (elendi: mekanizma kaniti ile olcut olcumunu ayirmak dogru; ikisi farkli seyler) · Ayni aracta test etmek (elendi: farkli-arac kosulu kanit degerini artirir)
- **Geri alma:** Ucuz - tatbikat tekrarlanabilir; F5 araclari geri alınabilir
- **Kanıt:** `[gözlendi]` — Sahibin raporu + yapistirilan yanit icerigi (2026-08-24)

## 2026-08-24 · F6b Derin Interview Kampanyasi eklendi; mekanizma!=deger dersi · T-B

- **Karar:** F6b eklendi (F6 sonrasi, F7 oncesi): kapsam haritasi PROFILE'da (12 alan + platform alanlari, alan basina yuzde), interview modu ('beni tani' tetikleyici, 3-5'lik baglantili gruplar, platform-oncelikli siralama: tasarim zevki -> arac/model tercihleri -> proje turleri -> ...), vault-first (Documents/All hedefli okuma, bilinen sorulmaz). Kural revizesi: <=1/oturum yalniz normal oturumlarda; interview modunda gruplar serbest (G42 verim + tekrar-yasak gecerli). Sistemik ders: mekanizma fazlarina icerik kampanyasi adimlari (F8 pilot, F12a envanter oturumu, F12b diff kosulari). Vault yolu bulundu: Documents/All (obsidian.json'dan).
- **Gerekçe:** Sahibin itirazi hakliydi: '3 soruyla neremi anladin - onlarca/yuzlerce soru gerekmez mi'. F6 mekanizmayi kurdu ama kampanyayi planlamamisti; vision §3 12 alan sayiyor ve sahibin acik sozuyle 'cok sayida soruya acik'. Ayrica sahibin paralel oturum bilgisi: vault Documents/All'da - interview v1 dosya erisimiyle okuyabilir.
- **Alternatifler:** Serpistirilmis soru modu (elendi: sahibin secimi grup grup uzun oturum) · Vault'suz interview (elendi: sahibin secimi vault-first; cift sorma riski) · F7'den sonra baslamak (elendi: sahibin secimi simdi; v1 dosya erisimi yeterli)
- **Geri alma:** Ucuz - kampanya PROFILE kapsam haritasiyla sinirli; kural tek satir
- **Kanıt:** `[gözlendi]` — Sahibin itirazi + 4 soru-cevap + vault yapisi gozlendi (11 klasor + vision.md)

## 2026-08-25 · Gözden geçirildi · T-C

- **Kapsam:** 14 karar gözden geçirildi.
- **Onay bekleyen:** 0 (yok)
- **Kanıt:** `[gözlendi]` — `tools/review.py --done`

## 2026-08-25 · F8 pilot basladi: yuk=ledger, P1-P4 esikleri kilitlendi · T-B

- **Karar:** Pilot yuk: ledger (kisisel gelir-gider CLI, Projects/ledger/BRIEF.md hazif). Yeni-proje ritueli insa edildi (tools/newproject.py: BRIEF+git+MIT+README/CHANGELOG+STATE+.aios kapi opt-in) ve ledger'e --augment ile uygulandi (BRIEF korunudu, 5 bilesen eklendi). Kapsam filtresi .aios marker yuruyusuyle genisletildi: ledger oturumlari artik zorlanir, DC/Documents-All sessiz kalir (komutla dogrulandi). P-olcutler veri gorulmeden kilitlendi: P1 calisan CLI <=4 oturum VEYA 6 hafta (KATI fren, dolursa negatif bulguyla kapanir); P2 teknik secimler AIOS tarafindan, sahibe teknik soru=0, her secim >=2 alternatif+gerekce; P3 DECISIONS 2-8 bandi, T-A <=1; P4 sahibin algi 'dogrudan sohbetten yavas degil'.
- **Gerekçe:** Sahibin onayi ('plan dahilinde gidiyorsak onayliyorum') + pilot oncesi esik sabitleme kurali 8. G43'un ilk gercek sinavi: depolama bicimi ve CLI catisi kararlari arastirmayla AIOS tarafindan kapatilir. .aios opt-in mekanizmasi kapsam filtresinin insa-donemi kisitini duzenli cikis noktasina bagladi (sahibin 'sonra iptal edelim' kararinin uygulama yolu).
- **Alternatifler:** Pilot yuk olarak baska proje (elendi: sahibin onayi ledger uzerinde) · P-olcutleri pilot sirasinda ayarlamak (elendi: kural 8 - esik veri gorulmeden sabitlenir)
- **Geri alma:** Ucuz simdi - ilk hafta icinde yuk degisir; fren dolursa negatif bulguyla kapanir
- **Kanıt:** `[gözlendi]` — Rituel ciktisi + kapsam testi (ledger FIRED, DC sessiz) komutla dogrulandi
