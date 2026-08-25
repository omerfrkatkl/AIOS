# STATE — AIOS v3

| | |
|---|---|
| **Amaç** | Şu an neyin doğru olduğunu tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde yeniden yazılır; eskiyen satır silinir, asla eklenmez |
| **Sahip** | Proje sahibi; Claude yazar, sahip diff'i onaylar |
| **Okuma tetikleyicisi** | Her oturum açılışı |
| **Tavan** | ~900 kelime |
| **Son güncelleme** | 2026-08-25 |

## Durum

- Restukturizasyon: **F0–F11 bitti; F12a yarım (sahip envanteri bekliyor); F9.5/F10-v2 kapandı.** Tek yetkili harita `PLAN.md` (checkbox'lı yürütme haritası — her oturum oradan devam eder). Kilometre taşları: `ms/f5-tamam`.
- **F11 beceri kütüphanesi:** skills/ şeması + indeks + çağrılma kuralı · 4 beceri: haftalik-review, yeni-proje, derle-dogrula (standart doğrulama taraması), donemsel-ozet (opt-in).
- **F12a kayıt defteri v1:** tools/registry.py (init/validate/list/route/update) · Kanal Sözleşmesi kart şeması (G47) · registry/ YEREL katman (gitignored, G10) · 3 kart (claude-code-cli, opencode-cli aktif; ollama-yerel-aday pasif) · route gerekçeli öneri + --gizli yerel-filtresi.
- **R-002 kararlı rapor:** yerel kanal = Ollama birincil aday / LocalAI yedek / LM Studio Layer-1 elendi (kapalı kaynak). Karşıt-bulgu: Ollama tool_choice eksikliği belgeli → devreye-alım önşartı ajan-zinciri tool-testi. check TEMİZ.
- **F9 karar sistemi (10/10):** iki-katmanlı puanlama (evrensel sabitler filtresi + proje ağırlıkları 0–1) · decide.py --scores/--sonuc-izle/--ilgili · sentetik test 3/3 (atıfsız puan reddedilir) · tartışma/geri-çağırma/kademeli otonom/sonuç-izleme kuralları CLAUDE.md'de.
- **F10 araştırma hattı v2 (makine-denetlenebilir):** kriter kitabı `research/README.md` (T1-T3 kontrol-listesi, manşet=tam-çekim+destek, obs-tabanlı tazelik, negatif-arama zorunlu, mekanik güven) · sindir.py check/claim/badge · **R-001 v2** (check TEMİZ exit 0; negatif-arama OpenAI'ın Şubat 2026 SWE-V emeklilik kararını buldu → bağımsız harness'ta açık-ağırlık farkı yalnız 0,6 puan, Verified rakamları şişik; L-003 gerekçesi güncellendi) · decide.py bayat-atıf uyarısı · pano+review araştırma görünür.
- **F9.5 HTML panosu:** pano.py SplitWire-formatı (sidebar + çipler + kartlar, koyu/amber). **Sahibin görsel onayı bekliyor.**
- **F8 pilot:** P1/P2/P3 ✅ · **P4 ⏸ ölçülemedi** (sahibin kullanıcı yüzü yoktu) → görünürlük + gerçek kullanım sonrası. Ledger beklemede (dönem başlayınca doğal kullanım).
- **F6:** kapanış kanıtı sonraki yeni oturumda (S-1 zinciri sorulmaz + audit temiz). **F6b interview:** Tur 1 tamam (kapsam ~%40), Tur 2+ "beni tanı" tetiklemeli.
- **Çalışan zorlama:** kapı 6 aktif rejected tarar (test 11/11 · 0/12) — Claude Code blok, opencode tespit. **Kapsam:** AIOS dizini + `.aios` işaretli projeler; DC/Documents-All sessiz.
- **Çalışan araçlar (15):** gate · review · decide · ledger · why · summary · context_cost · aioslog · bundle · backup · milestone · audit · newproject · pano · sindir.
- **Tetikleyici:** 2026-09-28 dönem planı → ritim güncellenir.

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C · append-only · dört-alan · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı (revize):** komutla doğrulanan her şey Claude'da; sahibe yalnız erişilemez ortamlar / kararı-beyanı gerekenler / öznel yargı.
- **Araştırılabilirlik filtresi:** objektif sorular sahibe SORULMAZ — F10 hattına.
- **Soru disiplini:** kuyruk ≤1/oturum + takip zinciri ≤3/cevap; interview modunda sınırsız (verim kuralı).
- **Eşzamanlılık v1:** tek yürütücü. **Oturum türleri:** proje/sohbet/araştırma. **Ledger modeli:** sahibin arayüzü sohbet, CLI ajanın aracı.

## Sıradaki

1. **F12a kalan adımlar — SAHİP ENVANTER OTURUMU GEREKLİ:** abonelik/kanal/model envanteri (hangi araçlara erişim, limitler, maliyet) → kartlar doldurulur → limit doğrulama araştırmaları → Ollama tool-calling testi (R-002 önşartı)
2. F6 kapanış kanıtı (yeni oturumda otomatik) · interview Tur 2 ("beni tanı") · pilot gerçek kullanım
3. F12b/c/d (keşif/kota/empirik) → F13 failover → F14 bağlantı → F15 GUI (P4 gerçek ölçüm) → F16

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| P4 ölçümü yine ertelenir | görünürlük sonrası da algı oluşmuyorsa F15'te zorunlu ölçüm |
| opencode spawn ETIMEDOUT (bir kez) | tekrarlanırsa timeout 30s→60s veya direkt python yolu |
| Tempo kayması (öğrenci ritmi değişken) | 2 hafta sessizlik → duraklama sinyali |
| Sıkıştırma sonrası bağlam kaybı | PLAN + STATE + DECISIONS güncel tutulmalı (bu dosya) |
