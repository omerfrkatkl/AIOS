# REJECTED — reddedilen öneriler bankası

| | |
|---|---|
| **Amaç** | Daha önce reddedilmiş bir önerinin tekrar sunulmasını engellemek (G32) |
| **Yaşam döngüsü** | **Yalnızca eklenir.** Bir red geçersizleşirse yeni kayıtla iptal edilir, silinmez. |
| **Sahip** | Proje sahibi — **her kayıt insan onayı gerektirir** |
| **Okuma tetikleyicisi** | Stop hook, her yanıt tamamlanmadan önce. Otomatik, Claude'un iş birliğine bağlı değil. |

> **Bu bir veto listesi değildir.** Her kayıt bir *kapsam* ve mümkünse bir *alternatif* taşır.
> Kapsamı dışında aynı fikir meşru olabilir. Kapı asla sessizce bastırmaz — eşleşmeyi gösterir, kararı sahibe bırakır.

**Anahtarlar iki dilli yazılır.** Model bazen İngilizce yanıt verir; tek dilli anahtar kaçırır. `[gözlendi] 2026-08-15`

**Alan sözlüğü (adlar İngilizce, içerik Türkçe):** `keys` eşleştirme ifadeleri (`|` ile ayrılır, iki dilli) · `reason` red gerekçesi · `scope` reddin nerede geçerli olduğu · `strength` firm/partial · `alternative` yerine önerilen yol · `approved` onay tarihi (`YYYY-AA-GG`). **`approved` bir tarih değilse kayıt kapıda etkisizdir.**

---

## R-001 · Yönetilen projeler AIOS'un içinde yaşasın

- **keys:** projeleri aios içinde | aios içinde yaşasın | iç içe topoloji | aios projeleri barındırsın | projects inside aios | nested topology | aios contains projects
- **reason:** Tek git deposunda karışık geçmiş, bağımlılık karışması, AIOS state'inin proje ayrıntılarıyla kirlenmesi. Ayrılma kararı her geleceğe uyumlu ve maliyeti sıfırken, iç içe geçme ayrılmak istendiğinde git ameliyatı gerektirir.
- **scope:** Kalıcı topoloji kararı. Geçici scratch dizinleri bu redde girmez.
- **strength:** firm
- **alternative:** Topoloji C — `Projects/AIOS/` ve `Projects/<proje>/` kardeş dizinler.
- **approved:** 2026-08-15

## R-002 · Knowledge graph tabanlı hafıza katmanı

- **keys:** knowledge graph tabanlı hafıza | zep kullanalım | graphiti | temporal knowledge graph | graph tabanlı memory | knowledge graph memory | graph based memory layer | zep for memory
- **reason:** Konuşma başına 600.000+ token ayak izi ve arka plan işleme yükü; tek kullanıcı için işletilemez ve çürüyecek standing infrastructure.
- **scope:** Kaynak-of-truth veya birincil hafıza katmanı olarak. İleride salt-okuma bir görselleştirme aracı olarak yeniden değerlendirilebilir.
- **strength:** firm
- **alternative:** Markdown + git kaynak-of-truth; SQLite indeks katmanı.
- **approved:** 2026-08-15

## R-003 · Self-hosted NVIDIA NIM

- **keys:** self-hosted nim | nim container kur | nvidia nim kendi sunucumuzda | kendi gpu üzerinde nim | self hosted nvidia nim | run nim locally | host nim ourselves
- **reason:** GPU donanımı ve üretim için AI Enterprise lisansı gerektiriyor; tek kişilik kişisel sistem için gerekçesiz maliyet ve karmaşıklık.
- **scope:** Yalnızca **self-hosted** dağıtım. Hosted NVIDIA API (build.nvidia.com) bu redde **girmez** — seyrek ikinci-görüş çağrıları için hâlâ test adayıdır.
- **strength:** firm
- **alternative:** Hosted API, dar kapsamlı ikinci görüş için.
- **approved:** 2026-08-15

## R-004 · BMAD-METHOD benimsenmesi

- **keys:** bmad method | bmad benimseyelim | 12 ajanlı yaşam döngüsü çerçevesi | adopt bmad | bmad framework
- **reason:** 12+ ajan, yüksek token maliyeti ve öğrenme eğrisi; başarı ölçütünün "sistem işi yavaşlatmamalı" maddesini doğrudan tehdit ediyor ve tek-yazıcı ilkesiyle çelişiyor.
- **scope:** Bütün olarak benimseme. Tekil fikirlerinin (ör. dosya-tabanlı devir) ödünç alınması bu redde girmez.
- **strength:** firm
- **alternative:** Claude Code plan mode + kendi protokolümüz.
- **approved:** 2026-08-15

## R-005 · Agent Teams'in şu aşamada kullanılması

- **keys:** agent teams kullanalım | agent team kuralım | paralel ajan takımı | use agent teams | parallel agent team | spawn agent team
- **reason:** Önizleme aşamasında, paylaşılan durum gerektiren tasarım işinde kırılgan, daha yüksek token maliyeti. Tek-yazıcı ilkesiyle çakışıyor.
- **scope:** **Ertelendi, kalıcı değil.** İlk dikey dilim teslim edildikten sonra, ≥3 gerçekten ayrık artefakt ve tanımlı kabul testi varsa yeniden değerlendirilir.
- **strength:** partial
- **alternative:** Read-only subagent (keşif) + bağımsız temiz-bağlam inceleyici.
- **approved:** 2026-08-15
