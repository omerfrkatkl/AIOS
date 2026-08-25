# research/ — araştırma hattı (F10, kriter kitabı v2)

| | |
|---|---|
| **Amaç** | Kanıt-etiketli araştırma raporları; karar puanlamasına makine-denetlenebilir kanıt besler (G14/G15). Sahip araştırmayı kendisi doğrulayamaz → kalite kontrolü bu kurallarla MAKİNADA. |
| **Yaşam döngüsü** | İzleme-soruları raporu yerinde tazelenir (Sürümler bloğu); kararlı-sorular yeni R-id alır. Takip dosyaları append-only varlıklar. |
| **Sahip** | Claude yazar; sahip raporu okur (format/yararlılık yargısı), içerik-doğrulamayı `sindir.py check` yapar. |
| **Okuma tetikleyicisi** | decide.py atıf doğrulaması · ilgili karar gündeme gelince · review/pano tazelik taraması |

## Sabit başlık anahtarları (pano/check bunları parse eder)

Her rapor üstünde tablo: `id` · `tarih` · `tur` (`izleme`|`kararli`) · `tetik` (YYYY-AA-GG tazelik sonucu) · `guven` (`yüksek`|`orta`|`düşük`) · `manşet` (tek cümle) · `kaynaklar` (sayı)

## Kaynak dereceleri — kontrol-listesi tabanlı (öznel değil)

| Derece | Şartlar (hepsi) |
|---|---|
| **T1-nötr** | Resmî benchmark kuruluşu veya bağımsız harness + yayınlanmış metodoloji + sıralanan modellerin satıcısı DEĞİL |
| **T1-kendi-beyanı** | Model-lab'ın kendi modeline dair resmi sayfası: o model için birincil, **karşılaştırma-manşetini tek başına asla desteklemez** |
| **T2** | Harness/gözlem-tarihi/harmanlama yöntemini açıklar + model-lab'a ait değil + rakip ürün satmıyor |
| **T3** | Yukarıdakileri sağlamayan her şey (SEO/reklam-içerik/opak toplama) |

## Manşet kuralı

Manşet-iddiası için: **≥1×T1-nötr VEYA ≥3×T2 mutabakatı**, ve destek kaynaklar **tam-çekim** olmalı.
Özet-arama (excerpt) kaynakları yalnız ikincil noktaları destekler. T3 hiçbir manşeti desteklemez.

## Güven etiketi — mekanik eşik

- **yüksek** = manşet kuralı sağlandı + çözülmemiş çelişki yok + taze
- **orta** = yukarıdakilerden biri eksik
- **düşük** = T3-bağımlı VEYA bayat VEYA açık çelişki
- Bildirilen güven hesaplanandan yüksekse `check` HATA verir.

## Tazelik

Pencere: `izleme` ≤30 gün · `kararli` ≤180 gün. Baz **gözlem-tarihi (`obs`)** — çekim-tarihi değil; obs bilinmiyorsa "obs-bilinmiyor" bayrağıyla çekim tarihi kullanılır. Tetik geçince rapor STALE sayılır (silinmez).

## Negatif-arama protokolü

Her raporda ≥1 karşıt sorgu **manşeti hedefler**; sonuç ya manşeti değiştirir ya kanıtla çürütülür (elde-tepti yok). Sorgu-kütüğüne `counter` etiketli yazılır.

## Kota

≤8 tam-çekim/rapor. Aşım = gerekçe queries.jsonl'e yazılır.

## Yapılandırılmış iddia katmanı

`R-*.claims.jsonl` alanları (≤8): `model` · `metrik` · `deger`(yüzdesel→0-100 normalize) · `obs` · `harness` · `kaynak` · `derece` · `not`
Çelişki = aynı model+metrik, benzer pencerede Δ>3 puan. Model kimliği: `aliases.jsonl` birikimli sözlükten (otomatik çözüm YOKtur — belgelenen sınır).

## Etiket sözlüğü eşlemesi

Araştırma-içi: `[ölçüldü]`=kaynağın ölçümünün aktarımı · `[raporlandı]`=ikincil aktarım · `[çıkarım]`=sentez.
DECISIONS girişleri **her zaman küresel** `[gözlendi]/[üretildi]/[varsayıldı]` kullanır; araştırma-etiketleri onların kaynak-alt-tipidir, yerine geçmez.

## Dil kapsamı

Benchmark/model araştırması İngilizce-birincil; yerel/yasal konularda Türkçe kaynak geçerli.

## Sürüm bloğu formatı

```
## Sürümler
- v2 2026-AA-GG — neden... (eski manşet: "...tek satır...")
```

Geçmiş manşet korunur — eski kararların dayandığı rakam sessizce değiştirilemez.

## Dosya yerleşimi

| Dosya | git? | Neden |
|---|---|---|
| `R-*.md`, `R-*.claims.jsonl`, `aliases.jsonl`, `sources.jsonl`, `queries.jsonl` | **evet** | provansans/birikimli varlık — yeniden üretilemez |
| `cache/snapshot-*` | hayır (gitignored) | hacimli ham metin; sha256 ile sources'a bağlı |
