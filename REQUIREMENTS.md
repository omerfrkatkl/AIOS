# AIOS — Gereksinim Kütüğü

| | |
|---|---|
| **Amaç** | Vizyon belgesini çalışılabilir dört listeye ayırmak: gereksinim, tercih, hipotez, açık soru |
| **Yaşam döngüsü** | Yerinde güncellenir. Hipotezler hükme bağlandıkça taşınır. |
| **Sahip** | Proje sahibi |
| **Okuma tetikleyicisi** | Her yeni aşamanın başında + bir kararın hangi gereksinime hizmet ettiği sorgulandığında |
| **Kaynak** | `AIOS_Vision_and_Requirements.md` §1–§29 + oturum eklemeleri |

> Bu kütük mimari değildir. Gereksinimler *ne doğru olmalı*yı söyler, *nasıl* sorusunu değil.

---

## G — Gereksinimler

Her biri yanlışlanabilir olacak şekilde yazıldı. `§` kaynak bölüm.

### Hat ve sahiplik

| # | Gereksinim | § |
|---|---|---|
| **G1** | Fikirden sürdürmeye uzanan hat çalışır: keşif → netleştirme → araştırma → planlama → uygulama → test → sürdürme | 1, 2 |
| **G2** | Teknik ve bilişsel yükün büyük kısmını AIOS taşır; kullanıcı müdahalesi karar noktalarıyla sınırlı kalır | 1, 19 |
| **G3** | Kullanıcı vizyonun ve önemli kararların sahibi olarak kalır | 1, 19 |
| **G4** | **Karar görünürlüğü ≠ karar onayı.** Önemli kararlar görünür olur; her karar onay istemez | 5 |
| **G5** | Karar sınırı işler: yüksek etkili / pahalı geri alınır / yön veya kapsam değiştiren / kullanıcının önemsediği → kullanıcıya. Yerel / ucuz / hızlı fark edilen → AIOS çözer | 5 |
| **G6** | Kalıcı etkili işlemlerde (dosya silme, önemli ayar değişikliği) ayrı bir karar sınırı bulunur | 5 |

### Kullanıcıyı tanıma ve teknik yük

| # | Gereksinim | § |
|---|---|---|
| **G40** | Kullanıcı kısa bir onboarding ile "tanınmış" sayılmaz. Adaptive discovery / interview zaman içinde sürer; tek seferlik form değildir | 3 |
| **G41** | Sorular önceki cevaplara uyarlanır, **tekrar etmez**, gerektiğinde aynı özelliği farklı açılardan doğrular | 3 |
| **G42** | Ölçüt soru **sayısı** değil, sorunun kullanıcı modelini gerçekten geliştirmesidir. Kullanıcı çok sayıda soruya açıktır — verimsiz soruya değil | 3 |
| **G43** | **Teknik implementation kararları kullanıcıya geri itilmez.** AIOS araştırır, alternatifleri değerlendirir, trade-off'ları inceler, kendi önerisini oluşturur; yalnızca gerçekten kullanıcı kararı gerektiren noktaları getirir | 4 |

### Vizyon ve plan

| # | Gereksinim | § |
|---|---|---|
| **G7** | Vizyon yapay olarak küçültülmez. Model: uzun vadeli vizyon + kısa vadeli uygulanabilir dilimler | 6 |
| **G8** | "Küçük ilk sürüm" ile "küçük vizyon" karıştırılmaz | 6 |
| **G9** | Plan yaşayan artefakttır; yakın aşama ayrıntılı, uzak aşama kaba kalır | 7 |
| **G10** | Plan gerçek sistemle sürekli karşılaştırılır; sapma ve çelişki yakalanır | 7 |
| **G11** | Uygulamaya geçiş geciktirilmez | 7 |

### Bağlam ve süreklilik

| # | Gereksinim | § |
|---|---|---|
| **G12** | Konuşma uzadığında AIOS fark eder ve yeni oturum önerir; geçişte kritik bilgi kaybolmaz | 8 |
| **G13** | Handoff kompakt, eksiksiz ve **doğrulanabilir**tir | 8 |
| **G14** | Kullanıcı aynı şeyi tekrar tekrar anlatmak zorunda kalmaz | 8, 9 |
| **G15** | Uzun projelerde gerekli bağlam güvenilir biçimde korunur | 9 |
| **G16** | AIOS'un kendi state'i, yönettiği projelerin ayrıntılarıyla kirlenmez | 22 |

### Araştırma ve karar kalitesi

| # | Gereksinim | § |
|---|---|---|
| **G17** | AIOS bir problemin **nasıl araştırılacağına** da karar verir; yöntem (web, dokümantasyon, literatür, prototip, spike, benchmark, bağımsız review, çapraz model, doğrudan deney) probleme göre seçilir | 10 |
| **G18** | Gereksiz araştırma azalır, erken kapanma önlenir, önemli alternatifler kaçırılmaz, yanlış kararlar erken yakalanır | 10, 11 |
| **G19** | Yüksek etkili kararlarda alternatifler, varsayımlar, karşı kanıt, riskler ve geri dönüş maliyeti değerlendirilir | 11 |
| **G20** | **Kullanıcının önerileri de otomatik doğru kabul edilmez.** AIOS gerektiğinde kullanıcı fikrini ve kendi ilk önerisini eleştirir | 11 |
| **G21** | Sürekli alternatif üretip hiç karar vermeyen sistem de kabul edilmez | 11, 24 |

### Doğrulama ve kanıt

| # | Gereksinim | § |
|---|---|---|
| **G22** | Aynı modelin kendi çıktısını değerlendirmesi tek başına yeterli sayılmaz | 12 |
| **G23** | Mümkün olan her yerde yürütmeyle doğrulama (test, grep, build, execution, benchmark) tercih edilir | 12 |
| **G24** | Kalıcı state'te kanıt kökeni ayrışır: `[gözlendi]` / `[üretildi]` / `[varsayıldı]`. Doğrulanmamış üretim doğrulanmış gerçek gibi kullanılmaz | 13 |
| **G25** | Karar; gerekçe, değerlendirilen alternatifler, dayandığı kanıt, geri alma maliyeti ve yeniden değerlendirme koşulu ile izlenebilir | 14 |

### Kaynak ve dikkat

| # | Gereksinim | § |
|---|---|---|
| **G26** | Multi-model kullanım **varsayılan değildir**; yalnızca kritik review, bağımsız ikinci görüş ve model çeşitliliğinin anlamlı olduğu durumlarda | 15 |
| **G27** | Tek yazıcı / authoritative-state bütünlüğü korunur | 16 |
| **G28** | Kaynak yalnızca token, para ve süre değildir: kullanıcının dikkat süresi, istenen karar sayısı, okuma yükü ve tekrar anlatma maliyeti de kaynaktır | 17 |
| **G29** | En güçlü model her görevde varsayılan değildir; model ve efor seviyesi göreve göre değişir | 17 |
| **G30** | **Dikkat yükü bağımsız kalite kriteridir.** İyi teknik sonuç verip kullanıcıyı inceleme yükü altında bırakan sistem başarılı sayılmaz | 18 |

### Öğrenme ve kendini geliştirme

| # | Gereksinim | § |
|---|---|---|
| **G31** | AIOS zaman içinde şunları öğrenir: yaptığı hatalar, işe yaramayan yaklaşımlar, hangi araçların gerçekten değer kattığı, hangi modellerin hangi görevde iyi çalıştığı, hangi prosedürlerin kullanıcıya gereksiz yük bindirdiği | 20 |
| **G32** | **Daha önce reddedilmiş bir öneri tekrar sunulmaz, ve bu birbirinden bağımsız oturumlar arasında çalışır.** Reddedilme gerekçesi de saklanır | 20 + oturum |
| **G33** | Sistemin kendi kendinde yaptığı değişiklikler gözlenebilir, izlenebilir ve geri alınabilir olur | 20 |
| **G34** | Kendi çalışma yöntemini sürekli optimize edip gerçek işe geçemeyen meta-döngüye girilmez | 20, 26 |

### Arayüz ve teslim

| # | Gereksinim | § |
|---|---|---|
| **G35** | Görsel arayüzde şunlar görülebilir: aktif projeler, proje state'i, kararlar, açık sorular, AI aktivitesi, kaynak kullanımı, müdahale noktaları, riskler, ilerleme | 21 |
| **G36** | **İlk teslim biçimi bir Windows uygulamasıdır.** CLI aracı sonra gelebilir | oturum |

### Ölçüt

| # | Gereksinim | § |
|---|---|---|
| **G37** | Pilotun amacı kendi çıktısını mükemmelleştirmek değil, AIOS hakkında kanıt üretmektir. Pilot AIOS'un yerine geçmez | 23 |
| **G38** | Başarı ölçütü: **kullanıcı daha büyük, daha uzun ve daha karmaşık projeleri gerçekten bitirebiliyor mu** | 28 |
| **G39** | *(Yeni — belgede yoktu)* Kurtarma: bozuk state'ten çıkma yolu, yedekleme ve geri alma bulunur | öneri |

---

## T — Tercihler

Gereksinim değil; ihlal edilirse sistem başarısız sayılmaz ama kullanıcı memnuniyeti düşer.

| # | Tercih | § |
|---|---|---|
| T1 | Tasarımsal konularda (tema, renk, arayüz stili) kullanıcıya seçenek sunulması | 5 |
| T2 | Claude ana çalışma ortağı olabilir | 15 |
| T3 | Windows araçları Scoop ile merkezî yönetilir | oturum |
| T4 | Uzun ömür: tek bir sağlayıcıya kilitlenmeme | oturum |

---

## H — Hipotezler

§25 uyarınca hiçbiri karar değildir. S1/S2 araştırması sonrası hükümler:

| Hipotez | Hüküm | Gerekçe |
|---|---|---|
| Markdown + git kaynak-of-truth | **Benimse** | Model/araç değişimine dayanan tek katman; lock-in'e karşı en güçlü savunma |
| Obsidian | **Benimse — yalnızca görünüm** | Vault zaten markdown klasörü; agent Obsidian'a özgü özelliklere bağlanmaz |
| `STATE` + `DECISIONS` ayrımı | **Koru ve genişlet** | Temel sağlam; eksik olan zorlama katmanı |
| `REJECTED` ayrı dosya | **Benimse** | Farklı okuma tetikleyicisi (öneri-öncesi), `DECISIONS`'a gömülürse ölür |
| Claude Code yerel memory | **Benimse — dar rol** | Kurallar + küçük profil. ~200 satır sınırı negatif bilgi için yetersiz |
| SQLite | **Benimse — sonra** | İndeks/sorgu katmanı, panel adımında |
| Vektör store | **Test — kaynak değil** | Yalnızca eşleştirme indeksi; eşik kırılgan (0.78–0.92, modele bağlı) |
| MCP memory sunucuları | **Test** | Yerel/dosya-tabanlı olanlar uyumlu; bulut olanlar lock-in |
| Knowledge graph (Zep/Graphiti) | **Reddet** | Konuşma başına 600.000+ token ayak izi; tek kişi için işletilemez |
| T-A/T-B/T-C katmanları | **Test sürüyor** | Pratikte işledi, tek dilimlik kanıt |
| Kanıt etiketleri | **Test sürüyor** | Aynı |
| Subagents · Agent Teams · Gemini · hosted NVIDIA API · model routing · GUI mimarisi · prompt şablonları | **Henüz sırada değil** | İlgili aşamada ele alınacak |

## S — Açık sorular

Karar verilmemiş, araştırma veya deney gerektiren konular.

| # | Soru | Bağımlı gereksinimler |
|---|---|---|
| **S1** | **Bilgi mimarisi:** hangi bilgi türleri (memory, state, decisions, research, user profile, handoff, history, hata/red kütüğü) ayrı yapılara dönüşür, nerede yaşar, kim yazar, ne zaman okunur | G14–G16, G24, G25, G31, G32 |
| **S2** | *(kısmen cevaplandı — mekanizma yok, en iyi yaklaşım: deterministik hook gate + hibrit eşleştirme + insan onayı)* **Geri çağırma disiplini:** reddedilmiş fikirlerin, öğrenilmiş hataların ve **daha önce sorulmuş soruların** bağımsız oturumlarda *okunmasını zorlayan* mekanizma nedir; anlam eşleştirmesi nasıl yapılır | G31, G32, G41 |
| **S3** | **Uygulama teknolojisi:** Tauri / Electron / .NET / Avalonia / Python+Qt / başka. *Karar, salt-okunur panel adımında verilecek* | G35, G36 |
| **S4** | **Uygulama ile ajan ilişkisi:** uygulama mı ajanı çağırır, ajan mı uygulamanın durumunu günceller, yoksa ikisi ortak dosya katmanı üzerinden mi buluşur | G35, G36, G27 |
| **S5** | **Karar sınırının teknik uygulaması:** G5'teki ayrım çalışma zamanında nasıl uygulanır | G4, G5, G6 |
| **S6** | **Konvansiyon paylaşımı:** AIOS'un kuralları yönetilen projelere nasıl aktarılır (global CLAUDE.md / Skills / şablon / MCP) | G16 |
| **S7** | **Model yönlendirme:** hangi görev hangi model ve efor seviyesi | G26, G29 |
| **S8** | **Profil yükü:** kullanıcı profilinin ne kadarı her oturumda yüklenir | G28 vs §3 gerilimi |

---

## Çelişkiler ve boşluklar

| Konu | Durum |
|---|---|
| §3 (çok sayıda soru) vs §18 (gereksiz soru sormama) | **Çelişki değil** — §3 kendi ölçütünü veriyor: soru sayısı değil, soru verimi (G42) |
| §3 (zengin kalıcı kullanıcı profili) vs §17 (kaynak tasarrufu) | **Gerçek gerilim.** Profil büyüdükçe her oturumun taban maliyeti artar → S8 |
| §20 (self-improvement) vs §26 (meta-döngü yasağı) | **Çelişki değil** — §20 sınırı kendi içinde çiziyor ("zaman zaman değerlendirebilir"). Sınırın operasyonel tanımı eksik |
| §21 (GUI) vs §9 (markdown+dizin state) | Kullanıcı kararıyla çözüldü: uygulama birincil arayüz. State formatı hâlâ açık → S1 |
| **Boşluk: kurtarma** | Belgede yoktu → G39 olarak eklendi |
| **Boşluk: AIOS'un kendisinin nasıl test edileceği** | §28 başarı göstergeleri veriyor ama test mekanizması yok. Aşama testleriyle karşılanacak |
