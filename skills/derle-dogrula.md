# BECERİ: derle-dogrula

| | |
|---|---|
| **Amaç** | "Her somut değişiklik sonrası önceki adımlar doğrulanır" kuralının standart uygulaması (sahibin çalışma kuralı) |
| **Yaşam döngüsü** | Test/envanter listesi araç setiyle büyür; liste burada güncel tutulur |
| **Sahip** | Claude koşar, tablo raporu verir; sahibin erişemediği ortamlar ayrıca ona sorulur |
| **Tetikleyici** | Her somut değişiklik sonrası VEYA sahibin "doğrula" isteği |

## Adımlar

1. `git status --short` (AIOS + aktif alt-projeler) → boş = temiz
2. `uv run --no-project python -m unittest discover -s tests` (AIOS)
3. `uv run --no-project python tests/test_gate.py` → Yakalama ≥%80
4. ledger repo: `Push-Location Projects/ledger; uv run python -m unittest discover -s tests; Pop-Location`
5. `uv run --no-project python tools/review.py | Select-String "REVIEW|LEDGER|GATE|CONTEXT|RESEARCH"`
6. `uv run --no-project python tools/context_cost.py` → hedef ≤446
7. Varsa araştırma raporları için: `tools/sindir.py check R-XXX`
8. Sonuç tablosu: kontrol | komut | sonuç (✓/✗) — başarısız varsa DÜZELTMEDEN rapor verme

## Doğrulama

- Tüm satırlar ✓; herhangi ✗ → kök-neden + düzeltme + yeniden-tarama

## Kısıtlar

- Bu beceri salt-okunur denetimdir; düzeltme gerekiyorsa normal karar akışı işler (hata → düzeltme → tekrar tarama)
- Sahibin erişilemediği ortamlar (tarayıcı-görseli, öznel yargı) tabloya girmez — Sahip Doğrulama Kapısı'na gider
