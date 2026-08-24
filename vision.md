# AIOS — Vizyon v2

| | |
|---|---|
| **Amaç** | Sahibin isteklerinin tek kaynağı — north-star belgesi |
| **Yaşam döngüsü** | Yerinde güncellenir; sahibin sözü esastır, mekanizma seçimi planın işidir |
| **Sahip** | Proje sahibi |
| **Okuma tetikleyicisi** | Her faz başı + her yeni oturum + mimari karar anı |

## 1. Kimlik — kişisel AI platformu

Yıllarca kullanacağım platform: hangi yapay zekâyı, hangi arayüzü, hangi modeli kullanırsam kullanayım aynı davranır — unutmaz, beni tanır, kararlarını araştırmaya dayanarak doğrular, beni fikirden sonuca taşır. "Tek cevap" ile "yıllarca sürecek proje" aynı sistemin iki ucudur.

## 2. Kalıcı beyin

Hafıza benim makinemdedir: state, karar geçmişi (neden), **onay/red/erteleme kayıtları**, profilim. Oturum/araç/model değişse beyin aynıdır; kaldığı yerden devam eder. Reddedilen öneri tekrar sunulmaz, ertelenen vaktinde hatırlatılır. Derin kişisel bilgim (tasarım zevki, uygulama tercihleri) Obsidian vault'umda yaşar; yapay zekâ bana sormadan oraya bakar — yalnızca ilgili nota, asla her şeyi okuyarak.

## 3. Çoklu-AI senkronu

Birçok yapay zekâ aynı beyin üzerinden senkron çalışır: **önce beyin, sonra bağlantı.** "Ana yapay zekâ" unvan değil, **yürütücü rolü**dür — her an değiştirilebilir. Yürütücü işi alt yapay zekâya devredebilir (ör. araştırma); çıktıyı kendisi toplar, değerlendirir, beyne yazar — birleştirme tek noktada olur. Yapay zekâlar bir kararı tartışabilir: sınırlı turda, çıktısı **öneridir** — karar hattına girer, son söz doğrulama sisteminin ve benimdir. **Bir yapay zekâ hata yaptıysa bu loglanır; sonraki yapay zekâ hata kaydına bakıp "önceki bunu yapmış, ben aynılarını yapmayayım" diyebilmeli** — bunu yapamayacağı kaynak türlerinde (web) çıktı sindirme ile telafi edilir.

## 4. Beni tanıması

Tek seferlik form değil, zamanla süren adaptif sorular: tekrar yok, cevaplar profile işlenir. Karar verme biçimimi, teknik ayrıntı ihtiyacımı, iletişim üslubumu bilir; bana "bana göre" konuşur.

## 5. Kaynak zekası

Aboneliklerim, API'lerim, ücretsiz kanallarım, yerel modellerim envanterdedir — limitleri ve tazelik tarihleriyle. Her görev için kanal+model+efortu kendisi seçer: *"bu iş ChatGPT free'de bedavaya yarar"*, *"Gemini API bugün boş — Pro değil, Flash medium yeter"*, *"Claude kotası dar, kritik review'e sakla"*. Limit bitince geçiş: API'de otomatik, chat'te bana öneri. **Yeteneği olmayan modele yetenek takviyesi** yapılır (web araması olmayana web-arama — OpenWebUI/LM Studio sınıfı yetenekler). Araçlar da aynı defterdedir: "bu iş typst ister, bu iş uv ister."

**Canlı kaynak istihbaratı:** sistem OpenRouter ve benzeri platformlarda yeni/ücretsiz/sınırsız modelleri arka planda denetler; "eski model yerine artık bu" diye beni bilgilendirir. Entegre ettiği her modelin **dosya yükleme limitini, sohbet kısıtını, token sınırını, arayüz kurallarını, girdi kabiliyetlerini (metin/görsel/video), araştırma/artifact gibi araçlarını** eksiksiz bilir (ör. "platform projesi: en fazla 5 dosya, 20 MB, 1000 karakter talimat"). Sınırlar değiştiğinde kendisi araştırıp test eder, stratejiyi anında günceller. Ben sözlü olarak bir değişiklik bildirirsem (ör. "limit 20 MB oldu") bunu anında merkezi bilgiye işler ve sonraki tüm yönlendirmeleri güncel veriyle yapar. Kullanım sınırlarını arka planda takip eder — "Claude'un limiti doldu, 3 saat sonra yenilenir" bilir ve beni tükenmiş bir modele yönlendirmez. Güncelleme ister otomatik ister manuel butonla olur.

## 6. Karar sistemi

Önce araştırma — kendisi bir motordur: doğru yöntemi seçer (web, dokümantasyon, prototip, benchmark, çapraz-model), raporu kanıt-etiketlidir, aynı soruyu yeniden araştırmadan önce geçmiş rapora bakar. **Araştırma devri yapabilir:** "Gemini Deep Research'te şu promptla araştır, sonucu getir", "Claude daha iyi araştırır ama limiti bitiyor — yarım saat beklemek ister misin?", "ücretsiz web araştırması da yeterli", "üçünü birden yaptır, hepsini getir" — bana bu tarz plan sunar, ben seçerim. Alternatifler **önceden sabitlenmiş boyutlarda puanlanır; her puan kanıta dayanır; ölçek 0–1'dir.** Puanlama iki katmanlıdır: **evrensel sabitler** (modülerlik, loglama, hata yönetimi, açık kaynak — her yerde kusursuz olmalı; ihlal eleme sebebidir) ve **proje ağırlıkları** (ben "bu projede hız önce" dersem ağırlıklar o proje için kayar). Kararlar izlenebilir (neden / alternatifler / kanıt / geri-alma maliyeti / yeniden değerlendirme koşulu) ve **zamanla sınanır** — sonuçlar puanlamayı kalibre eder. Sistem güvenilir olduğu alanda otonomlaşır, hata yaptığı alanda tekrar bana danışır. Benim önerim de, sistemin ilk önerisi de otomatik doğru değildir; ama sonsuz alternatif üretip karar vermeyen sistem de olmaz. **Web'den gelen bir çıktı sisteme yapıştırıldığında arka planda analiz edilir: gerçekten istediğim mi, daha önce yaptığım bir hatanın tekrarı mı?**

## 7. Yönlendirilmiş akış

Fikrimi yazarım, sorularını yanıtlarım; gerisini sistem taşır: netleştirme → araştırma → karar → plan → dilim dilim uygulama → test → teslim. "Hangi kütüphane?" cümlesini duymam; yalnızca yön/kapsam kararı olan noktalarda başvurulurum. Önemli kararlar bana görünürdür — **görünürlük ≠ onay**.

## 8. Arayüz ve teslim

Nihai yüzey **Windows uygulamasıdır**; görsel tasarım opencode'dan alınır/uyarlanır — tasarım için emek harcanmaz, emek arka plan sistemine gider. Uygulama **istemcidir**: sistem onsuz da çalışır. İçinde model seçici, tartışma arayüzü, araştırma görünümü, durum panosu, kota panosu, model matrisi, olay akışı, log görüntüleyici ve **normal sohbet modu** olur. **Parametre panelleri kanalın gerçeğine göre çizilir:** lokal modelde temperature/max-token gibi parametreleri ben değiştiririm; API/router'da ne izin veriliyorsa o kadarı; web-chat'te parametre görüntülenmez — platform her kaynağın türünü ayırt eder ve **o kaynağın gerçek imkânlarına uygun** arayüz sunar; hepsine tek kalıp dayatmaz.

## 9. Kaynak disiplini

Token, para, süre **ve benim dikkatim** kaynaktır. Oturum açılışında gereksiz hiçbir şey yüklenmez; en güçlü model ve en pahalı yol varsayılan olmaz; gereksiz soru, rapor, karar taşınmaz — önemli olan görünür kalır.

## 10. Modülerlik

Her şey eklenebilir ve çıkarılabilir olmalı: yeni araç, yeni yetenek, yeni kanal, yeni bilgi türü — basit işlemler. Bileşenler sözleşmeler ve kayıt defteriyle birbirine bağlanır; çekirdek hiçbirine kilitlenmez. Yenilikler geldikçe sistem bozulmadan büyür.

## 11. Loglama ve hata yönetimi

Her araç, her olay, tek standardda loglanır. Hata bana üç satırla gelir: **ne oldu / neden / ne yapmalıyım.** Teknik detay logdadır. Tekrarlanan hatalar sisteme öğrenme olarak işlenir.

## 12. Açık kaynak

AIOS ve onunla yapılan projeler açık kaynak standartlarına tam uyar (MIT; LICENSE, README, CHANGELOG, sürümleme).

## 13. Kalite standardı

İlk çözümle yetinmez ama sonsuz alternatif de üretmez; büyük vizyonu korur ama uygulanamaz plan üretmez; teknik ayrıntıyı benden alır ama önemli kararı gizlemez; otonomdur ama beni projeden koparmaz; bağlamı korur ama her şeyi sonsuza dek taşımaz.

## 14. Başarısızlık modları

Erken kapanma · gereksiz kapsam küçültme · aşırı planlama · planın gerçeklikten kopması · belge çürümesi · kararların görünmezleşmesi · çelişkili state · context kaybı · gereksiz token · dikkat aşırı yükü · habersiz önemli karar · hatasını doğrulayamama · ürettiğini gerçek sanma · eski kararın yeni gerçeklikle çelişmesi · sonsuz iyileştirme · metodolojiyi sürekli yeniden tasarlama · **sahte nesnellik (kafadan puan, sentetik kanıt)** · **arayüz kilidi** · **log gürültüsü**.

## 15. Önceki sistemden dersler

Çalışan mekanizma da periyodik kanıt ister · test, test ettiği şeyden bağımsız yazılır · beyan komutla doğrulanır · sessizlik onay değildir · tazelik tarihten değil içerikten anlaşılır · hatırlamaya güvenilmez, zorlama kurulur.

## 16. Başarı

AIOS kullanırken daha büyük, daha uzun, daha karmaşık projeleri **gerçekten bitirebiliyor muyum?** Somut, yanlışlanabilir başarı ölçütü gereksinimlerde tanımlanır ve ölçüm tarihi taşır.

## 17. Kullanım kuralı

Bu belge north-star'dır; nihai mimari ve teknoloji ayrıca araştırılır. Çelişki görülürse belirtilir, daha iyi yol biliniyorsa önerilir, gereksiz meta-planlamaya girilmez.
