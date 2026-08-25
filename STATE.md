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

- Restukturizasyon: **F0–F7 v1 bitti; F8 pilot başladı (yük = ledger).** Tek yetkili harita `PLAN.md` §8. Süreklilik tatbikatı: 11 saniye (F5 kapanışı, `ms/f5-tamam`).
- **Çalışan zorlama:** kapı LEDGER'ı tarar (6 aktif rejected; test 11/11 · 0/12) — Claude Code tam blok, opencode tespit+log. **Kapsam:** AIOS dizini + `.aios` işaretli yönetilen projeler (ledger opt-in edildi); DC / Documents/All sessiz atlanır (sahibin paralel işleri korumada).
- **Çalışan araçlar:** gate · review · decide · ledger · why · summary · context_cost · aioslog · bundle · backup · milestone · audit · newproject (ritüel). aioslog UTC; logs/ yerel.
- **F6/F6b:** S-1 + zinciri cevaplandı → PROFILE işlendi; interview Tur 1 tamam (kapsam ~%40); **kapanış kanıtı sonraki oturumda** (S-1 zinciri tekrar sorulmaz + audit temiz).
- **F7 v1:** `vault/` (AIOS/vault, gitignored, backup kapsamında) + iki-vault disiplini (Documents/All salt-okunur). Açık soru: öğrenmeler vault'a yansısın mı (sahip kararı).
- **Tetikleyici:** 2026-09-28 — yeni dönem planı → ritim güncellenir.
- **Pilot eşikleri (veri öncesi kilitli):** P1 çalışan CLI ≤4 oturum VEYA 6 hafta (katı fren) · P2 teknik soru = 0, her seçim ≥2 alternatif + gerekçe · P3 DECISIONS 2–8, T-A ≤1 · P4 "sohbetten yavaş değil".

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C (varsayılan T-C) · append-only DECISIONS · dört-alanlı dosyalar · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı (revize):** komutla doğrulanan her şey Claude'da; sahibe yalnız erişilemez ortamlar / kararı-beyanı gerekenler / öznel yargı.
- **Araştırılabilirlik filtresi:** objektif sorular sahibe SORULMAZ — F10 hattına gider.
- **Eşzamanlılık v1:** tek aktif yürütücü; beyne tek yazıcı. **Oturum türleri:** proje/sohbet/araştırma (sohbet → yalnız yapılandırılmış sinyal).

## Durum (F8 eki)

- **Pilot ilk çalışan dilim canlı doğrulandı:** add/expense/income/summary komutları; test 3/3; DB UTF-8 sağlam; negatif tutar tuzağı expense/income komutlarıyla çözüldü. P1 çekirdeği 1. oturumda sağlandı.
- Teknik kararlar ledger deposunda (Topoloji C): SQLite + Typer (web araştırmalı, ≥2 alternatif + gerekçe — DECISIONS ledger/DECISIONS.md).

## Sıradaki

1. **Pilot kullanıma açık:** export komutu canlı (BRIEF #4 tamam, test 4/4) — sahibin gerçek kullanımı P4 algı ölçümünü üretir
2. F6 kapanış kanıtı sonraki oturumda; sonra F9 karar sistemi → F10 → F11 → F12a/b/c/d → F13 → F14 → F15 GUI → F16

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| Pilot teknik kararları yetersiz araştırılmış | P2 ihlali: gerekçesiz/alternatifsiz seçim DECISIONS'ta |
| opencode spawn ETIMEDOUT (bir kez) | tekrarlanırsa timeout 30s→60s veya direkt python yolu |
| Tempo kayması (öğrenci ritmi değişken) | 2 hafta sessizlik → duraklama sinyali |
