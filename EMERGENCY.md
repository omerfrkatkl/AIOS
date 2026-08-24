# EMERGENCY — acil durum kartı

| | |
|---|---|
| **Amaç** | Her şey bozulduğunda (kapı öldü, state bozuldu, araçlar çalışmadı) uygulanacak minimum kurtarma akışı |
| **Yaşam döngüsü** | Nadiren değişir; mimari değişince gözden geçirilir |
| **Sahip** | Proje sahibi |
| **Okuma tetikleyicisi** | Yalnızca acil durumda — normal oturumlarda yüklenmez |

## Manuel mod — 10 satır

1. **Sakin ol, hiçbir şey kalıcı kayıp değil:** beyin git'te, kişisel katman `backups/`'ta.
2. **Son sağlıklı noktayı bul:** `git log --oneline -10`
3. **Bozuk dosyayı geri al:** `git checkout HEAD -- <dosya>` (tek dosya) veya `git reset --hard <commit>` (tümü — son kararından eminsen).
4. **Kişisel katmanı geri yükle:** `uv run --no-project python tools/backup.py --restore backups/<en-yeni>.zip`
5. **Kapı öldüyse:** `uv run --no-project python adapters/claude-code/install.py --uninstall` sonra `--dry-run` + kurulum ile yeniden dene.
6. **Araçlar çalışmıyorsa:** `uv run --no-project python tools/review.py --files` — hangi dosya MISSING/bozuk görünüyor?
7. **Minimum kurallar (her koşulda geçerli):** kanıt etiketleri · T-A/B/C mantığı · append-only kayıt · görünürlük ≠ onay.
8. **Karar veremiyorsan:** hiçbir kalıcı işlem yapma; bir sonraki oturuma not bırak (`STATE.md`'ye tek satır).
9. **Toparlanınca:** ne olduğunu `DECISIONS.md`'ye yaz — acil durum da bir karardır.
10. **Önleme:** haftalık `tools/backup.py` + `tools/review.py` bu kartı okumana gerek bırakmamalı.
