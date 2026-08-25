# BECERİ: yeni-proje

| | |
|---|---|
| **Amaç** | Yönetilen proje açılış ritüelini tek akışta: iskelet + kapı kapsamı + beyin kaydı (F8/F9.5) |
| **Yaşam döngüsü** | newproject.py arayüzüne bağlı; araç değişirse güncellenir |
| **Sahip** | Sahip isim+vizyon söyler; Claude iskeletler; vision kısmı SAHİBİNDIR |
| **Tetikleyici** | Sahibin yeni yönetilen proje isteği |

## Adımlar

1. İsim + tek cümlelik amaç al
2. `uv run --no-project python tools/newproject.py <ad>`
3. BRIEF.md dört-alanını sahibin sözlü girdisiyle doldur (vision metnini SEN yazmazsın — onu dikte ettirip yerleştirirsin)
4. `.aios` marker'ın konduğunu doğrula → kapı kapsam filtresi projeyi görmeli
5. AIOS'a kaydet: STATE.md yönetilen-projeler satırı + DECISIONS T-C giriş (`--ilgili` ile F8 pilotuna bağla)
6. Kapı canlı-testi: proje klasöründe rejected bir anahtar içeren dosya denemesi → FIRED beklenir

## Doğrulama

- `git -C Projects/<ad> log --oneline` → ilk commit
- `test -f Projects/<ad>/.aios`
- Kapı FIRED kanıtı (logs/aios.jsonl)

## Kısıtlar

- **F8 pilot fazı 2026-08-25'te kapandı** — yeni yönetilen projesi artık açılabilir; yine de aynı anda ≤1 aktif inşa (eşzamanlılık v1)
- Vision/metin sahibin; Claude doldurulan alanlarda kendi fikrini vizyon olarak yazamaz
