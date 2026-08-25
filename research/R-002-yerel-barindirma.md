# R-002 · Yerel-model barındırma: AIOS yerel kanalı seçimi

| anahtar | değer |
|---|---|
| id | R-002 |
| tarih | 2026-08-25 |
| tur | kararli |
| tetik | 2027-02-21 |
| guven | yüksek |
| manşet | Yerel barındırma üç tamamlayıcı katmandır (motor/DX/UI); AIOS için birincil aday Ollama (MIT · daemon · Docker), yedek LocalAI; LM Studio açık-kaynak evrensel sabitiyle elenir; KARŞIT BULGU: Ollama'nın tool_choice/streaming-tool eksikliği ajan-sürümlü kullanımda belgelenmiş risk → devreye-alım öncesi araç-çağrısı doğrulaması şart. |
| kaynaklar | 6 |

## Plan

- **Yöntem:** çoklu-kaynak çapraz-okuma + ≥3×T2 tam-çekim + zorunlu karşıt-sorgu
- **Kanal önerileri:** glukhov.org (teknik seriler) · tech-insider · gudz.ai · github canlı issue durumu
- **Kota notu:** 3 tam-çekim + 3 özet-paket; kota içinde
- **Çoklu-getiri:** manşet her maddesi için ≥2 bağımsız onay hedeflendi

## Bulgular

### Katman mimarisi (çoklu mutabakat)

- Araçlar rakip değil **tamamlayıcı**: tipik yığın = Ollama (runtime/API) + OpenWebUI (web arayüzü/RAG) + LM Studio (keşif/GUI) `[raporlandı — K1, K3]`
- Üçü de llama.cpp motorunu paylaşır → ham hız farkı yok-es; seçim arayüz/lisans/iş-akışına göre yapılır `[ölçüldü — K1 tablo; K2]`

### Aday değerlendirmesi (AIOS bağlamı: CLI-merkezli · açık-kaynak sabiti · gizlilik bölgesi)

- **Ollama** — MIT ✓ · daemon + OpenAI-uyumlu :11434 + resmî Docker + SDK'lar ✓✓; API olgunluk 5/5-stable AMA araç-çağrısı SINIRLI (`tool_choice` ve streaming-tool yok) `[ölçüldü — K1, K2]`; boşta RAM ~100–200 MB (GUI'lere göre ~5× düşük) `[ölçüldü — K1]`; ~179k GitHub yıldız (canlı repo sayfası) `[ölçüldü — K4]`
- **LocalAI** — tam OpenAI tools-API (parallel invocation dahil) + multimodal + açık kaynak → **ajan-yönlü kullanımda teknik olarak üstün alternatif**; ekosistem daha küçük `[raporlandı — K2]`
- **LM Studio** — kapalı kaynak (freeware, ticari ücretsiz Tem 2025'ten beri) → **evrensel sabit ihlali → LAYER-1 ELEME** (F9 filtresi; puanlamaya gerek kalmadan) `[ölçüldü — K1 lisans satırı; K3 matris]`
- **Jan** — Apache 2.0, denetlenebilir; API beta + araç-çağrısı sınırlı → yedek-audit seçeneği `[raporlandı — K1, K2]`
- **vLLM** — üretim-sınıfı tam tool-calling ama GGUF'suz + tek-kullanıcı masaüstü için aşırı `[raporlandı — K2]`

### Karşıt-bulgu (negatif-arama — manşeti koşullandırdı)

- Ollama eleştirileri: Windows oto-start (kapatma ayarı yok, güncelleme geri açıyor), kurulum şeffafsızlığı, `tool_choice` hâlen yok (issue #17921, v0.32.15, Ağustos 2026'da AÇIK), ROCm/AMD hataları `[raporlandı — K5 counter paketi; K4 canlı issues]`
- "Enshittification erken işaretleri" izleme listesi: paywall/kilit-lenme sinyalleri `[raporlandı — K5]`
- Yanlılık notu: elephas gibi bazı eleştiri-kaynakları rakip ürün satıyor `[raporlandı — K5 notu]`

### AIOS kararı (G11 gerekçeli öneri)

1. **Birincil yerel aday: Ollama** — envanter oturumunda donanım teyidiyle pasif kart aktifleşir
2. **Devreye-alım önşartı:** gerçek ajan zinciriyle tool-calling doğrulama testi (tool_choice eksikliği senaryomuza çarpıp çarpmadığı ölçülecek); başarısızsa **yedek LocalAI** aynı testten geçer
3. **LM Studio elendi** — açık-kaynak sabiti (Layer-1)
4. OpenWebUI: yalnız F15 GUI yüzeyi istenirse değerlendirilir (tek-kullanıcı CLI sahibi için şimdilik gereksiz yük)

## Kaynaklar

- **K1** Tech Insider üçlü karşılaştırma (**T2, TAM**, makale 2026-07-02) — https://tech-insider.org/ollama-vs-lm-studio-vs-jan-2026
- **K2** Glukhov 12+ araç teknik karşılaştırma (**T2, TAM**) — https://www.glukhov.org/llm-hosting/comparisons/hosting-llms-ollama-localai-jan-lmstudio-vllm-comparison/
- **K3** gudz.ai üçlü+OpenWebUI matrisi (**T2, TAM**, affiliate-notlu) — https://gudz.ai/posts/local-ai-llm-tools-2026
- **K4** Ollama GitHub repo/issues canlı (**T1-kendi-beyanı**, erişim 2026-08-25) — https://github.com/ollama/ollama/issues
- **K5** Karşıt-kanıt paketi: glukhov enshittification + dasroot + HN + elephas (T2/T3 karışık, yanlılıklar notlu) — counter sorgusu kayıtlı
- **K6** Destek özetleri: promptquorum (API v1 stable + Anthropic-endpoint) · seodatapulse · ntwk.es (bayat 2025-10) · knolli/aicoolies (T3) — manşet desteğine katılmaz

## Sınırlar (dürüst)

- Sahibin donanımı (RAM/VRAM/GPU) bilinmiyor — model-boyut önerileri verilemedi (envanter oturumu şart)
- LocalAI/Ollama araç-çağrısı kendi zincirimizde test edilmedi — literatür + issue takibi düzeyinde
- Affiliate içerik ekosistemi yoğun; T2'lerde bile çıkar-notları bırakıldı
