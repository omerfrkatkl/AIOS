# R-001 · Model-benchmark araştırması (Ağustos 2026)

| anahtar | değer |
|---|---|
| id | R-001 |
| tarih | 2026-08-25 |
| tur | izleme |
| tetik | 2026-09-24 |
| guven | yüksek |
| manşet | Anthropic zirvede ama tek değil: bağımsız harness'ta açık-ağırlıklı DeepSeek V4 Pro yalnız 0,60 puan geride (97,0 vs 96,4); SWE-bench Verified mutlak rakamları kontaminasyon nedeniyle şişiktir (OpenAI Şubat 2026'da benchmark'ı emekli etti) — gerçek-yetenek ayrımı SWE-bench Pro'da (~%64 zirve). |
| kaynaklar | 9 |

## Sürümler

- v2 2026-08-25 — negatif-arama OpenAI'ın Şubat 2026 SWE-V emeklilik kararını ortaya çıkardı (%59,4 hatalı test, her frontier modelde kontaminasyon); vals.ai T1-nötr tam-çekim açık-ağırlık farkını ~15 puan DEĞİL 0,6 puan gösterdi; tüm sayısal iddialar yapılandırılmış kayda taşındı; K5/K6 T3'e düşürüldü. (eski manşet: "Agentic kodlama: Anthropic Claude ailesi lider (Opus 5 / Mythos 5 / Fable 5 — gürültü bandında). Açık ağırlıklar ~15 puan geride.")
- v1 2026-08-25 — ilk tarama, 6 özet-kaynak, tek sorgu, negatif-arama yok. **Geriye-dönük öz-durum bildirimi:** tam-çekim yapılmamıştı, çıkar-çatışması denetlenmemişti (K5 reklam-içerikti), arama-stratejisi kayıt altında değildi, mayıs verisi ağustosla aynı havuzda kullanılmıştı.

## Plan

- **Yöntem:** çoklu-platform çapraz-okuma + ≥1×T1-nötr tam-çekim + negatif-arama (kriter kitabı v2)
- **Kanal önerileri:** swebench.com (resmî) · vals.ai (bağımsız harness) · scale.com/leaderboard (Pro) · T2 izleyiciler
- **Kota notu:** 9 getiri / 8 tam-çekim kotasının içinde 2 tam-çekim kullanıldı; kalan özet-mod (manşet desteklemez)
- **Çoklu-getiri:** manşet için ≥3 bağımsız onay şartı sağlandı

## Bulgular

### Manşet bulgular

- Bağımsız bash-only harness (vals.ai, 19/08 güncelleme): **Claude Opus 5 %97,00 lider; DeepSeek V4 Pro %96,40 ikinci** — açık-ağırlık model kapalı liderin 0,60 puan gerisinde; Kimi K3 %93,40 kapalı Opus 4.8'in (%88,60) önünde `[ölçüldü — K7]`
- Aynı sıralamayı T2 izleyicileri doğruluyor: BenchLM Opus 5 %96 zirve `[ölçüldü — K1]`, DataLearner Opus 5 SOTA `[ölçüldü — K2]`, llm-stats Fable 5 %95 `[ölçüldü — K4]` → Anthropic-zirve iddiası 4 bağımsız kanalla ayakta
- **Ancak** DataLearner'ın DeepSeek'i %80,6 göstermesi ile vals.ai'nın %96,4'ü arasındaki ~16 puan, kendi-harness raporları ile bağımsız-harness farkının tipik boyutunu gösteriyor `[çıkarım — K7 vs K2]`

### Benchmark güvenilirliği (negatif-arama bulgusu — v2'nin en önemli düzeltmesi)

- OpenAI Şubat 2026'da SWE-bench Verified'ı değerlendirme standardından çekildi: audit'te **sorunların %59,4'ünde hatalı test** + test edilen HER frontier modelde eğitim-kontaminasyonu kanıtı + doyma (marjinal kazanç ≤%0,1) `[raporlandı — K9 tessl, OpenAI post'unu doğrudan aktarır]`
- Topluluk geçişte: **SWE-bench Pro** (Scale AI SEAL, contamination-resistant 1.865 görev) yeni standart adayı; Nisan tablosunda Claude Opus 4.7 %64,3 lider, GPT-5.4 xHigh %59,1 `[ölçüldü — K8]` → Verified'daki ~%95-97 bandı ile Pro'daki ~%56-64 bandı arasındaki uçurum, şişme boyutunun göstergesi `[çıkarım]`
- Sonuç: **Verified mutlak rakamları pazarlama-sınıfı; platformlar-arası sıralama sinyali olarak yalnız aynı-harness içi karşılaştırmalar geçerli** `[çıkarım]`

### Genel akıl yürütme (ikincil)

- Hiçbir model her kategoriyi kazanmıyor; güvenilir sinyaller GPQA Diamond / HLE / Arena Elo; MMLU-HumanEval doymuş `[raporlandı — K6, T3 kaynak: teyitsiz ikincil bilgi]`

### L-003 ilişkisi (self-hosted hat)

- v1 gerekçesi ("açık modeller ~15 puan geride") **Verified'da geçersizleşti** (vals.ai: 0,6 puan). Ancak (a) Verified rakamları kontaminasyon-şişkin olduğundan gerçek-yetenek paritesini kanıtlamaz, (b) Pro'da açık modellerin konumu henüz bu raporda ölçülmedi, (c) self-hosting pratik maliyetleri (donanım/bakım) bu raporun kapsamı dışı. **L-003 redsi hâlâ geçerli ama gerekçesi güncellenmeli** `[çıkarım]`

## Kaynaklar

- **K1** BenchLM SWE-v leaderboard (T2, özet) — https://benchlm.ai/benchmarks/swe-bench-verified
- **K2** DataLearner coding leaderboard (T2, özet) — https://www.datalearner.com/en/leaderboards/category/code
- **K3** LLM Reference SWE-v / vals.ai aktarımı (T2, v1'den; v2'de K7 ile değiştirildi) — https://www.llmreference.com/benchmark/swe-bench-verified
- **K4** llm-stats SWE-v (T2, özet) — https://llm-stats.com/benchmarks/swe-bench-verified
- **K5** Crevio best-LLM blogu (**T3 — reklam-içerik**, manşet desteğinden çıkarıldı) — https://crevio.co/blog/best-llm-for-coding
- **K6** ClickRank leaderboard rehberi (**T3 — SEO/pazarlama**) — https://www.clickrank.ai/llm-leaderboard/
- **K7** Vals AI SWE-bench Verified (**T1-nötr, TAM-ÇEKİM**, obs 19/08) — https://www.vals.ai/benchmarks/swebench
- **K8** AgentMarketCap Pro-geçiş analizi (T2, özet; SEAL scaffold detaylı) — https://agentmarketcap.ai/blog/2026/04/24/
- **K9** Tessl: OpenAI SWE-V emeklilik analizi (T2, özet; OpenAI post'u doğrudan alıntılar) — https://tessl.io/blog/openai-moves-beyond-swe-bench-verified-as-coding-benchmarks-saturate
- Resmî site: https://www.swebench.com/ (**T1-nötr, TAM-ÇEKİM** — skor tablosu JS-render; sayısal iddia üretemedi, varlık+metodoloji teyidi sağladı)

## Sınırlar (dürüst)

- SWE-bench Pro resmî Scale tablosu tam-çekilmedi (K8 özetiyle yetinildi) → sonraki tazelemede birincil
- Websearch deterministik değil: sorgu-kütüğü yaklaşık reprodüksiyon sağlar
- Takma-ad çözümü elle (aliases.jsonl); otomatik entity-resolution yok
- Tek araştırmacı; ihtilaf halinde mini-G22 protokolü devreye girer (bu raporda gerek kalmadı — çelişki yok)
