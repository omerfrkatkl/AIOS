# R-004 · Ücretsiz API limitleri: OpenRouter · NVIDIA NIM · Gemini (izleme)

| anahtar | değer |
|---|---|
| id | R-004 |
| tarih | 2026-08-25 |
| tur | izleme |
| tetik | 2026-09-24 |
| guven | yüksek |
| manşet | Ücretsiz API katmanları AIOS'un yedek-yönlendirme ihtiyacı için kullanılabilir ama kapasiteleri küçük ve politikaları hızla değişkendir: OpenRouter `:free` resmî belgeyle sabit (20 istek/dk · 50 istek/gün taban · $10 ömür-boyu krediyle kalıcı 1000/gün), NVIDIA NIM hesap-geneli ~40 RPM deneme-limiti (kredi sistemi Eylül 2025'te kaldırıldı, personel teyitli), Gemini ücretsiz katman sayılarını yayınlamıyor ve üçüncül kaynaklar çelişiyor (Aralık 2025 kırpımı belgeli). Ücretsiz katmanlara kişisel/hassas veri gönderilmez. |
| kaynaklar | 12 |

## Plan

Sahibin envanter oturumunda kaydedilen üç ücretsiz API kanalının (openrouter-api, nvidia-nim-api, gemini-api) gerçek kotalarının doğrulanması — F12a'nın son adımı. Sorular: (1) günlük/dakikalık istek sınırları nedir? (2) limitler ne kadar stabil? (3) gizlilik yükümlülüğü var mı? Yöntem: sağlayıcı birincil belgeleri (T1-kendi-beyanı) + bağımsız takip kaynakları (T2 tam-çekim ×3) + karşıt-sorgu. Not: ai.google.dev rate-limits sayfasına iki tam-çekim denemesi timeout oldu — Gemini sayıları bu nedenle yalnız üçüncül kaynaklardan, çelişkiyle birlikte raporlanır.

## Bulgular

### 1. OpenRouter — resmî sabitler (yüksek güven)

`openrouter.ai/docs/api-reference/limits` tam-çekiminde limitler sayfa kaynağında sabit olarak duruyor: `FREE_MODEL_RATE_LIMIT_RPM = 20`, `FREE_MODEL_NO_CREDITS_RPD = 50`, `FREE_MODEL_HAS_CREDITS_RPD = 1000`, `FREE_MODEL_CREDITS_THRESHOLD = 10`. Bağımsız test (lilting.ch) ve topluluk izleme-deposu (cheahjs) aynı rakamları veriyor.

Operasyonel notlar:
- Günlük sınır **ömür-boyu kredi satın-alımına** bakar; tek seferlik $10 kalıcı olarak 1000/gün'e yükseltir [gözlendi].
- **Başarısız denemeler de kotaya sayılır**; negatif bakiye ücretsiz modellerde bile 402 verir.
- İzleme için resmî uç: `GET /api/v1/key` → `usage_daily`, `is_free_tier` alanları — kotu.py'ye entegrasyon için ideal.
- Tarihçe (karşıt-bulgu): Nisan 2025'te günlük taban 200→50 düşürüldü → limitler kalıcı değil, izleme-gerektirir.
- Gizlilik: ücretsiz modellerde prompt/çıktılar barındıran tarafça loglanır (lilting.ch; runapi üçüncül teyidi).
- Bilinen hata: bazı `:free` modellerde tool-calling "No endpoints found that support tool use" ile düşebilir.

### 2. NVIDIA NIM — kredi sistemi kaldırıldı (orta-yüksek güven)

Kartımızdaki "ücretsiz kredi" notu ESKİDİ — düzeltildi:
- Resmî forumda moderator (Eyl 2025): *"We no longer use a credit-based system for build.nvidia.com"* → yerine model-başına değişen, yayınlanmayan rate-limit'ler; üst-sınır UI'da görünüyor.
- NVIDIA personeli (May 2026): 40 RPM *"the published free-tier cap and is not adjustable on a per-account basis."*
- Creeta analizi (Tem 2026): ~40 RPM havuzu **hesap-geneli** — modeller arası paylaşımlı; karışık-model ajanı havuzu iki kat hızlı tüketir.
- Süre-sınırı yok ("trial" zamana değil amaca bağlı); production yasak → NVIDIA AI Enterprise gerekir.
- Technology Access şartları: PHI/PCI/kişisel veri **yasak**; garanti/erişilebilirlik taahhüdü yok; modeller haber vermeksizin free→partner'e kayabilir (kimi-k2-thinking örneği).

### 3. Gemini API — sayılar yayınlanmıyor, kaynaklar çelişiyor (yapısal bulgu orta / rakamlar düşük)

- Resmî docs sayfası iki denemede timeout → birincil doğrulama eksik; Google artık evrensel RPM/TPM/RPD tablosu yayınlamıyor (rapidevelopers gözlemi), kota AI Studio konsolunda proje-başına görünüyor.
- Üçüncül tablolar ÇELİŞİYOR: 2.5 Pro günlük 100 (Ara-2025 tablosu) vs 25 (Haz-2026 gözlemi); Flash 250 vs 500. claims.jsonl'de zaman-etiketli ayrı metrikler olarak kayıtlı.
- Stabil yapısal bulgular: ücretsiz katman model+proje bazlı; **Aralık 2025'te %50-80 kırpıldı** (iki bağımsız kaynak); sıra büyüklüğü: Pro onlarca RPD, Flash yüzlerce, Lite ~1000; TPM ortak ~250K; gün sonu gece yarısı Pasifik.
- Gizlilik: ücretsiz katman verileri Google ürün geliştirmede kullanılabilir.

## Karşıt-bulgu muhasebesi

| Karşıt sorgu | Sonuç | Adres |
|---|---|---|
| OpenRouter limit-değişikliği/şikâyet | Nisan 2025'te 200→50 kırpım belgelendi (aibase + 2024 GitHub "200/day" kalıntısı) | Manşetin "değişken" vurgusunu destekler; mevcut 50/1000 resmî sabitle uyumlu |
| NIM kredi/rate-limit durumu | Eylül 2025 kredi-kaldırma + Mayıs 2026 "40 RPM published cap" personel beyanı | Kartın eski kredi-notu yanlıştı → düzeltildi; iki figür (dashboard-gösterimi vs 40 tabanı) uzlaşır şekilde raporlandı |
| Gemini tutarsız tablolar | Pro RPD 100 vs 25, Flash 250 vs 500 | Rakamlara güven VERİLMEDİ; yalnız yapısal bulgular manşete girdi |

## AIOS etkisi

1. **openrouter-api kartı:** limit notu netleşti (50/gün taban — sahibin kredisi yoksa); `$10` tek-seferlik yatırım 20×kapasite → sahibin T-C kararı.
2. **nvidia-nim-api kartı:** kredi-notu → hesap-geneli ~40 RPM deneme-limiti; hassas-veri yasağı kart işlendi.
3. **gemini-api kartı:** "sayılar yayınlanmıyor, konsoldan bakılmalı" notu.
4. **kotu.py yol haritası:** OpenRouter `GET /api/v1/key` gerçek kota-okuması için birinci sırada; NIM/Gemini için elle sohbet-girdisi devam.
5. **G46/G48 uyumu:** ücretsiz API'lere kişisel veri akmaz (kart enforcement notları zaten kapıyı dışlıyor).

## Sürümler

- v1 · 2026-08-25 · ilk yayın (12 kaynak, 10 iddia, 2 karşıt-sorgu)
