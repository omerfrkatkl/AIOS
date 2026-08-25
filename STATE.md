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

- Restukturizasyon: **F0–F8 bitti** — pilot P1/P2/P3 sağladı; **P4 ölçülemedi** (sahibin kullanıcı yüzü yok — dürüst tespit) → görünürlük sonrası ölçülecek. Tek yetkili harita `PLAN.md` §8. Kilometre taşları: `ms/f5-tamam`.
- **Sıradaki faz: F9 · Karar sistemi** — literatür taraması + iki-katmanlı puanlama şeması (evrensel sabitler filtresi + proje ağırlıkları, 0–1) → sahip onayı.
- **Çalışan zorlama:** kapı LEDGER'ı tarar (6 aktif rejected; test 11/11 · 0/12) — Claude Code tam blok, opencode tespit+log. **Kapsam:** AIOS dizini + `.aios` işaretli projeler (ledger opt-in); DC / Documents/All sessiz.
- **Çalışan araçlar:** gate · review · decide · ledger · why · summary · context_cost · aioslog · bundle · backup · milestone · audit · newproject.
- **Kullanıcı görünürlük (yeni — sahibin tespiti):** sistemin sahibin göreceği bir yüzü yoktu; minimal görünürlük = 3 komut (summary/review/context_cost) — sahibine tanıtıldı; tam yüzey F15.
- **Oturum türleri:** proje / sohbet / araştırma (sohbet → yalnız yapılandırılmış sinyal). **Tetikleyici:** 2026-09-28 dönem planı → ritim güncellenir. F6 kapanış kanıtı: sonraki yeni oturumda.

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C (varsayılan T-C) · append-only DECISIONS · dört-alanlı dosyalar · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı (revize):** komutla doğrulanan her şey Claude'da; sahibe yalnız erişilemez ortamlar / kararı-beyanı gerekenler / öznel yargı.
- **Araştırılabilirlik filtresi:** objektif sorular sahibe SORULMAZ — F10 hattına gider.
- **Eşzamanlılık v1:** tek aktif yürütücü; beyne tek yazıcı. **Ledger kullanım modeli:** sahibin arayüzü sohbet; CLI ajanın aracı.

## Sıradaki

1. **F9 · Karar sistemi:** ADR/MCDA literatür taraması → iki-katmanlı puanlama şeması taslağı → **sahip onayı** → decide entegrasyonu
2. Sonra F10 Araştırma motoru (ilk gerçek iş: model-benchmark araştırması) → F11 → F12a/b/c/d → F13 → F14 → F15 GUI → F16

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| P4 ölçümü yine ertelenir | kullanıcı görünürlük tanıtımından sonra da algı oluşmuyorsa |
| opencode spawn ETIMEDOUT (bir kez) | tekrarlanırsa timeout 30s→60s veya direkt python yolu |
| Tempo kayması (öğrenci ritmi değişken) | 2 hafta sessizlik → duraklama sinyali |
