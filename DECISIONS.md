# DECISIONS — karar geçmişi

| | |
|---|---|
| **Amaç** | Ne olduğunu ve neden olduğunu kaydetmek |
| **Yaşam döngüsü** | **Yalnızca eklenir.** Hiçbir giriş düzenlenmez veya silinmez. Yanlışsa yeni giriş yazılır. |
| **Sahip** | Proje sahibi (tek yazıcı) |
| **Okuma tetikleyicisi** | Haftalık gözden geçirme + bir kararın nedeni sorgulandığında |

**Format:** `tarih · başlık · katman · durum` → Karar / Gerekçe / Alternatifler / Geri alma / Kanıt

---

## 2026-08-15 · Çalışma protokolü v2.1 kabul edildi · T-A · onaylandı

- **Karar:** Yürütmenin araştırmayı çektiği, STATE/LOG ayrımlı, üç katmanlı karar protokolü.
- **Gerekçe:** Önceki projenin başarısızlık biçimi araştırma eksikliği değil, yürütme ve doğrulama eksikliğiydi.
- **Alternatifler:** Faz temelli RKZ v1/v2 (elendi: yürütmeyi geciktiriyor, belge üretiyor) · protokolsüz doğrudan çalışma (elendi: karar görünürlüğü yok).
- **Geri alma:** Ucuz — protokol iki dosya ve bir dizi kuraldan ibaret.
- **Kanıt:** `[üretildi]` + sahibin dört turluk incelemesi.

## 2026-08-15 · Başarı ölçütü tanımlandı · T-A · onaylandı

- **Karar:** Sonuç-çıpalı dört yan cümle + üç başarısızlık cümlesi, ölçüm 2026-11-15.
- **Gerekçe:** Özellik temelli ölçüt ("sistemde şu var") kullanılmayan özellik inşasını ödüllendirir ve yanlışlanamaz.
- **Alternatifler:** Sistem-özelliği ölçütleri (elendi) · ölçüt yazmadan başlamak (elendi: yanlışlanamazlık).
- **Geri alma:** Orta — kriter değişirse üç aylık gözlem penceresi yeniden başlar.
- **Kanıt:** `[varsayıldı]` — kriterlerin doğru kriterler olduğu henüz kanıtlanmadı, kullanımla sınanacak.

## 2026-08-15 · Pilot yük seçildi · T-B · onaylandı

- **Karar:** Eski knowledge-base projesinin minik dilimi (tek kaynak sayfası → üç öğe → tek sayfalık derlenmiş PDF).
- **Gerekçe:** Sahibin ilk tercihi olan "OS'in kendisi" reddedildi: (1) başarı ölçütünün ilk yan cümlesi anlamsızlaşıyor, (2) OS'in zayıflığı ile projenin zayıflığı aynı olduğu için arıza kendi teşhisini bozuyor, (3) dış zorlayıcı yok — sonsuza kadar "iyileştirilebilir" kalır.
- **Alternatifler:** OS'in kendisi (elendi, yukarıdaki üç gerekçe) · yeni küçük proje (canlı tutuldu; sahip isterse değiştirilebilir).
- **Geri alma:** Ucuz — ilk hafta içinde değiştirilebilir.
- **Kanıt:** `[gözlendi]` — önceki projenin 16 revizyonluk kaydı, dış zorlayıcı yokluğunun sonucunu doğrudan gösteriyor.

## 2026-08-15 · Eski proje belgeleri girdi değil, referans · T-B · onaylandı

- **Karar:** Eski plan, A/B kütükleri ve revizyon geçmişi pilota başlangıç girdisi olarak alınmaz.
- **Gerekçe:** Yük seçmenin amacı gerçek iş taşımak; birikmiş spesifikasyonu geri ithal etmek değil.
- **Geri alma:** Ucuz — gerektiğinde referans olarak açılabilir.
- **Kanıt:** `[gözlendi]` — sahibin açık talimatı.

## 2026-08-15 · Dikkat bütçesi ve WIP limiti · T-C

- **Karar:** Günlük 60+ dk bütçe kaydedildi; T-A WIP limiti buna rağmen 3'te tutuldu.
- **Gerekçe:** Yüksek bütçenin riski düşük bütçeninkinin tersidir — inceleyebilmek, sisteme inceletecek iş ürettirir. Bütçe iş hacmini değil, gerektiğinde derine inme payını finanse etmeli.
- **Kanıt:** `[varsayıldı]` — 2-3 haftada kalibre edilecek.

## 2026-08-15 · A2 prior-art taraması yapıldı · T-A · onaya açık

- **Karar:** Hazır bir çözüm benimsenmiyor, ama kapsam ikiye bölünüyor: hat (spec→plan→inşa) ve hafıza/devir **hazırdan alınır**; karar katmanlama, görünürlük/veto, kanıt kökeni, dikkat bütçesi ve plan-gerçeklik mutabakatı **inşa edilir**.
- **Gerekçe:** A1'in dört yan cümlesinden 1 ve 2 mevcut araçlarca büyük ölçüde karşılanıyor; 3 ve 4 hiçbiri tarafından karşılanmıyor. Kill kriteri (≥%70) sağlanmadı, ama "sıfırdan inşa" da gerekçesiz.
- **Alternatifler:** BMAD-METHOD (elendi: 12+ ajan, token maliyeti ve öğrenme eğrisi A1'in 4. yan cümlesini doğrudan tehdit ediyor, ayrıca tek-yazıcı ilkesiyle çelişiyor) · GitHub Spec Kit (kısmen alınabilir: "constitution" fikri) · Kiro (elendi: AWS'e bağlı, kredi ölçümlü) · hiçbir şey benimsememek (elendi: hafıza ve hat zaten çözülmüş).
- **Geri alma:** Ucuz — benimseme kararları dosya düzeyinde.
- **Kanıt:** `[gözlendi]` — kaynaklar 2026 tarihli uygulayıcı karşılaştırmaları; SDD araçlarının enforcement/verification sütunlarının neredeyse tamamen boş olduğu ve statik spec'lerin uygulamadan hızla saptığı bağımsız olarak raporlanmış.

## 2026-08-15 · Tarama bütçesi aşılmadı · T-C

- **Karar:** A2, 3 aramada kapatıldı; 60 dk `[bütçe]` tavanı korundu.
- **Kanıt:** `[gözlendi]`.

## 2026-08-15 · Dilim-1 tanımlandı (A3) · T-B

- **Karar:** Tek kaynak sayfası → üç öğe → tek sayfalık derlenmiş PDF; kasten iki oturuma bölünür.
- **Gerekçe:** Dilim OS'in dilimidir, yükün değil — yük yalnızca harness'ı sürer. Bölme kasıtlı: A1'in süreklilik ölçütü tek oturumda sınanamaz, bölmek sıfıra mal olur ve en riskli iddiayı en erken test eder.
- **Alternatifler:** Tek oturumluk dilim (elendi: süreklilik hakkında sinyal vermiyor) · daha büyük dilim, çoklu sayfa (elendi: 1 haftada bitmez, T-A/1'i test edemez).
- **Geri alma:** Ucuz.
- **Kanıt:** `[varsayıldı]` — bir haftada bitip bitmeyeceği ölçülecek.

## 2026-08-15 · A4: iki T-A açıldı, üçüncü yuva boş bırakıldı · T-B

- **Karar:** T-A/1 iş biriminin tanımı, T-A/2 OS–yük sınırı. Diğer adaylar T-B/T-C'ye indirildi.
- **Gerekçe:** WIP kotası doldurulmadı; yapay T-A üretmek protokolün en olası bozulma biçimi. T-A/2 için ucuz bir dedektör (dosya başına `OS`/`YÜK` etiketi) kuruldu — geç-fark-edileni erkene çekiyor, dolayısıyla dedektör çalışırsa karar T-B'ye iner.
- **Alternatifler:** Durum formatını, çalışma yüzeyini ve araç zincirini de T-A yapmak (elendi: hepsi tersinir ve sürtünme hemen hissediliyor).
- **Kanıt:** `[gözlendi]` — protokolün üç koşullu pre-execution istisnası her iki T-A'ya uygulandı, ikisi de "kullanınca fark edilir" olduğu için tetiklenmedi.

## 2026-08-15 · Mutabakat kontrolü sonucu · T-C

- **Karar:** Üç girdiden ikisi hazır (kaynak sayfa sağlanabilir, Claude Code kurulu), biri eksik (typst). Eksik girdi, dilim-1'in ilk işi olarak alındı — ayrı bir faz açılmadı.
- **Kanıt:** `[gözlendi]` — sahibin beyanı.

## 2026-08-15 · Çalışma tek tarafta: Windows · T-B

- **Karar:** Dilim-1 tamamen Windows tarafında çalışır. WSL karıştırılmaz. typst Scoop ile kurulur.
- **Gerekçe:** Sahibin merkezî ve temiz kurulum tercihi Scoop'u işaret ediyor; WSL'i işin içine katmak yol çevirisi ve iki ayrı paket yöneticisi demek — dilim-1 için gerekçesiz karmaşıklık. En dar kapsam.
- **Alternatifler:** WSL içinde typst (elendi: merkezî yönetim tercihine aykırı, ikinci paket yöneticisi) · Windows typst'i WSL'den `typst.exe` olarak çağırmak (elendi: yol çevirisi sürtünmesi, dilim-1'de gereksiz).
- **Geri alma:** Ucuz — tek binary, tek klasör.
- **Kanıt:** `[varsayıldı]` — Claude Code'un Windows'ta mı WSL'de mi kurulu olduğu ilk komutla doğrulanacak; WSL çıkarsa karar yeniden değerlendirilir.

## 2026-08-15 · Klasör yapısı = OS/YÜK etiketi · T-B

- **Karar:** Kök = OS, `yuk/` = YÜK. Ayrı bir etiketleme mekanizması kurulmaz; dizin konumu etikettir.
- **Gerekçe:** T-A/2'nin dedektörünü sıfır maliyetle kuruyor — yerleştirilemeyen dosya, sınırın yanlış olduğunun sinyali. Ayrı metadata alanı tutmak hem fazladan iş hem unutulmaya açık.
- **Alternatifler:** Dosya başına metadata etiketi (elendi: unutulur, doğrulanamaz).
- **Geri alma:** Ucuz.
- **Kanıt:** `[varsayıldı]` — dedektörün gerçekten ateşlenip ateşlenmediği 1. hafta sonunda ölçülecek.

## 2026-08-15 · CLAUDE.md yazıldı · T-C

- **Karar:** Harness'ın tek yeni bileşeni; kurallar, dosya politikası, OS/YÜK dedektörü ve dilim-1 kapsam dışı listesi.
- **Kanıt:** `[üretildi]` — etkisi 1. haftada ölçülecek.

## 2026-08-15 · Dosya ve dizin adlandırması · T-B

- **Karar:** `LOG.md` → `DECISIONS.md`; `yuk/` → `projects/kb-slice/{source,output}`. Kök dosyalar kalıcı kabul edildi. `STATE.md` yeniden adlandırılmadı.
- **Gerekçe:** Adlandırma mimari taahhüt taşır. `payload/` iç içe topolojiyi onaylardı; `projects/` ise bir dizin seviyesi karşılığında ikinci projeyi bedavaya getiriyor ve bütün olarak dışarı taşınabildiği için T-A/2'yi foreclose etmiyor. `DECISIONS` adı, dosyaya hangi bilgi türünün ait olduğunu adıyla zorluyor — "LOG" yalnızca-eklenir olan her şeyi davet ediyordu.
- **Alternatifler:** `payload/` (elendi: iç içe topolojiyi sabitliyor) · hiç değiştirmemek (elendi: şu an maliyet sıfır, altı hafta sonra değil) · `STATE.md` → `MEMORY.md` (elendi: açık bir T-B'yi gizlice karara bağlardı).
- **Geri alma:** Ucuz şimdi, orta ileride — bu yüzden şimdi.
- **Kanıt:** `[varsayıldı]` — çok-projeli kullanımın gerçekleşip gerçekleşmeyeceği ölçülmedi.

## 2026-08-15 · Sistem adı: AIOS · T-C

- **Karar:** `ai-os` → `AIOS`. Akronim olarak büyük harf; yönetilen projeler kebab-case slug.
- **Gerekçe:** Kategori adı yerine özel ad; dizin, komut ve konvansiyon adı aynı kalır.
- **Not:** `AIOS` kısaltmasının açılımı bir yere yazılmalı — altı ay sonra okuyan Claude olacak. `[varsayıldı]` Akademik literatürde aynı adlı bir LLM ajan OS çalışması var; kişisel sistem olduğu için pratik maliyeti yok.

## 2026-08-15 · Topoloji C onaylandı · T-A · onaylandı

- **Karar:** AIOS ve yönetilen projeler fiziksel olarak ayrı, kardeş dizinler: `Documents/Projects/AIOS/` + `Documents/Projects/<proje>/`. Projeler AIOS'un içinde yaşamaz.
- **Gerekçe:** Asimetri belirleyici oldu — "ayrı dursun" her üç geleceğe uyumlu ve maliyeti sıfır; "içinde yaşasın" ayrılmak istendiğinde git ameliyatı gerektirir. Ayrıca ADR literatüründeki bulgu: işten uzakta yaşayan karar kayıtları terk edilir, dolayısıyla her projenin kararları kendi deposunda yaşamalı.
- **Alternatifler:** A projeler AIOS içinde (elendi: karışık git geçmişi, bağımlılık karışması, STATE kirlenmesi) · B düz kardeşlik mekanizmasız (C'nin alt kümesi; mekanizma çalışmazsa doğal geri çekilme noktası).
- **Geri alma:** Şimdi ucuz, ilerideyse pahalı — bu yüzden şimdi.
- **Kanıt:** `[gözlendi]` — Claude Code'un tek çalışma dizini sınırı, C'nin sürtünmesini hemen görünür kılıyor.

## 2026-08-15 · Paylaşım mekanizması ertelendi · T-B

- **Karar:** Konvansiyonların projelere nasıl aktarılacağı (kullanıcı seviyesi CLAUDE.md / skill / şablon kopyası) kararlaştırılmadı. Pilot süresince Claude Code `Documents/Projects/` kökünde başlar — mekanizmasız çözüm.
- **Gerekçe:** Kökte çalışmak rahatsız ederse mekanizma gerekiyor demektir; etmezse gerekmiyor. Karar vermek yerine sinyal toplanıyor.
- **Geri alma:** Ucuz.
- **Kanıt:** `[varsayıldı]`.

## 2026-08-15 · Proje adı: knowledge-base · T-C

- **Karar:** `kb-slice` → `knowledge-base`. Alt dizinler `source/`, `output/`. Şimdilik kendi STATE/DECISIONS'ı yok.
- **Gerekçe:** Eski projenin gerçek adı bu — console script'i `knowledge-base` idi; ad icat edilmiyor. `KB` elendi (kısaltmalar çürür, ambigü), `KnowledgeBase` elendi (PascalCase, kebab-case kardeşleriyle çakışır). Dilim `knowledge-base` projesinin bir dilimidir, ayrı bir proje değil — ayrı adlandırmak ileride yeniden adlandırma gerektirirdi.
- **Geri alma:** Ucuz.
- **Kanıt:** `[gözlendi]` — eski proje belgelerindeki CLI adı.

## 2026-08-15 · Girdi mutabakatı çalıştırılır, sorulmaz · T-B

- **Karar:** Makine/dünya durumu hakkındaki iddialar rapordan alınmaz; komutla doğrulanır. Girdi mutabakatı bir komut dizisidir, bir soru değil.
- **Gerekçe:** Dilim-1 mutabakatı iki kalemde birden yanlıştı (typst yanlış olumsuz, kaynak sayfa yanlış olumlu) çünkü sahibe sorularak yapıldı ve sonucu `[gözlendi] — sahibin beyanı` diye kaydedildi. Bu etiket yanlıştı: beyan, niyet ve tercih için kanıttır, makine durumu için değil. Protokolün kendi "ölçümler alınır, istenmez" kuralı ihlal edilmişti.
- **Alternatifler:** Dördüncü kanıt etiketi `[bildirildi]` eklemek (elendi: kural netleşince vaka ortadan kalkıyor, taksonomi şişirmeye gerek yok) · oturuma özgü hata sayıp geçmek (elendi: eski projenin Revizyon 16 hatasının küçük ölçekli tekrarı).
- **Geri alma:** Ucuz.
- **Kanıt:** `[gözlendi]` — dilim-1 oturum 1'de iki yanlış işaretin ikisi de doğrulandı.

## 2026-08-15 · Sahip ile yazar ayrıldı · T-B

- **Karar:** `STATE.md`'yi Claude yerinde güncelleyebilir, sahip diff'i onaylar. Claude'un yazamayacağı üç alan tanımlandı: başarı ölçütü, T-A kararının çözüldü işareti, risk satırının silinmesi. `DECISIONS.md` herkes için yalnızca-eklenir kalır, sahip dahil.
- **Gerekçe:** Sahibin onayı meşruydu; eksik olan yetkinin sınırıydı. "Sahip" ve "tek yazıcı" dosyalarda aynı şeymiş gibi kullanılmıştı. Tek-yazıcı ilkesi eşzamanlı çakışan yazımı yasaklıyordu, sırayla yazıp diff onaylamayı değil — ihlal yok, terim karışıklığı vardı.
- **Alternatifler:** Yetkiyi tümüyle geri almak (elendi: bayat STATE'i sahibin elle güncellemesi dikkat bütçesini yakıyor) · sınırsız yazma yetkisi (elendi: başarı ölçütü sessizce değişebilirdi).
- **Geri alma:** Ucuz — sinyal tanımlı: STATE'te tanınmayan satır.
- **Kanıt:** `[gözlendi]` — sahibin açık onayı.

## 2026-08-15 · items.md matematik lehçesi · T-C

- **Karar:** Oturum 2'nin ilk işi LaTeX → typst dönüşümü; bilinçli yapılacak, tesadüfen değil.
- **Gerekçe:** items.md `$$...$$` ve `\,` gibi LaTeX sözdizimi taşıyor; typst'te display math `$ ... $` (boşluklu). Dosyanın kendisi "LaTeX paketi aramaya gerek yok" derken içeriği LaTeX. Çeviri, "kaynakla eşleşiyor" ölçütünün zarar gördüğü yerdir.
- **Kanıt:** `[gözlendi]` — items.md içeriği okundu.

## 2026-08-15 · Vizyon belgesi ayrıştırıldı; eksik okuma düzeltildi · T-B

- **Karar:** `REQUIREMENTS.md` oluşturuldu — 43 gereksinim, 4 tercih, 17 hipotez, 8 açık soru.
- **Düzeltme:** İlk ayrıştırma belgenin 60–103 satırları (§3'ün sonu, §4'ün tamamı) okunmadan yapıldı. Okunduğunda G40–G43 eklendi ve "§3 vs §18 gerçek gerilim" işaretlemesi geri alındı — §3 kendi ölçütünü zaten veriyor (soru verimi, soru sayısı değil).
- **Kanıt:** `[gözlendi]` — atlanan satırlar sonradan okundu.

## 2026-08-15 · Uygulama sıralaması · T-B

- **Karar:** v1 salt-okunur gösterge paneli; S1/S2 kararlaştıktan ve model 1–2 hafta gerçek işte kullanıldıktan sonra. Teknoloji seçimi (S3) o adıma ertelendi.
- **Gerekçe:** Salt-okunur olmak state bozulma riskini ve tek-yazıcı çakışmasını ortadan kaldırır; §21'in dokuz maddesi zaten okuma. Uygulama bilgi mimarisinin görüntüsü olduğu için modelden önce yapılırsa yeniden yazılır. Gerçek veriyle doğması, olmayan içeriğe göre ekran tasarlamayı önler.
- **Alternatifler:** Erken iskelet (elendi: boş ekranlar, kesin yeniden yazım) · en sona bırakmak (elendi: G4 ve G30 aylarca teslim edilmez).
- **Oyalanma freni:** S1/S2 kararından sonra 3 hafta içinde uygulama işi başlamazsa duraklama sinyali.
- **Kanıt:** `[varsayıldı]`.

## 2026-08-15 · S1/S2 araştırması sonrası depolama mimarisi · T-A · onaya açık

- **Karar:** Markdown + git kaynak-of-truth. Obsidian yalnızca insan görünümü, agent-kritik bağımlılık yasak. Knowledge graph reddedildi. Vektör store ve SQLite kaynak değil, sonraki adımlarda indeks katmanı olarak.
- **Gerekçe:** Uzun ömür ve lock-in'e karşı direnç belirleyici oldu — model ve araçlar bir yıl içinde değişince markdown+git hayatta kalır, indeksler yeniden kurulabilir. Knowledge graph tek kullanıcı için işletilemez (konuşma başına 600.000+ token ayak izi, arka plan işleme).
- **Alternatifler:** Letta/PostgreSQL (elendi: standing infrastructure, çürür) · Zep/Graphiti (elendi: ayak izi) · bulut memory servisleri (elendi: lock-in, gizlilik).
- **Geri alma:** Orta — biçim değişimi migrasyon gerektirir, ama markdown her hedefe dönüştürülebilir.
- **Kanıt:** `[gözlendi]` — S1/S2 araştırma raporu; benchmark sayıları taraflı olduğu için vendor iddiaları olduğu gibi alınmadı.

## 2026-08-15 · G32 için kapı tasarımı: tetikleyici ve eşleştirme ayrıldı · T-A · onaya açık

- **Karar:** v1 kapısı Claude Code Stop hook'u olarak kurulur. Yanıt üretildikten sonra `REJECTED.md`'ye karşı taranır; eşleşme varsa tamamlanma bloke edilir ve red gerekçesi geri beslenir. v1'de embedding ve LLM-judge YOK — yalnızca tetikleyicinin çalışıp çalışmadığı test edilir.
- **Gerekçe:** İki bileşen bağımsız; eşleştirme kalitesine yatırım, tetikleyici çalışmıyorsa tamamen boşa gider. Araştırma iki bağımsız kanıt hattıyla "yaz ve umut et"in başarısız olduğunu gösteriyor (NASA LLIS denetimleri 2002/2012; agent'ların enjekte edilmiş hafızayı fiilen atlaması). Kanıtlanmış tek kaldıraç deterministik script.
- **Alternatifler:** SessionStart ile bağlam yükleme (elendi: araştırma tam olarak bunun başarısız olduğunu gösteriyor — bir vakada model enjekte edilen hafızayı prompt injection sanıp reddetti) · kullanıcının `/propose` komutuyla tetiklemesi (elendi: disipline bağlı) · doğrudan tam sistem (elendi: yanlış sırayla yatırım).
- **Yanlış baskılama koruması:** Kapı asla sessizce reddetmez; eşleşmeyi ve gerekçeyi gösterip devam izni sorar. Araştırmadaki en ciddi çöküş modu buydu — agent bir yaklaşımın hep başarısız olduğuna yanlış kanaat getirirse onu bir daha denemez.
- **Yanlışlama testi:** 20 kasıtlı tekrar-öneri. Kapı %80'in altında yakalarsa veya hiç ateşlemezse tasarım yanlıştır.
- **Geri alma:** Ucuz — tek hook script'i.
- **Kanıt:** `[varsayıldı]` — hook'un bu senaryoda güvenilir ateşlediği henüz ölçülmedi.

## 2026-08-15 · Yalnızca REJECTED.md oluşturulur · T-C

- **Karar:** `FAILURES.md` ve `ASKED.md` şimdilik oluşturulmaz.
- **Gerekçe:** Kendi kuralımız — okuma tetikleyicisi yazılamayan dosya var olmamalı. İkisinin de tetikleyicisi henüz inşa edilmedi.
- **Kanıt:** `[gözlendi]`.

## 2026-08-15 · Kapı v1 inşa edildi ve yanlışlama testi geçti · T-B

- **Karar:** Stop hook tabanlı kapı kuruldu. `REJECTED.md` (5 onaylı kayıt), `hooks/gate.py`, `tests/test_gate.py` (20 vaka), `settings.json`.
- **Sonuç:** İlk koşu KALDI — %60 yakalama. Kök neden tek bir hataydı: Türkçe büyük-I dönüşümü `AIOS` → `aıos`, `NIM` → `nım` yapıyordu, anahtarlar ise `aios`/`nim` yazılıydı. Kısaltmalar Türkçe kuralına kurban gitmişti. Düzeltme: her iki tarafta simetrik `ı` → `i` katlaması. İkinci koşu: **%100 yakalama, %0 yanlış-pozitif.**
- **Gerekçe:** Test önceden yazılmış karar kuralıyla (≥%80 yakalama, ≤%20 yanlış-pozitif) koşuldu; sonuca bakılıp eşik ayarlanmadı.
- **Kanıt:** `[gözlendi]` — test çıktısı, iki koşu.
- **Uyarı:** Bu test yalnızca EŞLEŞTİRME katmanını ölçtü. Hook'un Claude Code içinde gerçekten ateşlediği HENÜZ ÖLÇÜLMEDİ; kanıtı `.gate-canary.log` dosyasıdır ve canlı ortamda kontrol edilmelidir. Asıl riskli varsayım budur.

## 2026-08-15 · Hook yapılandırması kullanıcı seviyesinde · T-B

- **Karar:** `settings.json` içeriği `C:\Users\Atakul\.claude\settings.json` dosyasına (mevcut içeriğe ekleyerek) yerleştirilir, proje seviyesine değil.
- **Gerekçe:** Claude Code proje ayarlarını başlatıldığı dizinden okur. Proje seviyesinde tutulursa kapı yalnızca doğru klasörden başlatıldığında ateşler — yani "hatırlamaya" bağlı hale gelir. Kapının varlık sebebi tam olarak hatırlamaya güvenmemekti; Stop hook'u SessionStart'a tercih etme gerekçesiyle aynı ilke.
- **Alternatifler:** `Projects/.claude/settings.json` (elendi: başlatma dizinine bağımlı) · her projeye ayrı kopya (elendi: senkronizasyon yükü, kopyalar sapar).
- **Geri alma:** Ucuz — tek dosya taşınır.
- **Kanıt:** `[varsayıldı]` — kullanıcı seviyesi hook'ların her oturumda yüklendiği canary ile doğrulanacak.

## 2026-08-15 · T-A/2 sınırı ikiliden üçlüye genişledi · T-A · onaya açık

- **Karar:** Sınır AIOS / PROJECT ikilisi değil, AIOS / PROJECT / **ENVIRONMENT** üçlüsüdür. ENVIRONMENT, aracın kendi yapılandırmasını barındırır (`~/.claude/`), makineye özgüdür ve git'e girmez.
- **Değişmez kural:** Mantık AIOS'ta kalır, ENVIRONMENT'ta yalnızca ona bir işaret durur. Ortam bölgesindeki bir dosyanın silinmesi AIOS'tan bilgi kaybettirmemeli, yalnızca bir mekanizmayı devre dışı bırakmalı.
- **Gerekçe:** Dedektör `settings.json` üzerinde ateşledi — dosya hiçbir tarafa yerleşmiyordu. Bu, sınır tanımının eksik olduğunun sinyaliydi ve dedektör amacına uygun çalıştı.
- **Geri alma:** Ucuz — tanım değişikliği.
- **Kanıt:** `[gözlendi]` — dedektör gerçek bir vakada ateşledi.

## 2026-08-15 · Adaptör deseni: çekirdek taşınabilir, tetikleyici ortama özgü · T-A · onaya açık

- **Karar:** Kapı üç katmana ayrıldı. Çekirdek (`gate.py`, `REJECTED.md`) düz Python + markdown, taşınabilir. Adaptör (`adapters/claude-code/hook.json`) araca özgü ama **AIOS'a ait**. Ortamdaki `~/.claude/settings.json` yalnızca kurulumun bıraktığı izdir, kaynak değildir.
- **Gerekçe:** Sahip haklı olarak AIOS'un Claude'a özel kurulmadığını hatırlattı (T4: sağlayıcıya kilitlenmeme). Yapılandırmayı aracın dizinine koymak AIOS'u o araca bağlıyordu. Dosyayı taşımak bağımlılığı kaldırmaz — deterministik bloklama bugün Claude Code'da yalnızca hook'larla mümkün, MCP sunucusu modelin çağırmayı hatırlamasını gerektirir ki reddedilen şey tam olarak budur. Doğru çözüm katmanı ayırmak: yarın `adapters/gemini-cli/` eklenir, çekirdek değişmez.
- **Kabul edilen sınır:** Hook mekanizması olmayan bir ortamda kapı bloke edemez, yalnızca uyarabilir. Taşınabilirliğin gerçek maliyeti budur.
- **Alternatifler:** MCP sunucusu (elendi: modelin hatırlamasına bağlı) · transcript izleyici (elendi: post-hoc, bloke edemez) · yapılandırmayı proje seviyesinde tutmak (elendi: başlatma dizinine bağımlı).
- **Geri alma:** Ucuz — `install.py --uninstall`.
- **Kanıt:** `[gözlendi]` — install.py sahibin gerçek settings.json'ı üzerinde test edildi: 7 anahtar korundu, yedek alındı, çift kurulum tekrar girdi üretmedi, kaldırma hooks'u temizledi.

## 2026-08-15 · Mevcut settings.json silinmeyecek · T-C

- **Karar:** Sahibin `~/.claude/settings.json` dosyası (model, effortLevel, tui, theme, bildirimler) korunur; `hooks` bloğu birleştirilerek eklenir. `install.py` bunu otomatik ve yedekli yapar.
- **Kanıt:** `[gözlendi]` — kuru çalıştırma çıktısı doğrulandı.

## 2026-08-15 · Tetikleyici doğrulandı; okuma katmanı kırık · T-B

- **Sonuç:** `.gate-canary.log` oluştu — `2026-08-15T18:54:07 ATEŞLEDİ yanıt boş`. **Bu aşamanın en riskli varsayımı çözüldü: Claude Code Stop hook'u gerçekten ateşliyor.** Eşleştirme testi sahibin makinesinde de %100/%0 geçti.
- **Yeni sorun:** Kapı ateşliyor ama transcript'ten yanıt metnini çıkaramıyor, dolayısıyla hiçbir zaman eşleşme bulamaz. İki hipotez: (a) transcript şeması varsayımdan farklı, (b) Stop hook son mesaj diske yazılmadan ateşliyor (yarış koşulu).
- **Yapılan:** Çıkarıcı toleranslı hale getirildi (dört farklı şema varyantı sentetik olarak test edildi, hepsi geçti) + 4 denemelik kısa yeniden-deneme eklendi (yarış koşulu için) + canary artık transcript yolunu ve yanıt uzunluğunu kaydediyor. Teşhis aracı yazıldı: `tests/diagnose_transcript.py`.
- **Gerekçe:** Hangi hipotezin doğru olduğunu tahmin etmek yerine ölçmek. Toleranslı çıkarıcı iki hipotezi de kapsıyor; teşhis aracı hangisi olduğunu söyleyecek.
- **Kanıt:** `[gözlendi]` tetikleyici için · `[varsayıldı]` düzeltmenin işe yaradığı için — canlı doğrulama bekliyor.

## 2026-08-15 · settings.json'da model anahtarı kayboldu · T-C

- **Gözlem:** Sahibin paylaştığı sürümde `model: opus` ve `effortLevel: high` vardı; kurulum sırasında `model` yok ve `effortLevel: medium`. `install.py` anahtar silmez (mevcut 7 → sonra 7). Değişikliği başka bir şey yaptı, muhtemelen Claude Code'un kendisi.
- **Eylem:** Yalnızca kayda geçirildi. Eski hal `settings.json.bak-*` dosyalarında duruyor.
- **Kanıt:** `[gözlendi]` — kurulum çıktısı.

## 2026-08-15 · Kapı uçtan uca doğrulandı; sidechain koruması eklendi · T-B

- **Sonuç:** `19:00:56 ATEŞLEDİ temiz | 5 kayıt | yanıt 1118 karakter`. Tetikleyici ve okuma katmanları kanıtlandı. Doğrulanmamış tek halka: eşleşme bulunca bloke etme.
- **Sertleştirme:** Gerçek transcript yapısında `isSidechain` alanı görüldü — subagent mesajları aynı dosyaya yazılıyor. Kapı artık onları atlıyor; aksi halde ana yanıt yerine subagent metnini tarayabilirdi. Sentetik testlerde bu alan yoktu; yalnızca gerçek veriye bakıldığı için yakalandı.
- **Kapanan konu:** `model`/`effortLevel` değişikliğini sahip yapmış. `install.py` şüphesi kalktı.
- **Kanıt:** `[gözlendi]` — canary log ve teşhis çıktısı.

## 2026-08-15 · Eşleştirici Türkçe çekimde kırıldı; test kendini doğruluyormuş · T-B

- **Gözlem:** Kapı gerçek bir eşleşmeyi kaçırdı. Claude Code "Projeleri AIOS **içine** almak" yazdı; anahtar "projeleri aios **içinde**" idi. Tek harflik ek farkı sabit-ifade aramasını kırdı.
- **Daha önemlisi:** İlk 20 vaka anahtarlarla aynı ifadelerle yazılmıştı — test kendini doğruluyordu ve %100 skoru sahteydi. Bu, `[gözlendi]` etiketini bir beyandan almakla aynı sınıftan hata: ölçüm, ölçtüğü şeyden bağımsız değildi.
- **Düzeltme:** Sabit ifade araması yerine üç kısıt birlikte — (1) kaba kök eşleşmesi (4 karakter) Türkçe çekimi tolere eder, (2) sıralı alt-dizi araması kelime sırasını korur, (3) pencere dağınık eşleşmeyi engeller. Tek kelimelik anahtarlar kök yerine tam eşleşme ister ('graphiti' kökü 'grap' olup 'graph' ile çakışıyordu).
- **Test seti düzeltildi:** Canlı oturumdan alınan GERÇEK metin pozitif vaka olarak eklendi; gevşek eşleştiriciyi yakalayacak iki tuzak negatif eklendi. Ara sonuç %17 yanlış-pozitif verdi (eşiğin altında ama rahatsız edici), sıra kısıtı eklenince **11/11 yakalama, 0/12 yanlış-pozitif**.
- **İkinci gözlem:** Claude Code bu vakada doğru davrandı — `CLAUDE.md`'deki kararı hatırlayıp tek başına uygulamayı reddetti. Ama araştırmanın bulgusu tam da buydu: model bazen hatırlar ve hatırlamadığında sessizce hatırlamaz. Kapı bunun yedeği, yerine geçeni değil.
- **Kanıt:** `[gözlendi]` — canary log ve gerçek transcript metni.

## 2026-08-15 · Kapı uçtan uca çalışıyor — dilim tamamlandı · T-B

- **Sonuç:** `19:21:27 BLOKE R-001`. Zincirin üç halkası da kanıtlandı: ateşliyor → okuyor → bloke ediyor. Claude Code tasarlandığı gibi davrandı: eşleşmeyi bildirdi, kapsamı değerlendirdi, kararı sahibe bıraktı, sessizce bastırmadı. `ATLANDI stop_hook_active` döngü korumasının çalıştığını gösterdi.
- **Ama testin sınırı:** Bu vakada Claude Code eşleşmeyi kapı ateşlemeden önce zaten kendisi bulmuştu, çünkü Topoloji C kararı `CLAUDE.md`'de yazılıydı. Yani kapı olmasa da doğru davranacaktı. Kapının asıl değeri, modelin bağlamında OLMAYAN redleri yakalamaktır ve bu henüz kanıtlanmadı. Gerçek test `CLAUDE.md`'de geçmeyen bir red gerektiriyor (R-002 veya R-004).
- **Kodlama düzeltmesi:** Windows konsolu UTF-8'i cp1252 sanıp blok mesajını bozuyordu. `sys.stderr.reconfigure(encoding="utf-8")` eklendi; canary log ilk oluşumda BOM ile yazılıyor (PowerShell ve Notepad BOM'suz UTF-8'i ANSI sanıyor).
- **Eklenen:** `--demo` bayrağı — kapıyı Claude Code olmadan denemek için. Uçtan uca test: exit kodu 2, doğru stderr, doğru canary satırı.
- **Bilinen sınır:** `stop_hook_active` koruması gereği kapı bir blokten sonra ikinci denemeyi taramaz. Sonsuz döngüyü önlemenin kabul edilen bedeli.
- **Kanıt:** `[gözlendi]` — canary log, Claude Code çıktısı, sentetik payload testi.

## 2026-08-15 · Kapının varlık sebebi kanıtlandı · T-A · onaya açık

- **Sonuç:** `19:40:36 BLOKE R-002`. Bu test öncekinden farklı ve belirleyici: `CLAUDE.md` ve `STATE.md`'de `zep`, `graphiti`, `knowledge graph` için **sıfır eşleşme** doğrulandı — model reddi bilmiyordu.
- **Kanıtın gücü:** Claude Code'un kapı öncesi yanıtı Zep'i olumlu değerlendirdi ("solid", "good fit") ve açıkça "bunu T-A olarak işaretler, 1-2 alternatife karşı yazılı eleme kriteri isterim" dedi — yani kararı AÇIK bir soru sandı. Oysa karar ölçülmüş kanıtla (600.000+ token ayak izi) kapatılmıştı. Kapı olmasaydı aynı araştırma yeniden yapılır, belki karar tersine dönerdi.
- **Değerlendirme:** Önceki test kapının çalıştığını gösterdi; bu test neden var olduğunu gösterdi. G32 artık varsayım değil, gözlem.
- **Kanıt:** `[gözlendi]` — canary log, model çıktısı, dosya araması.

## 2026-08-15 · Kabul edilen sınır: kapı önlemez, düzeltmeye zorlar · T-B

- **Gözlem:** Stop hook yanıt üretildikten SONRA ateşliyor. Kullanıcı reddedilmiş öneriyi bir kez görüyor, ardından düzeltmeyi görüyor.
- **Neden değiştirilemez:** Claude Code'da düz metin yanıtı bir araç çağrısı değil; `PreToolUse` gibi önceden ateşleyen bir kanca yok.
- **Kabul:** Sessiz tekrar imkânsız hale geliyor — kazanılan şey bu. Önleme değil, zorunlu düzeltme.
- **Kanıt:** `[gözlendi]` — üç adımlı akış canlı gözlendi (yanıt → hook → düzeltilmiş yanıt).

## 2026-08-15 · Anahtarlar iki dilli yazılır · T-C

- **Karar:** Her `REJECTED` kaydının anahtarları hem Türkçe hem İngilizce ifade içerir. Beş mevcut kayıt güncellendi.
- **Gerekçe:** Model İngilizce yanıt verdi; eşleşme yalnızca `graphiti` ve `temporal knowledge graph` zaten İngilizce terimler olduğu için tuttu. Tamamen Türkçe anahtarlı bir kayıt İngilizce parafrazı kaçırırdı.
- **Doğrulama:** İngilizce metinlerle test edildi — "adopt BMAD framework" ve "graph based memory layer" artık yakalanıyor; 20 vakalık test seti hâlâ 11/11 ve 0/12.
- **Kanıt:** `[gözlendi]`.

## 2026-08-15 · Kaydetme yolu kuruldu · T-B

- **Karar:** `tools/reject.py` — taslak ekleme, onaylama, banka sağlığı. Kaydetme ZORLANMAZ; kolay yol + bayatlama dedektörü kurulur.
- **Gerekçe (asimetri):** Geri çağırma otomatik olmak zorundaydı çünkü başarısızlığı sessizdir — tekrar ettiğini fark etmezsin. Kaydetme başarısızlığı görünürdür: banka büyümüyorsa bellidir. Zorlama koymak, "red sinyali" için anahtar kelime taraması gerektirirdi ("hayır", "olmaz") ve sürekli yanlış ateşleyip gürültüye boğardı — benimsenmemeyi garantilerdi, ki kaçındığımız şeyin ta kendisi.
- **Onay mekanizması:** Kayıt `onay: BEKLİYOR` ile açılır ve kapıda **etkisizdir**. Claude serbestçe taslak yazabilir; yalnızca sahip tarih girerek aktive eder. Uydurulmuş bir kuralın bankaya sızıp kalıcılaşması böyle engellenir (Honest Lying: ExpeL'de iki oyla kalıcılaşan uydurma kural).
- **Bulunan hata:** Mevcut `parse_rejected` yalnızca `onay` alanının dolu olmasına bakıyordu — "BEKLİYOR" da doluydu, yani onaysız kayıtlar aktif sayılırdı. Onay artık `YYYY-AA-GG` biçiminde bir tarih olmak zorunda.
- **Doğrulama:** Uçtan uca test — taslak eklendi, kapı görmedi, onaylandı, kapı gördü. `[gözlendi]`
- **Bayatlama:** 21 günden uzun süre kayıt eklenmezse `--durum` uyarı veriyor. NASA LLIS'in ölüm biçimine karşı tek dedektör.
- **CLAUDE.md:** Kapı ve kaydetme kuralları eklendi; 67 → 92 satır.

## 2026-08-16 · Dil ayrımı: makineye bakan İngilizce, konuşma kaydı Türkçe · T-B

- **Karar:** Kod, tanımlayıcı, yorum, docstring, CLI bayrakları, çıktı mesajları, log olayları, `REJECTED.md` alan adları ve `CLAUDE.md` **İngilizce**. `DECISIONS.md`, `STATE.md`, `REQUIREMENTS.md` ve red kayıtlarının `reason`/`scope` metni **Türkçe**. Red **anahtarları iki dilli** kalır.
- **Gerekçe:** Sahip kodların İngilizce olabileceğini bildirdi. Mevcut durum en kötüsüydü — `gerekce`, `guc` gibi ASCII'ye kırpılmış Türkçe tanımlayıcılar ne okunabilir ne doğru. `CLAUDE.md` İngilizce çünkü modele her oturumda *talimat* olarak okunuyor. Diğer belgeler Türkçe çünkü sahibin okuduğu, konuşmalarımızın nüansını taşıyan kayıtlar.
- **Göç:** `anahtarlar→keys`, `gerekçe→reason`, `kapsam→scope`, `güç→strength` (kesin→firm, kısmi→partial), `alternatif→alternative`, `onay→approved`. Log olayları `ATEŞLEDİ→FIRED`, `BLOKE→BLOCKED`, `ATLANDI→SKIPPED`. CLI `--ekle→--add`, `--onayla→--approve`, `--durum→--status` vb.
- **Zamanlama gerekçesi:** Beş kayıtla göç ucuz; elli kayıtla ayrıştırıcı + veri + araç üçlü göçü gerekirdi.
- **Doğrulama:** `[gözlendi]` — test 11/11 ve 0/12, `--status` 5 aktif kayıt, `--demo` R-002'yi hâlâ yakalıyor, İngilizce metin R-004'ü yakalıyor.
- **Not:** Türkçe metin normalizasyonu (kök, `ı→i` katlama) DEĞİŞMEDİ — eşleştirilen içerik hâlâ Türkçe, yalnızca kodun dili değişti.

## 2026-08-16 · STATE.md gerçeğe döndürüldü · T-B

- **Sorun:** `STATE.md` bayat kalmıştı — hâlâ "pilot yük = knowledge-base", "Dilim-1 = tek sayfadan üç öğe → PDF", "Oturum 2 buradan başlar" yazıyordu. Yön haftalar önce değişmişti; bayat satır silinmemişti. STATE'in tek işi güncel gerçeği tutmaktı ve yapmıyordu.
- **Yapılan:** Yerinde yeniden yazıldı. Yol haritası, çalışan yetenekler, açık T-A'lar, dil ayrımı ve riskler güncellendi. Knowledge-base "park edildi, Aşama 4'te doğrulama yükü olarak döner" diye işaretlendi. 748 kelime, 2 sayfa tavanının altında.
- **Sahibin onayına bırakılan:** Başarı ölçütü §1 "pilot yük" derken knowledge-base'i kastediyordu; yük artık AIOS'un kendisi. Kriter-1 bu okumayla zaten karşılanmış olabilir. Claude başarı ölçütünü değiştiremez (CLAUDE.md kuralı), bu yüzden soru olarak bırakıldı.
- **Kanıt:** `[gözlendi]` — eski STATE içeriği okundu ve gerçekle karşılaştırıldı.

## 2026-08-16 · Onaysız T-A birikimi tespit edildi · T-C

- **Gözlem:** Üç T-A "onaya açık" olarak yazıldı, sahip ilerledi ama açıkça onaylamadı: üçlü sınır, adaptör deseni, kapının varlık sebebi. Protokolün kendi kuralı "sessizlik onay değildir" ihlal ediliyordu.
- **Eylem:** STATE'e `[incelenmedi]` listesi olarak eklendi ve risk tablosuna aktif risk olarak yazıldı. İki haftalık gözden geçirme atlanırsa WIP limiti 1'e düşer.
- **Kanıt:** `[gözlendi]` — DECISIONS girişleri tarandı.

## 2026-08-16 · Beş karar onaylandı; karar tahtası boşaldı · T-A · onaylandı

- **Onaylananlar:** (1) Üçlü sınır AIOS/PROJECT/ENVIRONMENT · (2) Adaptör deseni · (3) Kapının varlık sebebinin kanıtlanması · (4) T-A/1 çözüldü: iş birimi = "tek yetenek + yanlışlanabilir test" · (5) T-A/2 T-B'ye indi.
- **Sonuç:** Açık T-A yok, onay bekleyen yok. WIP 0/3.
- **Kanıt:** `[gözlendi]` — sahibin açık onayı.

## 2026-08-16 · Süreklilik testi yapıldı — dosyalar yeterli · T-B

- **Sonuç:** Sıfır bağlamlı yeni bir oturum, tek cümlelik istemle ("Read the files and tell me where we are and what comes next") aşamayı, kapının kanıtlanmış olduğunu, test sayılarını, sıradaki işi, onay bekleyen kararları ve §1'deki açık soruyu doğru çıkardı. **Bilgi mimarisi bağlamı taşıdı.**
- **Ölçülmeyenler:** Süre ve "neyi yeniden anlatmak zorunda kaldın" raporlanmadı. İkincisi testin en değerli çıktısıydı; bir sonraki devirde ölçülecek.
- **Sınır:** Bu test dosyaların yeterliliğini kanıtladı, A1'in "3 hafta ara → 15 dakika" ölçütünü değil. O ölçüm zamanı geldiğinde yapılacak.
- **Kanıt:** `[gözlendi]` — oturum çıktısı.

## 2026-08-16 · STATE §4 kusurlu yazılmıştı; tek listeye indirgendi · T-B

- **Bulgu:** §4'te iki farklı anlamda liste yan yana duruyordu — *çözülmeyi bekleyen açık kararlar* (T-A/1, T-A/2) ve *onay bekleyenler* (üçlü sınır, adaptör deseni, kapı kanıtı). Süreklilik testinde yeni oturum ikisini birleştirdi, sayıyı (3) doğru tutturdu ama içeriği karıştırdı ve **adaptör desenini tamamen düşürdü**.
- **Önemi:** "Önemli bir karar görünmez oldu" — G4'ün korumaya çalıştığı arızanın canlı örneği. Suç modelde değil, belge yapısında.
- **Düzeltme:** Tek tablo + `durum` sütunu. Benzer görünen iki liste yan yana durmayacak. Kural gerekçesiyle birlikte STATE'e yazıldı ki tekrar edilmesin.
- **Kanıt:** `[gözlendi]` — oturum çıktısı ile STATE içeriği karşılaştırıldı.

## 2026-08-16 · Kriter-1 karşılanmış sayılmıyor · T-A · karar

- **Karar:** Yük artık AIOS'un kendisi olduğu için kriter-1 ("gerçek iş planlama aşamasını geçip saklanacak bir çıktı üretti") teknik olarak okunabilirdi — kapı gerçek ve çalışıyor. Yine de **karşılanmış sayılmıyor.**
- **Gerekçe:** Bir günlük bir yetenek "saklanacak çıktı" değildir; ölçüt sistemin zaman içinde kullanımda kalmasını sorar. Birinci günde kendi ölçütünü geçmiş saymak, baştan beri kaçındığımız kendini-doğrulayan ölçümün ta kendisi olurdu — test setini anahtarlarla aynı ifadelerle yazmakla aynı hata sınıfı.
- **Kanıt:** `[varsayıldı]` — 2026-11-15'te yeniden değerlendirilecek.

## 2026-08-16 · `kapatır:` konvansiyonu benimsendi · T-A · onaylandı

- **Karar:** Bir T-A kararı onaylandığında veya reddedildiğinde, kapatan giriş her bir madde için `- **kapatır:** TARIH/Tam başlık` biçiminde ayrı bir satır taşımak zorundadır. Bu satır olmadan giriş kapatma sayılmaz.
- **Gerekçe:** `DECISIONS.md` yalnızca-eklenir olduğu için bir kararın durumu yalnızca sonraki bir girişle değişebilir; `tools/review.py` bekleyen T-A'ları bu bağlantı üzerinden kapalı sayar. 2026-08-16 tarihli "Beş karar onaylandı" girişi tam olarak bu eksiklikle yazıldı — üç maddeyi (üçlü sınır, adaptör deseni, kapı kanıtı) onayladı ama `kapatır:` satırı taşımadığı için `review.py` onları hâlâ bekliyor sayıyor. Sessiz bayatlamayı önleyecek tek mekanizma bu bağlantı olduğundan, eksikliği kendisi bir T-A: yanlış çıkarsa görünürlük sessizce bozulur.
- **Alternatifler:** Durumu serbest metinle anlatmak (elendi: `review.py` script'i bunu ayrıştıramaz, insan okuması gerekir) · `DECISIONS.md`'yi düzenlenebilir yapmak (elendi: yalnızca-eklenir ilkesini bozar, CLAUDE.md ile doğrudan çelişir).
- **Geri alma:** Ucuz — format kuralı, geçmiş girişler yeni kapatma girişleriyle düzeltilebilir.
- **Kanıt:** `[gözlendi]` — "Beş karar onaylandı" girişinin `kapatır:` satırı taşımadığı ve bu yüzden `review.py`'nin ilgili T-A'ları hâlâ açık sayması.

## 2026-08-16 · 2026-08-15 tarihli altı T-A kararı kapatıldı · T-A · onaylandı

- **Karar:** Aşağıdaki altı T-A kararı sahip tarafından onaylanmış kabul edilir ve `kapatır:` bağlantısıyla resmen kapatılır.
- **kapatır:** 2026-08-15/A2 prior-art taraması yapıldı
- **kapatır:** 2026-08-15/S1/S2 araştırması sonrası depolama mimarisi
- **kapatır:** 2026-08-15/G32 için kapı tasarımı: tetikleyici ve eşleştirme ayrıldı
- **kapatır:** 2026-08-15/T-A/2 sınırı ikiliden üçlüye genişledi
- **kapatır:** 2026-08-15/Adaptör deseni: çekirdek taşınabilir, tetikleyici ortama özgü
- **kapatır:** 2026-08-15/Kapının varlık sebebi kanıtlandı
- **Gerekçe:** Üçlü sınır, adaptör deseni ve kapı kanıtı zaten 2026-08-16 tarihli "Beş karar onaylandı" girişinde onaylanmıştı ama `kapatır:` bağlantısı taşımıyordu ([[kapatır-konvansiyonu-benimsendi]] bkz.). A2 prior-art ve S1/S2 depolama mimarisi ise hiçbir yerde açıkça kapatılmamıştı; sahibin ilerleyişi (A2 sonrası dilim-1'e geçilmesi, S1/S2 sonrası markdown+git üzerine inşa edilmesi) fiili onayı gösteriyor ama kayıt bunu hiç söylemiyordu. Bu giriş, `review.py`'nin bekleyen listesini gerçek duruma eşitler.
- **Kanıt:** `[gözlendi]` — altı girişin `DECISIONS.md`'de `T-A · onaya açık` olarak durduğu ve hiçbirinin önceki hiçbir girişte `kapatır:` ile hedeflenmediği doğrulandı.

## 2026-08-16 · `kapatır:` anahtarı eklere toleranslı; bağlanmayan bağlantılar DANGLING olarak raporlanıyor · T-C

- **Karar:** `kapatır:` satırının ayrıştırıcısı `TARIH/Başlık` sonrasına eklenen ek metne toleranslı — ayrıştırıcı başlığı kesiyor. Hiçbir kaydı kapatmayan `kapatır:` bağlantıları artık DANGLING olarak raporlanıyor.
- **Gerekçe:** Elle yeniden üretilen anahtar (tarih/başlık) er ya da geç yanlış üretilir; kural koymak yerine tolerans + tespit tercih edildi.
- **Kanıt:** `[varsayıldı]`.

## 2026-08-16 · `review.py` handoff yüzeyinin güvenilirliğini denetliyor · T-B

- **Karar:** `review.py` artık `STATE.md`'nin "Son güncelleme" damgasını denetliyor: damga en son karar tarihinden geriyse STALE uyarısı, damga hiç yoksa uyarı, içerik 900 kelime tavanını aşarsa uyarı.
- **Gerekçe:** G13 handoff'un doğrulanabilir olmasını istiyor; `STATE.md` içeriği taşıyordu ama güncel olup olmadığını söyleyen hiçbir şey yoktu ve haftalarca bayat kaldı — ancak elle okununca fark edildi. Kontroller sağlıklıyken sessiz kalıyor; 7 satır bütçesi korunuyor.
- **Alternatifler:** Ayrı bir handoff belgesi üretmek (elendi: `STATE.md` zaten o, ikinci belge sapma kaynağı olur) · elle gözden geçirmeye bırakmak (elendi: tam da başarısız olan yol).
- **Kanıt:** `[gözlendi]`.

## 2026-08-16 · G12 uzun oturum uyarısı `gate.py`'ye eklendi · T-B

- **Karar:** Transcript 120.000 karakteri aştıysa ve oturum başından beri ne `STATE.md` ne `DECISIONS.md` yazılmışsa, oturum başına bir kez uyarı verilir.
- **Gerekçe:** Risk uzunluk değil, dışarı yazılmadan uzamak — STATE ve DECISIONS güncellenerek geçen uzun oturum sağlıklıdır.
- **Eşik:** `[hipotez]`, `AIOS_SESSION_LIMIT` ile ayarlanabilir; hiç ateşlemezse düşür, oturum hâlâ iyiyken ateşlerse yükselt.
- **Kayıt:** Uyarı bir kez verilir, kaydı canary log'da tutulur — yeni dosya açılmadı.
- **Kabul edilen bedel:** Tavsiye tek kanal olan stderr'den gittiği için oturumda bir kez akışı kesiyor.
- **Alternatifler:** Yalnızca log'a yazmak (elendi: kullanıcı hiç görmez) · her turda uyarmak (elendi: gürültü, kapatılır).
- **Kanıt:** `[varsayıldı]`.

## 2026-08-16 · STATE.md Aşama 2/3 tamamlandığına göre yeniden yazıldı · T-B

- **Karar:** `STATE.md` 860 → 683 kelimeye indirildi; biten aşamaların ayrıntısı budandı, çalışan yetenekler ve iş bölümü eklendi.
- **Kanıt:** `[gözlendi]`.

## 2026-08-16 · Bayatlık dedektörünün sınırı gözlendi: zamansal, anlamsal değil · T-C

- **Gözlem:** `STATE.md` içerik olarak eskimişti (Aşama 2 ve 3 hâlâ "sırada" görünüyordu) ama tarih damgası taze olduğu için [[review-py-handoff-guvenilirligi-denetliyor]] uyarı vermedi. Dedektör zamansal bayatlığı yakalıyor, anlamsal bayatlığı değil.
- **Eylem:** Risk tablosuna eklendi; şimdilik çözülmüyor, kaydediliyor.
- **Kanıt:** `[gözlendi]`.

## 2026-08-16 · Sohbete durum aktarımı GitHub deposu üzerinden · T-B

- **Karar:** Sohbete durum aktarımı GitHub public deposu üzerinden yapılır (`github.com/omerfrkatkl/AIOS`); sohbet dosyaları `raw.githubusercontent.com` üzerinden seçerek okur. `bundle.py` yedek yol olarak kalır.
- **Gerekçe:** Bundle her seferinde 102.000 karakterin tamamını taşıyordu ve `DECISIONS.md` büyüdükçe büyüyecekti; depo seçici okumaya izin veriyor ve "hangi kopya gerçek" sorusunu tanımı gereği kapatıyor. Yeni altyapı değil — klasör zaten git deposuydu.
- **Kabul edilen bedel:** Depo public, yani karar geçmişi ve `hook.json` içindeki kullanıcı adı görünür.
- **Doğrulama:** 10 dosya çekildi, parmak izleri `--files` çıktısıyla birebir eşleşti; push edilmemiş iki dosya aynı kontrolde yakalandı.
- **Kanıt:** `[gözlendi]`.

## 2026-08-16 · Cowork degerlendirildi, sohbet + Claude Code korunuyor · T-B

- **Karar:** AIOS'un insasi ve planlamasi sohbet + Claude Code bolunmesiyle surer. Cowork kullanilmaz. R-006 olarak REJECTED'a kaydedildi.
- **Gerekçe:** Kapi bir Claude Code Stop hook'u; Cowork'te hook mekanizmasi yok ve is izole bulut ortaminda kosuyor. Gecis G32'yi sessizce devre disi birakir ve kayboldugu fark edilmez.
- **Alternatifler:** Cowork'e gecmek (elendi: G32 sessizce kaybolur) · Her ikisini kullanmak (elendi: iki onay yuzeyi)
- **Geri alma:** Ucuz - adapters/cowork/ yazilabilir, ama zorlayacak kanca yoksa yazacak sey de yok
- **Kanıt:** `[gözlendi]` — Anthropic destek dokumanlari incelendi

## 2026-08-16 · decide.py kanit etiketi ASCII ve Ingilizce alias kabul ediyor · T-C

- **Karar:** --evidence artik gozlendi/observed/uretildi/generated/varsayildi/assumed kabul ediyor, belgeye kanonik Turkce formu yaziliyor.
- **Gerekçe:** Sohbette verilen ilk decide.py komutu calisamadi: secenek listesi Turkce diakritik istiyordu, komut ASCII yazilmisti. CLI token'inda diakritik olmasi kendi dil kuralimizla celisiyordu - makineye bakan her sey Ingilizce olmaliydi. Toleransli girdi, kanonik cikti.
- **Kanıt:** `[gözlendi]` — Komut sessizce basarisiz oldu, Cowork girisi hic yazilmadi

## 2026-08-16 · Gözden geçirildi · T-C

- **Kapsam:** 57 karar gözden geçirildi.
- **Onay bekleyen:** 0 (yok)
- **Kanıt:** `[gözlendi]` — `tools/review.py --done`

## 2026-08-16 · PROFILE.md eklendi; kullanici tanima yol haritasina girdi · T-B

- **Karar:** PROFILE.md olusturuldu, her oturum basinda STATE ile birlikte okunuyor. Adaptive discovery mekanizmasi (G40-G43) yol haritasinda eksikti; simdilik gozlemler yaziliyor, soru sorma mekanizmasi sonraki asamada.
- **Gerekçe:** Sahibe dair her sey sohbetin icindeydi ve hicbir yerde yazili degildi; konusma bitince kaybolacakti - G14 ihlali. Mekanizma kurulmadan once elde olani kaybetmemek onceligi.
- **Alternatifler:** Mekanizmayi once kurmak (elendi: bu konusma bitmeden veri kayboluyor) · Ertelemeye devam (elendi: zaten unutulmustu, yol haritasinda hicbir asamada yoktu)
- **Geri alma:** Ucuz
- **Kanıt:** `[gözlendi]`

## 2026-08-16 · Talimatlara asama freni ve inceleme kurali eklendi · T-C

- **Karar:** Kural 13: asama freni hem sayiya hem takvime baglanir. Kural 14: onceki konusmanin yeni konusmayi incelemesi gerekiyorsa dosyalarda eksik satir var demektir - konusma degil dosya duzeltilir.
- **Gerekçe:** Yeni sohbete 'itirazlarimi tasi' denmisti; her konusma bir oncekinin onayina muhtacsa handoff olceklenmiyor. Inceleme yorumu artik eksik satirin dedektoru.
- **Kanıt:** `[gözlendi]`
