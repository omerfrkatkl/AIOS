# skills/ — beceri kütüphanesi (F11)

| | |
|---|---|
| **Amaç** | Tekrar eden, test edilmiş prosedürler isimle çağrılır — her seferinde yeniden türetilmez |
| **Yaşam döngüsü** | Bir prosedür elle 2+ kez yapıldıysa beceriye yazılır (spekülatif beceri yasak); adımlar araçlara atıfla kısa tutulur |
| **Sahip** | Claude yazar/uygular; sahip isimle çağırır veya çıktıyı veto eder |
| **Okuma tetikleyicisi** | Oturum bağlamı bir becerinin tetikleyicisiyle eşleşince indeks buradan açılır |

## Beceri şeması

```markdown
# BECERİ: <ad>
[dört-alan tablosu: amaç · yaşam-döngüsü · sahip · tetikleyici]
## Adımlar        (numaralı, araç-komutlarıyla)
## Doğrulama      (beklenen çıktı + nasıl anlaşılır)
## Kısıtlar       (kapılar/onaylar/asla-yapılmazlar)
```

## Çağrılma kuralı

1. **Sahipten:** "X becerisini uygula" → ilgili dosya okunur, adımlar koşulur.
2. **Otomatik-öneri:** oturum içinde bir becerinin `tetikleyici` koşulu oluşursa AI beceriyi önerir; yan-etkili adımlar (`--done`, proje-açılış) normal kapılardan geçer — beceri dosyası hiçbir kapıyı atlatmaz.
3. **Yeni beceri:** elle 2+ tekrar → kodlama; her beceri yazıldığı gün en az bir kez uçtan-uca doğrulanır.

## İndeks

| Beceri | Tetikleyici | Yan-etki |
|---|---|---|
| `haftalik-review` | son review ≥7 gün veya sahibin isteği | `--done` (sahip okuduktan sonra) |
| `yeni-proje` | sahibin yeni yönetilen proje isteği | klasör+git oluşturma |
| `derle-dogrula` | her somut değişiklik sonrası | yok (salt-okunur denetim) |
| `donemsel-ozet` | SADECE sahibin açık isteği (opt-in) | yok (sohbete rapor) |
