# STATE — AIOS v3

| | |
|---|---|
| **Amaç** | Şu an neyin doğru olduğunu tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde yeniden yazılır; eskiyen satır silinir, asla eklenmez |
| **Sahip** | Proje sahibi; Claude yazar, sahip diff'i onaylar |
| **Okuma tetikleyicisi** | Her oturum açılışı |
| **Tavan** | ~900 kelime |
| **Son güncelleme** | 2026-08-23 |

## Durum

- Restukturizasyon sürüyor: **F0–F2 bitti**, **F3 Beyin v1 sürüyor** (TUR 1 inşa edildi, sahibin testi bekliyor). Tek yetkili harita `PLAN.md` §8.
- Sistem şu an yalnızca belgelerden oluşuyor; zorlama makinesi (kapı/review/decide) **F4'te** gelir.
- Yönetilen projeler (KB, ledger, PDF360, DC, DNS) dokunulmadı; F8'e kadar yeni yönetilen proje başlatılmaz.
- Sohbet kanalı: STATE + PLAN raw'dan okunur; PROFILE/LEDGER yereldir (hibrit gizlilik), sohbete gerekirse bundle ile gelir (F5+).

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C (varsayılan T-C) · append-only DECISIONS · dört-alanlı dosyalar · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı:** her elle tutulur değişiklik sahibin testinden geçer; test talimatı komut + beklenen çıktı ile verilir.
- **Eşzamanlılık kuralı v1:** tek aktif yürütücü; paralel iş yürütücünün kontrolünde ve beyne tek yazıcıyla işlenir.

## Sıradaki

1. F3 TUR 1 sahibin testi (beyin dosyaları: 1.1–1.7)
2. F3 TUR 2 (özet üretici + token sayacı) → test 2.1–2.4
3. F3 TUR 3 (mimari karar kaydı + ölçüm ≤446 satır) → test 3.1–3.4 → F3 kapanışı
4. F4 · Zorlama v1 (log standardı + opencode spike'ı ilk adımlar)

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| F4'e dek zorlama yok (sahip onaylı) | kapısız yoğun günlük kullanım başlarsa F4 öne çekilir |
| Tempo kayması | 2 hafta sessizlik → duraklama sinyali, sahip kararır |
