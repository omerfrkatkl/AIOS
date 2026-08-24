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

- Restukturizasyon: **F0–F5 bitti** — süreklilik tatbikatı 11 saniyede geçti (sıfır bağlam, farklı araç, doğru yanıt; eşik ≤15 dk). Kilometre taşı: `ms/f5-tamam`. Tek yetkili harita `PLAN.md` §8.
- **PLAN revizyon 3 (2026-08-24):** platform genişlemesi — Kanal Sözleşmesi (yasa #7), GÖZLEMCİ katmanı, F12a/b/c/d, oturum türleri, iki-katmanlı puanlama, sindir.py, araştırma planı, provenance, öğrenme denetimi, GUI kapsamı. İzlenebilirlik eki: sahibin 58 isteği satır satır (§9). Sıra korundu: çekirdek → pilot → platform zekası.
- **Çalışan zorlama:** kapı LEDGER'ı tarar (6 aktif rejected; test 11/11 · 0/12). **Kapsam filtresi (geçici):** zorlama yalnız AIOS dizininde; F8 ritüeli yönetilen projeleri opt-in ile kapsama alır, o noktada yalnız-AIOS kısıtı kalkar (sahip kararı). Sahibin paralel iş oturumları (Documents/All, Projects/DC) kapsam dışı — sessiz atlanır.
- **Çalışan araçlar:** gate · review · decide · ledger · why · summary · context_cost · aioslog (JSONL, UTC, logs/ yerel).
- **Oturum türleri:** proje / sohbet / araştırma — sohbet varsayılan beyne yazmaz, yalnız yapılandırılmış sinyal akar (tercih/hata/düzeltme/onay/erteleme).
- Yönetilen projeler (KB, ledger, PDF360, DC, DNS) dokunulmadı; F8'e kadar yeni yönetilen proje başlatılmaz.

## Çalışma disiplini

- Kanıt etiketleri · T-A/B/C (varsayılan T-C) · append-only DECISIONS · dört-alanlı dosyalar · tek yetkili plan = PLAN.md.
- **Sahip Doğrulama Kapısı (revize):** komutla doğrulanan her şey Claude'da; sahibe yalnız erişilemez ortamlar / kararı-beyanı gerekenler / öznel yargı.
- **Eşzamanlılık kuralı v1:** tek aktif yürütücü; beyne tek yazıcı.

## Sıradaki

1. **F6 · Tanıma (8 adım):** soru kuyruğu şeması · adaptif döngü (oturum başına ≤1 soru, doğal anda) · tekrar-yasak · cevap→PROFILE (kanıt etiketli) · kişilik üslup kuralı · öğrenme denetimi (backup diff'i) · test: 2 ardışık oturum tekrarsız
2. Sonra F7 Obsidian → F8 Pilot (katı fren) → F9 karar sistemi → F12a/b/c/d → F13 failover → F14 bağlantı → F15 GUI → F16

## Açık riskler

| Risk | Erken sinyal |
|---|---|
| opencode spawn ETIMEDOUT (bir kez görüldü) | tekrarlanırsa timeout 30s→60s veya direkt python yolu |
| Tempo kayması | 2 hafta sessizlik → duraklama sinyali |
