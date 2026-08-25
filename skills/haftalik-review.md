# BECERİ: haftalik-review

| | |
|---|---|
| **Amaç** | Haftalık görünürlük ritmi: kararlar/kütük/kapı/bağlam sağlığını sahip için tek ekranda toplamak (G6) |
| **Yaşam döngüsü** | Araç sürümlerine bağlı; review.py değişirse bu dosya güncellenir |
| **Sahip** | Claude çalıştırır; sahip özeti OKUR — okumak onay değildir |
| **Tetikleyici** | Son `Gözden geçirildi` ≥7 gün önce VEYA sahibin açık isteği |

## Adımlar

1. `uv run --no-project python tools/review.py`
2. Bekleyen onay varsa: `review.py --full` ile tam metinleri göster; yoksa "temiz" de
3. Sahibe **3-7 satırlık Türkçe özet**: kaç yeni karar · bekleyen var mı · kütük/kapı/bağlam durumu · bayat araştırma var mı
4. Sahip okuduğunu söyledikten SONRA: `uv run --no-project python tools/review.py --done`
5. `uv run --no-project python tools/pano.py` (pano tazeleme)

## Doğrulama

- `--done` sonrası DECISIONS.md'de bugünün `Gözden geçirildi` satırı
- `review.py` yeniden koşulunca "0 new decisions since"
- pano.html zaman damgası güncel

## Kısıtlar

- **Adım 4 asla sahibin okuma onayı olmadan koşulmaz** (görünürlük ≠ onay)
- Bekleyen T-A varsa özette ayrıca vurgulanır; review kaydı bekleyeni kapatmaz
