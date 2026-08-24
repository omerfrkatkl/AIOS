# DECISIONS — karar geçmişi (v3)

| | |
|---|---|
| **Amaç** | Ne olduğunu ve neden olduğunu kaydetmek |
| **Yaşam döngüsü** | **Yalnızca eklenir.** Hiçbir giriş düzenlenmez veya silinmez. Yanlışsa yeni giriş yazılır. |
| **Sahip** | Proje sahibi (tek yazıcı; Claude yazar, sahip diff'i onaylar) |
| **Okuma tetikleyicisi** | Haftalık kontrol + bir kararın nedeni sorgulandığında |

> **Eski log:** `arsiv/DECISIONS.md` (2026-08-15 → 2026-08-23). Gerekçe ararken doğrudan arşiv taranır (F4'te why.py gelecek).

---

## 2026-08-23 · Sıfırdan yeniden inşa: eski sistem arşive, PLAN.md yürürlükte · T-A · onaylandı

- **Karar:** Aktif kök sıfırlandı; eski belgeler ve araçlar `arsiv/` altına **referans** olarak taşındı. Yeni sistem `PLAN.md`'deki 15 fazlık haritaya göre inşa edilir. Gizlilik mimarisi hibrit: PROFILE/LEDGER/envanter yerel (gitignored + bundle), yapısal dosyalar public.
- **Gerekçe:** Sahibin vizyonu netleşti (kalıcı beyin, çoklu-AI senkronu — önce beyin sonra bağlantı, onay/red/erteleme hafızası, tanıma, kaynak zekası, puanlamalı kararlar, platform kuzey-yıldızı) ve organik büyümüş yapı bunu taşımak yerine temiz temelden kurmayı hak etti. Karar geçmişi korunur: arşiv referans, git geçmişi tam.
- **Alternatifler:** Mevcut yapının üzerine ekleme (elendi: eski varsayımlar yeni tasarımı bağlardı) · yalnızca belge yenileme (elendi: sahip "her şey sıfırdan" dedi) · arşivsiz tam silme (elendi: arşiv bedava sigorta, git geçmişi zaten korur)
- **Geri alma:** `arsivden-geri-don.ps1` tek komut. Hook `install.py --uninstall` ile temiz kaldırıldı (8→7 anahtar, yedek alındı); geri dönüşte arşivden yeniden kurulur.
- **Kanıt:** `[gözlendi]` — kök: PLAN.md, CLAUDE.md, DECISIONS.md, arsivden-geri-don.ps1, arsiv/, .gitignore. **Bazal ölçüm:** 892 satır / 77.447 bayt (CLAUDE+STATE+PROFILE+DECISIONS). Sohbet kanalı (raw STATE/PROFILE) F3/F5'e dek duraklatıldı.

## 2026-08-23 · Vision v2 onaylandi; koke yazildi · T-A · onaylandi

- **Karar:** vision.md v2 koke yazildi - 17 bolum: kisisel AI platformu kimligi, kalici beyin (3-durum hafiza + Obsidian), coklu-AI senkronu (once beyin sonra baglanti; yurutucu-rolu; tartisma protokolu), tanima, kaynak zekasi (envanter+yönlendirici+failover+yetenek saglayicilar), arastirmaya dayali puanlama, yonlendirilmis akis, Windows GUI yuzeyi (opencode tasarim referansi), kaynak disiplini, modulerlik, loglama, acik kaynak, kalite standardi, basarisizlik modlari, arsiv dersleri, basari tanimi.
- **Gerekce:** Sahibin bu oturumdaki tum netlesmeleri tek belgede toplandi; taslak sunuldu, sahip onayladi ("daha cok detay gerekmiyor"). Detayin yeri gereksinimlerdir (F2) - vizyonda mekanizma yoktur, kuzey-yildiz bulaniklasmamali.
- **Alternatifler:** Eski vizyonu yerinde yamamak (elendi: yeni istekler eski yapiya sigmiyordu) · daha uzun taslak (elendi: detay F2'nin isi, vizyon siserse north-star kaybolur)
- **Geri alma:** Ucuz - arsiv/vision.md (v1) + git gecmisi; v2 yerinde revize edilebilir.
- **Kanit:** `[gözlendi]` - sahibin acik onayi 2026-08-23.
