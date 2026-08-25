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

- Restukturizasyon: **F0–F10 bitti + F9.5 panosu inşa edildi.** Tek yetkili harita `PLAN.md` (checkbox'lı yürütme haritası — her oturum oradan devam eder). Kilometre taşları: `ms/f5-tamam`.
- **F9 karar sistemi (10/10):** iki-katmanlı puanlama (evrensel sabitler filtresi + proje ağırlıkları 0–1) · decide.py --scores/--sonuc-izle/--ilgili · sentetik test 3/3 (atıfsız puan reddedilir) · tartışma/geri-çağırma/kademeli otonom/sonuç-izleme kuralları CLAUDE.md'de.
- **F10 araştırma hattı (10/10):** sindir.py (digest/badge/lookup) · research/R-001 model-benchmark (6 kaynak: Claude ailesi agentic kodlama lideri ~%96 SWE-v; açık ağırlıklar ~15 puan geride → L-003 redsi destekleniyor) · önbellek lookup-once (Türkçe-fold'lu) · decide.py artık uydurma R-id atfını exit 1 ile reddediyor · tests/test_sindir.py 4/4.
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

1. **Sahibin pano testi** (görsel onay) → F9.5 kapanışı
2. **F6 kapanış kanıtı** (yeni oturumda otomatik)
3. **F11 · Beceri kütüphanesi** — skills/ şeması + ilk beceriler (haftalık-review, yeni-proje, derle-doğrula)
4. F12a (envanter oturumu) → F12b/c/d → F13 → F14 → F15 GUI (P4 gerçek ölçüm) → F16

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| P4 ölçümü yine ertelenir | görünürlük sonrası da algı oluşmuyorsa F15'te zorunlu ölçüm |
| opencode spawn ETIMEDOUT (bir kez) | tekrarlanırsa timeout 30s→60s veya direkt python yolu |
| Tempo kayması (öğrenci ritmi değişken) | 2 hafta sessizlik → duraklama sinyali |
| Sıkıştırma sonrası bağlam kaybı | PLAN + STATE + DECISIONS güncel tutulmalı (bu dosya) |
