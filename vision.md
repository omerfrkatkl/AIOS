# AIOS — Vizyon, Gereksinimler ve Kullanıcı Beklentileri

> Bu belge, AIOS'un ne olması gerektiğine dair kullanıcıdan gelen ham vizyonu ve beklentileri toplar.
>
> Bu belge nihai mimari, teknik tasarım veya implementasyon planı değildir.
> İçindeki çözüm fikirleri zorunlu kararlar olarak kabul edilmemelidir.
> AIOS'un tasarım sürecinde bu belge gereksinim, tercih, hipotez ve açık soru olarak ayrıştırılmalı; gerektiğinde eleştirilmeli, değiştirilmeli veya reddedilmelidir.

## 1. AIOS'un temel amacı

AIOS, kullanıcının uzun vadeli ve karmaşık projelerini yapay zekâ ile daha güvenilir biçimde hayata geçirmesine yardımcı olan kişisel bir AI çalışma sistemi olmalıdır.

Kullanıcı bir fikirle başlayabilmelidir:

**fikir → keşif → netleştirme → araştırma → planlama → uygulama → test → sürdürme**

AIOS bu sürecin teknik ve bilişsel yükünün mümkün olduğunca büyük bölümünü üstlenmelidir.

Kullanıcı ise projenin vizyonu, amacı ve önemli kararları üzerindeki sahipliğini korumalıdır.

AIOS'un amacı yalnızca "kod yazan bir ajan" olmak değildir.

Uzun vadede AIOS; proje yöneticisi, araştırmacı, planlayıcı, teknik karar yardımcısı, execution agent, reviewer, tester, kalıcı proje hafızası ve kişisel çalışma ortağı rollerini gerektiğinde birleştirebilmelidir.

Ancak bunların hangi teknik mekanizmalarla gerçekleştirileceği henüz kesin değildir.

## 2. Kullanıcının AIOS ile çalışma modeli

Temel kullanım modeli kabaca şöyledir:

1. Kullanıcının aklına bir fikir gelir.
2. Kullanıcı bunu doğal dille AIOS'a anlatır.
3. AIOS kullanıcıyla konuşur ve fikri netleştirir.
4. AIOS kullanıcıyı gerektiği kadar tanımaya çalışır.
5. AIOS hedefleri, gereksinimleri ve kısıtları ortaya çıkarır.
6. AIOS araştırılması gereken şeyleri belirler.
7. AIOS teknik seçenekleri ve çözüm yollarını araştırır.
8. AIOS uygulanabilir bir plan ve çalışma yöntemi oluşturur.
9. Kullanıcı önemli kararları görebilir ve gerektiğinde müdahale eder.
10. AIOS uygun araçları, modelleri ve execution stratejisini seçer.
11. AIOS gerekli implementation işini yürütür.
12. AIOS test eder ve gerçek çalışmayı doğrular.
13. AIOS proje state'ini günceller.
14. İleride yeni bir sohbet veya oturum açıldığında kritik bağlam kaybolmadan devam edebilir.

Bu akışın kesin mimarisi araştırılmalıdır.

## 3. Kullanıcının AIOS tarafından tanınması

Kullanıcı için kişiselleştirme kritik bir gereksinimdir.

AIOS zaman içinde kullanıcı hakkında anlamlı ve kalıcı bilgi edinebilmelidir. Örneğin:
- vizyonu,
- genel hedefleri,
- tercihleri,
- karar verme biçimi,
- ne kadar teknik ayrıntı istediği,
- hangi durumlarda seçenek sunulmasını istediği,
- hangi konularda AI'a daha fazla özgürlük verdiği,
- hangi konularda mutlaka kendisine danışılmasını istediği,
- tasarımsal tercihleri,
- iletişim tercihleri,
- geçmişte hangi yaklaşımlardan memnun kalmadığı,
- hangi proje türlerinde neyi önemsediği.

Kullanıcı kısa bir onboarding ile "tanınmış" sayılmamalıdır.

AIOS'un adaptive discovery / interview yapabilmesi istenir.

Kullanıcı gerekirse çok sayıda soruya cevap vermeye açıktır. Önemli olan soru sayısı değil, soruların kullanıcının modelini gerçekten geliştirmesidir.

Sorular:
- önceki cevaplara göre uyarlanmalı,
- tekrar etmemeli,
- gerektiğinde farklı açılardan aynı özelliği doğrulamalı,
- zaman içinde devam edebilmeli.

Kullanıcıyı tanıma süreci tek seferlik bir form olmak zorunda değildir.

## 4. Kullanıcının teknik ayrıntı yükünü azaltma

Kullanıcı çoğu projede "sonuçta ne istediğini" anlatmak istemektedir.

Kullanıcının teknik implementation ayrıntılarını önceden bilmesi beklenmemelidir.

Örneğin kullanıcı:

> "Farklı kalem türleri bulunan bir PDF uygulaması istiyorum."

dediğinde AIOS'un:

> "Hangi Python kütüphanesini kullanalım?"

gibi teknik kararları kullanıcıya geri itmesi istenmez.

Bunun yerine AIOS:
- ilgili teknolojileri araştırmalı,
- alternatifleri değerlendirmeli,
- teknik trade-off'ları incelemeli,
- kendi önerisini oluşturmalı,
- yalnızca gerçekten kullanıcı kararını gerektiren noktaları kullanıcıya getirmelidir.

## 5. Kullanıcı sahipliği ve karar görünürlüğü

AIOS mümkün olduğunca otonom çalışabilmelidir.

Ancak kullanıcı proje üzerindeki kontrolünü kaybetmemelidir.

Önemli ayrım:

**Karar görünürlüğü ≠ karar onayı**

Kullanıcı AIOS'un önemli kararlarını görebilmelidir.

Ancak her küçük teknik karar için kullanıcıdan manuel onay alınmamalıdır.

Özellikle:
- yüksek etkili,
- geri alınması pahalı,
- yön veya kapsam değiştiren,
- kullanıcının açıkça önem verdiği

kararlar kullanıcıya getirilmelidir.

Buna karşılık:
- basit,
- yerel,
- hızlı fark edilen,
- kolayca geri alınabilen

kararlar AIOS tarafından doğrudan çözülebilmelidir.

Tasarımsal konularda kullanıcıya seçenek sunulması tercih edilir. Örneğin:
- koyu / açık tema,
- pastel / parlak renkler,
- farklı arayüz stilleri.

Dosya silme, önemli ayar değiştirme veya kalıcı etkiye sahip işlemlerde de uygun karar sınırı bulunmalıdır.

Bu sınırın teknik olarak nasıl uygulanacağı araştırılmalıdır.

## 6. Büyük vizyonu koruma

Kullanıcının büyük fikirleri gereğinden fazla küçültülmemelidir.

Kullanıcı yıllara yayılan veya çok büyük bir sistem hayal edebilir.

AIOS:
- vizyonu korumalı,
- onu yapay biçimde küçültmemeli,
- gerçekçilik konusunda dürüst olmalı,
- fakat uygulanabilirliği artırmak için işi küçük adımlara bölebilmelidir.

İstenen model:

**uzun vadeli vizyon + kısa vadeli uygulanabilir dilimler**

AIOS "küçük ilk sürüm" ile "küçük vizyon"u karıştırmamalıdır.

Örneğin kullanıcı üç yıllık bir PDF uygulaması vizyonu düşünüyorsa:
- bütün vizyon korunabilir,
- ilk birkaç özellik erken kullanılabilir,
- sonraki özellikler zaman içinde eklenebilir.

## 7. Planlama

Kullanıcı daha önce çok büyük ve ayrıntılı AI planları üretmiştir.

Bazıları:
- kendi içinde çelişmiş,
- gerçek sistemle uyuşmamış,
- uzun konuşmalar sonunda bağlam kaybetmiş,
- uygulanabilirliği düşük çıkmış,
- kullanıcıyı projenin ilerleyişinden koparmıştır.

Bu yüzden AIOS'un planlama yaklaşımı:
- uzun vadeli resmi korumalı,
- yakın aşamayı ayrıntılı hale getirmeli,
- planı gerçek sistemle sürekli karşılaştırmalı,
- çelişkileri tespit etmeli,
- uygulamaya geçmeyi geciktirmemeli.

"Her şeyi baştan ayrıntılı planla" yaklaşımı zorunlu kabul edilmemelidir.

Plan yaşayan bir artefact olmalıdır.

AIOS planın gerektiğinde değişebileceğini kabul etmeli, fakat değişikliklerin neden olduğunu görünür kılmalıdır.

## 8. Conversation ve context yönetimi

Uzun sohbetler kullanıcının karşılaştığı temel sorunlardan biridir.

AIOS:
- conversation çok uzadığında bunu fark edebilmeli,
- yeni sohbet açmanın daha iyi olduğunu önerebilmeli,
- yeni sohbete geçişte kritik bilgiyi kaybetmemeli,
- gereksiz eski konuşma context'ini taşımamalı,
- project state'i kalıcı biçimde taşıyabilmeli.

Kullanıcı aynı konuyu tekrar tekrar anlatmak istememektedir.

Handoff mekanizması:
- kompakt,
- eksiksiz,
- doğrulanabilir,
- gerekli bağlamı koruyan

bir yapıda olmalıdır.

Tam konuşma geçmişini sonsuza kadar taşımak zorunlu değildir.

## 9. Kalıcı hafıza ve project state

AIOS uzun projelerde kalıcı state gerektirir.

Ancak:
- memory,
- state,
- decisions,
- research,
- user profile,
- conversation handoff,
- history

gibi bilgi türlerinin tam olarak nasıl ayrılacağı henüz karar verilmiş değildir.

Obsidian olası bir kullanıcı-facing knowledge layer olarak düşünülebilir.

Ancak:
- Obsidian zorunlu değildir,
- plain Markdown + Git de adaydır,
- Claude Project Knowledge, CLAUDE.md, MEMORY.md, Skills, MCP vb. farklı katmanlar olabilir.

Doğru bilgi mimarisi araştırılmalıdır.

Temel gereksinim:

> Uzun projelerde gerekli bağlamın güvenilir biçimde korunması.

## 10. Research ve karar verme

AIOS yalnızca çözüm üretmemeli, bir problemin nasıl araştırılması gerektiğine de karar verebilmelidir.

Her problem aynı şekilde çözülmeyebilir.

Uygun yöntem:
- web research,
- official documentation research,
- literature research,
- prototype,
- spike,
- benchmark,
- independent review,
- cross-model review,
- direct experimentation

veya bunların kombinasyonu olabilir.

Amaç:
- gereksiz araştırmayı azaltmak,
- erken kapanmayı önlemek,
- önemli alternatifleri kaçırmamak,
- yanlış kararları erken yakalamak.

Örneğin bir Python kütüphanesi seçerken AIOS:
- mevcut seçenekleri araştırmalı,
- gerekirse benchmark veya küçük prototype yapmalı,
- trade-off'ları değerlendirmelidir.

## 11. Erken kapanmayı önleme

AIOS'un ilk makul çözümü otomatik olarak "en iyi çözüm" kabul etmesi istenmez.

Özellikle yüksek etkili kararlarda:
- alternatifler,
- varsayımlar,
- karşı kanıt,
- riskler,
- geri dönüş maliyeti

değerlendirilmelidir.

Kullanıcının getirdiği çözüm önerileri de otomatik olarak doğru kabul edilmemelidir.

AIOS gerektiğinde:
- kullanıcı fikrini eleştirmeli,
- kendi ilk önerisini de eleştirmeli,
- daha iyi bir alternatif varsa ortaya koymalıdır.

Ancak sürekli alternatif üreterek hiçbir zaman karar vermeyen bir sistem de istenmez.

## 12. Self-review ve bağımsız review

AIOS kendi işini denetleyebilmelidir.

Ancak aynı modelin kendi çıktısını tekrar değerlendirmesi tek başına yeterli sayılmamalıdır.

Gerektiğinde:
- self-review,
- devil's advocate,
- temiz context'te bağımsız reviewer,
- farklı modelden ikinci görüş,
- executable verification

kullanılabilir.

Gerçekten çalışıp çalışmadığını mümkün olan yerlerde:
- test,
- grep,
- build,
- execution,
- benchmark

ile doğrulamak tercih edilir.

## 13. Kanıt bütünlüğü

AIOS'un kalıcı state'inde bilgi kaynağının güvenilirliği ayrıştırılmalıdır.

Örneğin:
- `[gözlendi]` — gerçekten görüldü / çalıştırıldı,
- `[üretildi]` — AI tarafından üretildi ama doğrulanmadı,
- `[varsayıldı]` — varsayım.

Doğrulanmamış üretim, doğrulanmış gerçek gibi kullanılmamalıdır.

Özellikle yüksek etkili kararlarda kanıt kökeni korunmalıdır.

## 14. Proje kararları

Kararların yalnızca kaydedilmesi yeterli değildir.

Gerektiğinde karar:
- neden verildi,
- hangi alternatifler değerlendirildi,
- hangi kanıta dayandı,
- geri alma maliyeti,
- ne zaman yeniden değerlendirilmesi gerektiği

ile birlikte izlenebilmelidir.

Ancak karar kayıtlarının tam dosya yapısı veya formatı henüz sabitlenmemiştir.

## 15. AIOS'un diğer AI modellerini kullanması

Claude ana çalışma ortağı olabilir, ancak AIOS tek bir modele bağımlı olmak zorunda değildir.

Adaylar:
- Claude,
- Claude Code,
- Gemini,
- Gemini CLI,
- NVIDIA hosted APIs / NIM,
- ileride başka modeller,
- gerekirse local modeller.

Fakat multi-model kullanım varsayılan olmamalıdır.

Birden fazla model:
- kritik review,
- independent second opinion,
- model diversity'nin anlamlı olduğu durumlar

gibi koşullarda kullanılabilir.

Her göreve bütün modelleri koşturmak istenmez.

Self-hosted NVIDIA NIM ile hosted NVIDIA API aynı şey değildir ve ayrıca değerlendirilmelidir.

## 16. Subagents / Agent Teams / Skills / MCP

Bu mekanizmaların hepsi AIOS'un potansiyel araçlarıdır.

Ancak hiçbirini peşinen zorunlu çözüm olarak kabul etmiyoruz.

Örneğin:
- Subagent → sınırlı read-only keşif için yararlı olabilir.
- Agent Teams → gerçekten ayrışabilen bağımsız işler için yararlı olabilir.
- Skills → tekrarlı workflows için yararlı olabilir.
- MCP → harici sistemlere erişim gerektiğinde yararlı olabilir.

Hangisinin hangi durumda kullanılacağı AIOS tarafından belirlenebilmelidir.

Tek yazıcı/authoritative-state bütünlüğü korunmalıdır.

## 17. Token, maliyet ve kaynak yönetimi

AIOS'un kaynak tüketimini yönetmesi gerekir.

Kaynak sadece:
- token,
- para,
- süre

değildir.

Aynı zamanda:
- kullanıcının dikkat süresi,
- kullanıcıdan istenen karar sayısı,
- kullanıcının okumak zorunda olduğu bilgi miktarı,
- tekrar anlatma maliyeti

de kaynaktır.

Amaç:

**minimum gereksiz kaynak tüketimi + yeterli kalite**

olmalıdır.

En güçlü model her görevde varsayılan olmamalıdır.

Task'a göre model ve effort seviyesi değişebilir.

## 18. Human attention budget

Kullanıcının dikkat yükü bağımsız bir kalite kriteridir.

AIOS:
- gereksiz soru sormamalı,
- gereksiz rapor üretmemeli,
- gereksiz kararları kullanıcıya taşımamalı,
- önemli olanı görünür tutmalı.

Çok iyi teknik sonuç verip kullanıcıyı inceleme yükü altında bırakan bir sistem başarılı sayılmamalıdır.

## 19. User-controlled but AI-driven

Kullanıcı önemli kararların dışında kalmamalıdır.

Ama AIOS'un teknik işlerin büyük bölümünü kullanıcının üzerinden alması istenir.

İstenen denge:

**AI-driven execution + human ownership**

> AI işi mümkün olduğunca üstlenir; kullanıcı projenin sahibi olmaya devam eder.

## 20. Self-improvement

AIOS zaman içinde:
- yaptığı hataları,
- işe yaramayan yaklaşımları,
- hangi araçların gerçekten değer kattığını,
- hangi modellerin hangi görevlerde iyi çalıştığını,
- hangi prosedürlerin kullanıcıya gereksiz yük bindirdiğini

öğrenebilmelidir.

Ancak sistemin kendi kendini sınırsız biçimde değiştirmesi istenmez.

Değişiklikler:
- gözlenebilir,
- izlenebilir,
- gerektiğinde geri alınabilir

olmalıdır.

AIOS kendi metodolojisini de zaman zaman değerlendirebilir, ancak sürekli kendi çalışma yöntemini optimize edip gerçek işe geçemeyeceği meta-döngülere girmemelidir.

## 21. GUI / visual interface

Uzun vadede AIOS'un yalnızca terminal/chat tabanlı olması istenmiyor.

Görsel bir arayüzde örneğin:
- aktif projeler,
- proje state'i,
- kararlar,
- açık sorular,
- AI activity,
- kaynak kullanımı,
- intervention points,
- riskler,
- progress

görülebilir olmalı.

GUI'nin kesin tasarımı henüz belirlenmemiştir.

## 22. AIOS ve projeler arasındaki ilişki

Uzun vadede AIOS'un projelerden bağımsız bir sistem katmanı olarak yaşaması daha doğal görünmektedir.

Örneğin:

`C:\Users\Atakul\Documents\Projects\`

- `AIOS/`
- `knowledge-base/`
- `future-project/`

gibi.

AIOS bir proje olabilir ve kendi STATE / decisions / Git history'sine sahip olabilir.

Aynı zamanda AIOS'un konvansiyonları diğer projelere uygulanabilir.

Ancak:
- global `CLAUDE.md`,
- Skills,
- templates,
- MCP,
- başka paylaşım mekanizmaları

arasından hangisinin kullanılacağı henüz kesin değildir.

Önemli requirement:

> AIOS'un kendi state'i yönetilen projelerin detaylarıyla kirlenmemeli.

## 23. Pilotların amacı

Bir pilot veya küçük proje seçildiğinde amaç o projenin kendisini mükemmelleştirmek değildir.

Pilotun temel amacı:

> **AIOS'un gerçek bir iş üzerinde nasıl davrandığı hakkında kanıt üretmek.**

Pilotun kendi çıktısı gerçek ve doğrulanabilir olmalıdır; ancak pilotun değeri esas olarak AIOS hakkında öğrenme üretmesidir.

Pilot:
- AIOS'un continuity'sini,
- decision visibility'sini,
- planlama davranışını,
- execution handoff'unu,
- user attention cost'unu,
- context management'ını

test etmek için kullanılabilir.

Pilot, AIOS'un yerine geçmemelidir.

## 24. Kalite standardı

AIOS:
- ilk uygulanabilir çözümle yetinmemeli,
- fakat sonsuz alternatif üretmemeli.
- büyük vizyonu korumalı,
- ama uygulanamaz planlar üretmemeli.
- teknik ayrıntıyı kullanıcıdan almalı,
- ama önemli kararları gizlememeli.
- otonom olmalı,
- ama kullanıcıyı projeden koparmamalı.
- uzun süreli bağlamı korumalı,
- ama her şeyi sonsuza kadar context'e taşımamalı.

Bu denge sistemin temel kalite ölçütlerinden biridir.

## 25. Şu anda kesin kabul edilmemesi gerekenler

Aşağıdakiler fikir, hipotez veya aday mekanizmalardır; gerektiğinde reddedilebilir:

- Obsidian
- Claude Project Knowledge'ın rolü
- global `CLAUDE.md`
- `MEMORY.md`
- `DECISIONS.md`
- belirli bir memory schema
- Subagents
- Agent Teams
- MCP
- Gemini
- NVIDIA hosted API
- belirli model routing kuralları
- GUI mimarisi
- belirli klasör/topoloji mekanizmaları
- belirli prompt şablonları

Bunların doğru olup olmadığını AIOS araştırmalı ve gerektiğinde değiştirmelidir.

## 26. Temel başarısızlık modları

AIOS'un özellikle şu sorunlara karşı dayanıklı olması istenmektedir:

- premature closure
- gereksiz kapsam küçültme
- aşırı planlama
- planın gerçeklikten kopması
- belgelerin çürümesi
- kararların görünmezleşmesi
- çelişkili state
- context kaybı
- conversation drift
- gereksiz token tüketimi
- gereksiz agent kullanımı
- kullanıcı attention overload
- AI'ın kullanıcıdan habersiz önemli kararlar alması
- AI'ın kendi hatasını doğrulayamaması
- AI'ın ürettiği bilgiyi gerçek olarak kaydetmesi
- eski kararların yeni gerçeklikle çelişmesi
- projenin tamamlanmadan sonsuz iyileştirmeye dönüşmesi
- AIOS'un kendi metodolojisini sürekli yeniden tasarlaması

## 27. Önceki başarısız projelerden öğrenilecekler

Önceki projelerde:
- çok uzun implementation planları,
- çok sayıda revision,
- karar ve belirsizlik kütükleri,
- execution protokolleri

olmasına rağmen gerçek kullanımda sorunlar yaşandı.

Özellikle:
- planın büyümesi,
- context'in kaybolması,
- bazı belgelerin birbirleriyle çelişmesi,
- AI'ın yaptığı değişikliklerin gerçek uygulamaya yansımaması,
- sentetik içeriğin gerçek kanıt gibi görülmesi,
- kullanıcı tarafından projenin takip edilememesi

tekrar edilmemelidir.

Eski belgeler yeni sistem için bağlayıcı değildir; failure-case ve öğrenme kaynağıdır.

## 28. AIOS'un başarısı

AIOS'un başarısı yalnızca özellik sayısıyla ölçülmemelidir.

Asıl soru:

> **AIOS kullanırken kullanıcı gerçekten daha büyük, daha uzun ve daha karmaşık projeleri güvenilir biçimde bitirebiliyor mu?**

Başarı göstergeleri zaman içinde:
- gerçek proje çıktıları,
- context continuity,
- decision visibility,
- user control,
- execution reliability,
- attention cost,
- resource efficiency

üzerinden ölçülmelidir.

## 29. Bu belgenin kullanım kuralı

Bu belgeyi okuyan AI:

1. Buradaki her şeyi nihai mimari olarak kabul etmemelidir.
2. Gereksinimleri çözüm önerilerinden ayırmalıdır.
3. Çelişkileri tespit etmelidir.
4. Daha iyi bir fikir bulursa önerebilmelidir.
5. Gerektiğinde kullanıcıya soru sormalıdır.
6. Büyük resimde eksik bir gereksinim görürse belirtmelidir.
7. Gereksiz meta-planlama döngülerine girmemelidir.

Bu belge bir **north-star / requirement source** olarak düşünülmelidir.

Nihai architecture, technology choices ve implementation strategy ayrıca araştırılacaktır.
