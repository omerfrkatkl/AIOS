# STATE — AIOS v3

| | |
|---|---|
| **Amaç** | Şu an neyin doğru olduğunu tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde yeniden yazılır; eskiyen satır silinir, asla eklenmez |
| **Sahip** | Proje sahibi; Claude yazar, sahip diff'i onaylar |
| **Okuma tetikleyicisi** | Her oturum açılışı |
| **Tavan** | ~900 kelime |
| **Son güncelleme** | 2026-08-25 (2. büyük oturum kapanışı) |

## Durum

- **F0–F12c v1 bitti; F12a'dan yalnız limit-doğrulama kaldı (envanter tamamlandı).** Tek yetkili harita `PLAN.md` (checkbox'lı yürütme haritası). Kilometre taşları: `ms/f5-tamam` · `ms/f12c-v1`.
- **Envanter oturumu (2026-08-25) tamamlandı:** registry'de **12 kanal kartı** — claude-code-cli (limit baskısı yüksek: "çok çabuk bitiyor") · opencode-cli · gemini-abonelik (Google One/Gemini 5TB katman) · 5 ücretsiz web (ChatGPT/Qwen/Grok/DeepSeek/Kimi) · 3 ücretsiz API (OpenRouter :free / NVIDIA NIM bulut / Gemini AI Studio) · ollama-yerel-aday PASIF. Donanım: **16GB RAM + RTX 5060 8GB VRAM** → yalnız 7-8B Q4 çalışır; sahip deneyimi kaliteyi yetersiz buldu (R-002 ile uyumlu). PROFILE'a işlendi.
- **R-004 izleme raporu (check TEMİZ):** ücretsiz API limitleri doğrulandı; NIM kredi-sistemi-kaldırıldı bulgusuyla kart düzeltildi; tetik 2026-09-24 · **$10 OpenRouter sorusu sahibe açık**
- **3 kararlı araştırma raporu (hepsi check TEMİZ):** R-001 model-benchmark (OpenAI Şubat 2026 SWE-V emeklilik bulgusu; açık-ağırlık farkı bağımsız harness'ta 0,6 puan) · R-002 yerel-barındırma (Ollama aday/LocalAI yedek/LM Studio elendi; Ollama tool_choice eksik → devreye-alım önşartı tool-testi) · R-003 GUI-teknoloji (pywebview birincil aday/Flet yedek/Tauri-Electron dil-ekseniyle elendi; kesin karar F15'te T-A).
- **F10 hattı v2:** kriter kitabı research/README.md (T1-T3 kontrol-listesi, manşet=tam-çekim+≥1×T1-nötr/≥3×T2, negatif-arama zorunlu, mekanik güven) · sindir.py check/claim/badge · decide.py bayat-atıf uyarısı.
- **F11 beceriler:** haftalık-review (ilk uçtan-uca koşuldu: 9 karar kaydedildi), yeni-proje, derle-dogrula, donemsel-ozet (opt-in).
- **F12b keşif v1:** kesif.py OpenRouter poller + diff merdiveni (canlı 418 model, idempotent). **F12c kota v1:** kotu.py kullanım defteri + pencere matematiği + DOLU→route-dışları (G46).
- **review.py aynı-gün-karar hatası düzeltildi** (dosya-sırası tabanlı; 9 görünmez karar kurtarıldı).
- **Bekleyen onay:** gorev-kur --kos (günlük kesif-poll'un Task Scheduler kaydı) — sahibin "onayın" bekliyor.
- **F9.5 panosu sahibin görsel onayını aldı** ("tasarım iyi duruyor"). **F8 pilot:** P1-P3 ✅, P4 ⏸ F15 sonrası. **F6:** kapanış kanıtı yeni oturumda. **F6b interview:** Tur 1 ~%40, Tur 2 "beni tanı" tetiklemeli.
- **Çalışan zorlama:** kapı FIRED (test 11/11) · kapsam AIOS+.aios. **Araçlar (18):** gate review decide ledger why summary context_cost aioslog bundle backup milestone audit newproject pano sindir registry kesif kotu. Testler 35/35.
- **Tetikleyici:** 2026-09-28 dönem planı → ritim güncellenir.

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C · append-only · dört-alan · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı:** komutla doğrulanan her şey Claude'da; sahibe erişilemez ortamlar/karar-beyanı/öznel yargı.
- **Araştırılabilirlik filtresi:** objektif sorular sahibe SORULMAZ — F10 hattına.
- **Soru disiplini:** interview modunda gruplar halinde (3-5 bağlantılı); envanter oturumu bu modelle koştu.
- **Eşzamanlılık v1 tek-yürütücü. Ledger modeli:** sahibin arayüzü sohbet, CLI ajanın aracı.

## Sıradaki

1. **R-004 karar-noktası (sahibin, soruldu):** OpenRouter’a tek-seferlik $10 kredi → 50→1000 istek/gün (kalıcı, 20×kapasite)
2. **Ollama devreye-alım önşartı** (R-002): gerçek ajan zincirinde tool-calling testi (yerel kurulum gerekir)
3. kotu.py’ye OpenRouter GET /api/v1/key gerçek-kota okuması (R-004 önerisi)
3. gorev-kur onayı (sahip) · F6 kapanış kanıtı (yeni oturum) · interview Tur 2 ("beni tanı")
5. F12d empirik zeka → F13 failover → F14 bağlantı → F15 GUI (P4 gerçek ölçüm) → F16

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| Claude Pro limit baskısı | "çabuk bitiyor" sıklaşırsa: route alternatiflerine otomatik geçiş (F13 girdisi) |
| P4 ölçümü yine ertelenir | F15'te zorunlu ölçüm |
| opencode spawn ETIMEDOUT (bir kez) | tekrarlanırsa timeout 30s→60s |
| Tempo kayması | 2 hafta sessizlik → duraklama sinyali |
| Sıkıştırma sonrası bağlam kaybı | PLAN+STATE+DECISIONS güncel (bu dosya) — compact güvenli |
