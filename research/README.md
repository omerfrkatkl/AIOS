# research/ — araştırma hattı (F10)

| | |
|---|---|
| **Amaç** | Kanıt-etiketli araştırma raporları ve kaynak kütüğü; karar puanlamasına atıf besler (G14/G15) |
| **Yaşam döngüsü** | R-*.md raporları bir kez yazılır, tarih geçtikçe tazelenir (yeni R-id); cache/ yeniden üretilebilir, git'e girmez |
| **Sahip** | Claude yazar (websearch/araçlarla), sahip rapor kalitesini veto edebilir |
| **Okuma tetikleyicisi** | decide.py puanlaması öncesi (atıf kontrolü) · ilgili karar gündeme geldiğinde |

## Format

Her rapor `R-NNN-kisa-ad.md`:

```
# R-001 · <başlık>
| alan | değer |
| id/tarih/soru/yöntem/kaynak sayısı/provenance rozeti/verdict/beslediği kararlar |
## Plan  (soru → yöntem → kanal önerileri + kota notu + çoklu-getiri)
## Bulgular  (her bulgu kanıt-etiketli: [ölçüldü]/[raporlandı]/[çıkarım] + kaynak no)
## Kaynaklar  (numaralı: başlık — URL — erişim tarihi)
```

Etiketler: `[ölçüldü]` doğrudan benchmark/test verisi · `[raporlandı]` ikincil kaynak iddiası · `[çıkarım]` sentez.
Kural: aynı soruya önce cache/index.jsonl bakılır (G14). Puan yalnız var olan R-id'ye atıfla geçerli (G15).
