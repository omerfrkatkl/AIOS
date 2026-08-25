# R-001 · Model-benchmark araştırması: en güçlü modeller (Ağustos 2026)

| | |
|---|---|
| **id / tarih** | R-001 · 2026-08-25 |
| **soru** | 2026-08 itibarıyla kodlama ve genel görevlerde en güçlü modeller hangileri; açık kaynak seçenekler ne kadar geride? |
| **yöntem** | Çoklu-platform websearch taraması (6 bağımsız takip platformu), çapraz-doğrulama, harness-farkı ayrıştırma |
| **kaynak sayısı** | 6 |
| **provenance** | [kanıt: 6 kaynak · en taze 2026-08-25] |
| **verdict** | Agentic kodlama: Anthropic Claude ailesi lider (Opus 5 / Mythos 5 / Fable 5 — gürültü bandında). Açık ağırlıklar ~15 puan geride (DeepSeek-V4-Pro 80.6). Puanlar arası ≤2 fark = gürültü say. |
| **beslediği kararlar** | Gelecek model-seçim kararları (decide.py atıfları) · L-003 revisit kanıtı |

## Plan

- **Yöntem:** leaderboard çapraz-okuma (tek platforma güvenme — harness varyansı biliniyor [raporlandı])
- **Kanal önerileri:** benchlm.ai · llm-stats.com · datalearner.com · swebench.com resmî · vals.ai (standardize) · arena
- **Kota notu:** tek oturumda ~6 getiri yeterli (G21 kapanış kuralı); derinleşme talebe bağlı
- **Çoklu-getiri:** farklı platformlardan ≥3 bağımsız onay aranır; uyuşmazlık raporda açık yazılır

## Bulgular

### Kodlama (agentic, SWE-bench Verified odak)

- Tüm takip platformları Ağustos 2026'da zirvede **Anthropic Claude ailesini** gösteriyor: Claude Opus 5 %96, Mythos 5 %95.5, Fable 5 %95 `[ölçüldü — K1, K2, K4]`
- Bu üçlü arasındaki ≤1 puanlık fark **harness/tarih varyansı** — anlamlı sıralama değildir `[çıkarım — K2'nin kendi notuyla uyumlu]`
- Standardize bağımsız harness (vals.ai) tablosu çok daha düşük mutlak değerler veriyor: GPT-5.5 standartlaştırılmış %82.6 iken kendi beyan edilen %88.7 satırı karşılaştırılamaz işaretlenmiş `[ölçüldü — K3]` → **mutlak puanlar platformlar ARASI karşılaştırılamaz; aynı platform İÇİ sıralamalar geçerli**
- Nisan 2026 verilerinde zirve %72 idi (Augment Code + Opus 4.6) `[ölçüldü — K5]` → alan 4 ayda ~24 puan hareket etti: **raporların raf ömrü kısa, tazelik zorunlu**

### Genel akıl yürütme (kategori liderleri)

- Hiçbir model her kategoriyi kazanmıyor: GPT-5 AIME'de %100 + Arena Elo 1561 · Claude Mythos Preview GPQA Diamond %94.6 · Gemini 3.1 Pro maliyet-verimlilik lideri ($2/$12) `[ölçüldü — K6]`
- Güvenilir sinyaller 2026'da: GPQA Diamond, SWE-Bench Verified, HLE, Arena Elo; MMLU/HumanEval doymuş — ana sıralama sinyali olarak yok sayılmalı `[raporlandı — K6]`

### Açık ağırlıklar (L-003 ile ilişki)

- En güçlü açık model: DeepSeek-V4-Pro SWE-bench Verified %80.6 `[ölçüldü — K2]`; genel tarafta DeepSeek V3.2 (GPQA 85+, SWE-v 72+) `$0.28/$0.42` fiyatla `[ölçüldü — K6]`
- Frontier kapalı zirveyle açık model arası kodlama farkı: **~15 puan** (96 vs 80.6) `[çıkarım — K1+K2]` → yerel/self-hosted hattın kodlama kalitesinde hâlâ belirgin geride; L-003'ün reddi bu veriyle **destekleniyor** (revisit gerekmez)
- Değer segmenti: Kimi K2 Thinking (bütçe uzun-horizon) `[raporlandı — K5]`, Qwen coder aileleri açık-ağırlık alternatifi `[raporlandı — K5]`

## Kaynaklar

- **K1** BenchLM Coding Report (2026-08-25 erişim) — https://benchlm.ai/coding
- **K2** DataLearner Coding Leaderboard (2026-08-16 güncelleme) — https://www.datalearner.com/en/leaderboards/category/code
- **K3** LLM Reference SWE-bench Verified (vals.ai standardize verileriyle) — https://www.llmreference.com/benchmark/swe-bench-verified
- **K4** llm-stats SWE-Bench Verified Leaderboard (2026-08-25) — https://llm-stats.com/benchmarks/swe-bench-verified
- **K5** Crevio Best LLM for Coding (2026-07-06) — https://crevio.co/blog/best-llm-for-coding
- **K6** ClickRank LLM Leaderboard (2026-05-09) — https://www.clickrank.ai/llm-leaderboard/

## Sınırlar

- Tek oturum taraması; resmî swebench.com ham tablosu doğrudan çekilmedi (sonraki tazelemede)
- Fiyatlar kaynaklarda "yaklaşık" — kesin API fiyatı kullanım öncesi teyit edilmeli
