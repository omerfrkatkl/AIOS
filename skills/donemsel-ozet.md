# BECERİ: donemsel-ozet

| | |
|---|---|
| **Amaç** | Sahibin dönem-raporu: ne yapıldı, ne kaldı, riskler — tek sayfa Türkçe (opt-in) |
| **Yaşam döngüsü** | Araç seti değişince güncellenir; çıktı biçimi sahibin geri-beslemesiyle olgunlaşır |
| **Sahip** | SADECE sahibin açık isteğiyle koşar (otomatik değil); çıktı sohbete gelir |
| **Tetikleyici** | Sahibin açık isteği (tipik: dönem bitimi, 28 Eylül plan noktası, "özet çıkar") |

## Adımlar

1. `uv run --no-project python tools/summary.py` → karar özeti (son 14 gün bandı)
2. `uv run --no-project python tools/milestone.py --list` → kilometre taşları
3. `uv run --no-project python tools/review.py` → kütük/kapı/bağlam/araştırma sağlık satırları
4. ledger gerçek kullanım varsa: `Push-Location Projects/ledger; uv run ledger summary; Pop-Location`
5. PLAN.md'den: tamamlanan fazlar / sıradaki ☐ listesi
6. PROFILE kapsam yüzdelerinin güncelliğini not et
7. **Tek sayfa Türkçe rapor** üret: ① dönemde bitti ② sıradaki ③ açık riskler ④ senin katılımın gereken noktalar

## Doğrulama

- Rapor yalnız komutla üretilmiş veriden sentezlenir; her madde araca/rapora dayanır (kanıt-etiketi gerekmez — kaynak zaten araç)

## Kısıtlar

- **Opt-in: otomatik koşmaz, hatırlatma bile yapılmaz** (sahibin dikkat-bütçesi)
- Dosya YAZMAZ — sohbete verir; sahibin isterse md'e dökülür (anti-enflasyon)
