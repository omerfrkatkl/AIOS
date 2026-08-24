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

- Restukturizasyon sürüyor: **F0–F2 bitti, F3 Beyin v1 bitti** (açılış 83 satır / 4424 bayt — hedef ≤446 tuttu). Tek yetkili harita `PLAN.md` §8.
- Çalışan araçlar: `tools/summary.py` (aktif-karar özeti) · `tools/context_cost.py` (açılış ölçümü). Zorlama makinesi (kapı/review/decide) **F4'te** gelir.
- Yönetilen projeler (KB, ledger, PDF360, DC, DNS) dokunulmadı; F8'e kadar yeni yönetilen proje başlatılmaz.
- Sohbet kanalı: STATE + PLAN raw'dan okunur; PROFILE/LEDGER yereldir (hibrit gizlilik).

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C (varsayılan T-C) · append-only DECISIONS · dört-alanlı dosyalar · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı:** her elle tutulur değişiklik sahibin testinden geçer; test talimatı komut + beklenen çıktı ile verilir.
- **Eşzamanlılık kuralı v1:** tek aktif yürütücü; paralel iş yürütücünün kontrolünde ve beyne tek yazıcıyla işlenir.

## Sıradaki

1. **F4 · Zorlama v1** — ilk adımlar: log/hata standardı + opencode fizibilite spike'ı (≤ yarım gün)
2. F4'ün sahibe gerçek testi: Claude Code restart sonrası canlı kapı ateşlemesi (canary)
3. Sonra: kapı çekirdeği (taşınan test setiyle TDD) → adaptörler → review/decide/ledger/why

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| F4'e dek zorlama yok (sahip onaylı) | kapısız yoğun günlük kullanım başlarsa F4 öne çekilir |
| Tempo kayması | 2 hafta sessizlik → duraklama sinyali, sahip kararır |
