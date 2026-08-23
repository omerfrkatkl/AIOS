# STATE — AIOS

| | |
|---|---|
| **Amaç** | Şu an neyin doğru olduğunu tek yerde tutmak |
| **Yaşam döngüsü** | Yerinde yeniden yazılır. Asla eklenmez. Eskiyen satır **silinir**. |
| **Sahip** | Proje sahibi. Claude yerinde güncelleyebilir, sahip diff'i gözden geçirir. |
| **Okuma tetikleyicisi** | Her oturum başında + haftalık gözden geçirmede |
| **Tavan** | ~900 kelime. Aşarsa eklenmez, budanır. |
| **Son güncelleme** | 2026-08-23 |

---

## 1. Başarı ölçütü `[onaylandı 2026-08-15]`

**Ölçüm tarihi: 2026-11-15**

### ÇALIŞIYOR — dördü birden doğruysa
1. Gerçek iş planlama aşamasını geçip **saklanacak bir çıktı** üretti.
2. En az bir kez **3 haftadan uzun ara** verilip **15 dakika içinde** devam edilebildi.
3. **Hiçbir önemli karar sonradan sürpriz olarak** öğrenilmedi.
4. Sistemi kullanmak, aynı işi doğrudan sohbetle yapmaktan **yavaş değildi**.

### ÇALIŞMIYOR — biri bile doğruysa
- Belgeler güncel ama çalışan bir şey yok → **eski proje tekrarlandı**
- `DECISIONS.md`'ye girişler durdu → **terk**
- Protokolü atlamak daha hızlı → **ek yük değeri aştı**

> **Kriter-1 `[karar 2026-08-16]`:** kapı gerçek ve çalışıyor ama **karşılanmış sayılmıyor** —
> günlük bir yetenek "saklanacak çıktı" değildir. Birinci günde kendi ölçütünü geçmiş saymak,
> kaçındığımız kendini-doğrulayan ölçümün ta kendisi olur.

---

## 2. Yol haritası

| # | Aşama | Durum |
|---|---|---|
| 1 | Bilgi mimarisi | ✅ süreklilik testiyle kanıtlandı |
| 2 | Karar sınırı ve görünürlüğü | ✅ `review.py` |
| 3 | Context ve handoff | ✅ G12 · G13 · G14 |
| **4** | **Doğrulama pilotu — knowledge-base döner** | **sürüyor — oturum 1/≤3 bitti** |
| 5–8 | Araştırma · planlama · review · yürütme | sonra |
| 9+ | Self-improvement · salt-okunur panel | sonra |

**Aşama 4'ün amacı AIOS'u ölçmek, PDF'i mükemmelleştirmek değil.** Yük harness'ı sürer;
değerlendirme AIOS'un davranışına bakar, çıktının kalitesine değil. Bu ayrım bir kez kaydı.

**Yanlışlanabilir test `[karar 2026-08-17]`:** O1 tek sayfalık PDF ≤3. oturum VEYA 14 gün
(hangisi önce). O2 oturum 2 açılışında yeniden anlatılan olgu ≤1, ilk üretken komuta ≤15 dk.
O3 dilim boyunca DECISIONS girişi 2–8, açılan T-A ≤1. O4 kapsam dışı BLOCKED ≤1, taban
canary satırı = 10 (2026-08-17). Fren dolarsa aşama uzatılmaz, negatif bulguyla kapanır.

**Oturum 1 (2026-08-17) bitti:** `knowledge-base/output/items.md` typst lehçesine çevrildi
(`$$...$$` ve `\,` kaldırıldı), üç öğe (Theorem 3.2.4, general solution, fundamental set of
solutions) kaynak s. 114 ile birebir karşılaştırılıp değişmeden korundu. Şablon yazılmadı,
derleme yapılmadı — kasıtlı, oturum 2'nin işi.

**Oturum 2 buradan başlar:** typst şablonu yaz, `items.md`'deki üç öğeyi tek sayfada derle,
`typst compile` sıfır dönene kadar doğrula (existence-proof yetmez). L[y] köşeli parantezinin
ve otomatik operatör boşluklamasının derlemede görsel olarak beklendiği gibi çıktığını kontrol
et — bu ikisi `[varsayıldı]` kaldı.

---

## 3. Çalışan yetenekler

**Kapı (G32/G12)** — `REJECTED.md` + Stop hook. Ateşliyor, okuyor, bloke ediyor; modelin
bilmediği bir reddi yakaladığı **gözlendi** (R-002/Zep). Uzun oturum uyarısı: 120k karakter
**ve** oturum boyunca `STATE`/`DECISIONS` yazılmamışsa bir kez. Test 11/11 · 0/12.
Hook komutu 2026-08-23'te `uv run --no-project python`'a bağlandı (bare python kırıktı);
komut satırı kanıtlandı, Claude Code restart sonrası canlı ateşleme `[varsayıldı]`.

**Onarım dedektörü** — `review.py` artık `Projects/CLAUDE.md` işaretçisini de denetliyor
(yokluk/STALE uyarır); işaretçi bir kez sessizce silinmişti `[gözlendi]`. Vizyon uygunluk
görüntüsü `VISION-ANALYSIS.md`'de; her faz planlamasında tazelenir.

**Kaydetme** — `tools/reject.py --add|--approve|--status`. Kayıt `PENDING` doğar ve kapıda
etkisizdir; yalnızca sahip aktive eder. 21 gün kayıt yoksa bayatlama uyarısı.

**Görünürlük** — `tools/review.py`. Onay bekleyenler, katman dağılımı, bozuk `kapatır:`
bağlantıları, `STATE` bayatlığı ve tavanı, banka sağlığı. `--files` parmak izi verir.
Sağlıklıyken sessizdir.

**İş bölümü:** `DECISIONS.md`'yi **Claude Code yazar** — sohbetten kopya gönderilmez, sapma
kaynağıydı. Kod dosyaları sohbette üretilir, parmak izi ile doğrulanır.

---

## 4. Karar tahtası — WIP 0/3

Açık T-A yok, onay bekleyen yok. **T-A/1** (iş birimi = tek yetenek + yanlışlanabilir test) ve
**T-A/2** (AIOS/PROJECT/ENVIRONMENT sınırı) 2026-08-16'da kapandı.

> Bu bölüm bir zamanlar iki ayrı liste içeriyordu ve yeni bir oturum ikisini birleştirip bir
> kararı düşürdü `[gözlendi]`. Benzer görünen iki liste yan yana durmayacak.

---

## 5. Çalışma parametreleri

| Parametre | Değer | Etiket |
|---|---|---|
| Günlük inceleme bütçesi | 60+ dk | `[dikkat]` |
| Açık T-A WIP limiti | 3 | `[dikkat]` |
| Haftalık özet | ≤7 satır | `[dikkat]` |
| STATE tavanı | ~900 kelime | `[dikkat]` |
| Uzun oturum eşiği | 120k karakter | `[hipotez]` |
| REJECTED bayatlama | 21 gün | `[hipotez]` |
| Spike üst sınırı | yarım gün | `[bütçe]` |

**Dil:** makineye bakan her şey İngilizce (kod, CLI, `CLAUDE.md`, alan adları) · konuşma kaydı
Türkçe · red anahtarları iki dilli.

**Katmanlar:** T-A = pahalı geri alınır **veya** geç fark edilir → ≥2 alternatif + onay.
T-B = tersinir → veto penceresi. T-C = yerel → tek satır. **Varsayılan T-C.**

**Kanıt:** `[gözlendi]` · `[üretildi]` · `[varsayıldı]`. `[üretildi]` yükseltilmeden T-A'ya
dayanak olamaz.

---

## 6. Açık riskler

| Risk | Erken sinyal |
|---|---|
| Protokolü hiçbir şey zorlamıyor — tek dedektör DECISIONS akışı | 2 hafta giriş yok |
| REJECTED beslenmezse ölür (NASA LLIS biçimi) | 21 gün kayıt yok |
| Her şeyin T-A'ya kayması | Açık T-A sürekli 3'te |
| **Bayatlık dedektörü yalnızca tarihe bakıyor** | STATE içerik olarak eskiyor ama damga taze — `[gözlendi 2026-08-16]` |
| Elle dosya taşıma sapma üretiyor | `--files` parmak izleri ayrışıyor |
