# STATE — AIOS v3

| | |
|---|---|
| **Amaç** | Şu an neyin doğru olduğunu tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde yeniden yazılır; eskiyen satır silinir, asla eklenmez |
| **Sahip** | Proje sahibi; Claude yazar, sahip diff'i onaylar |
| **Okuma tetikleyicisi** | Her oturum açılışı |
| **Tavan** | ~900 kelime |
| **Son güncelleme** | 2026-08-24 |

## Durum

- Restukturizasyon: **F0–F3 bitti, F4 Zorlama v1 bitti** (kapı v3 + adaptörler + araç seti). Tek yetkili harita `PLAN.md` §8.
- **Çalışan zorlama:** kapı LEDGER'ı tarar (6 aktif rejected kayıt; test 11/11 · 0/12) — Claude Code'da tam blok, opencode'da tespit+log (bloke yüzeyi yok, belgeli sınır).
- **Çalışan araçlar:** gate · review · decide · ledger · why · summary · context_cost · aioslog (tek JSONL standardı, logs/ yerel).
- **Sahibin bekleyen canlı testi:** Claude Code restart → herhangi bir oturum kapat → `logs/aios.jsonl`'de FIRED; opencode restart → rejected ifade dene → BLOCKED (surface=opencode).
- Yönetilen projeler dokunulmadı; F8'e kadar yeni yönetilen proje başlatılmaz.

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C (varsayılan T-C) · append-only DECISIONS · dört-alanlı dosyalar · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı (revize):** komutla doğrulanan her şey Claude'da; sahibe yalnız erişilemez ortamlar / kararı-beyanı gerekenler / öznel yargı.
- **Eşzamanlılık kuralı v1:** tek aktif yürütücü; beyne tek yazıcı.

## Sıradaki

1. Sahibin canlı testleri (yukarıda) → sonuçlar DECISIONS'a
2. **F5 · Süreklilik + kartlar** — handoff, yerel-katman yedekleme, oturum sihirbazı, acil durum kartı, kuru koşu

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| opencode plugin'in session.idle olayı beklediği gibi gelmemesi | opencode restart sonrası canary sessizse plugin revize |
| Tempo kayması | 2 hafta sessizlik → duraklama sinyali |
