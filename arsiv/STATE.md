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
| **4** | **Doğrulama pilotu — knowledge-base döner** | **oturum 2/≤3 bitti, O1 karşılandı** |
| **4b** | **İkinci doğrulama yükü — `ledger` (AIOS sürer)** | **açılış bekliyor** |
| 5–8 | Araştırma · planlama · review · yürütme | sonra |
| 9+ | Self-improvement · salt-okunur panel | sonra |

**Aşama 4 AIOS'u ölçer, PDF'i mükemmelleştirmek değil** — değerlendirme davranışa bakar,
çıktı kalitesine değil.

**Yanlışlanabilir test `[karar 2026-08-17]`:** O1 tek sayfalık PDF ≤3. oturum VEYA 14 gün
(hangisi önce). O2 oturum 2 açılışında yeniden anlatılan olgu ≤1, ilk üretken komuta ≤15 dk.
O3 dilim boyunca DECISIONS girişi 2–8, açılan T-A ≤1. O4 kapsam dışı BLOCKED ≤1, taban
canary satırı = 10 (2026-08-17). Fren dolarsa aşama uzatılmaz, negatif bulguyla kapanır.

**Oturum 1 (2026-08-17):** `items.md` typst'e çevrildi; üç öğe kaynakla korundu. Ayrıntı
DECISIONS'ta.

**Oturum 2 (2026-08-23):** Gerçek yol `Projects/KB/` — "knowledge-base" klasör adı değildi.
`main.typ` yazılıp derlendi (KB'nin olgun `template.typ`'i kasıtlı atlandı — DECISIONS'ta).
**O1 karşılandı:** çıkış kodu 0, sayfa sayısı 1 `[gözlendi]`; L[y] parantezi ve operatör
boşluklaması görsel doğrulandı — iki `[varsayıldı]` `[gözlendi]` oldu. Sahip dilimi paralel
kendisi yaptığı için **ikinci yük açıldı: `ledger`** — iş bu kez AIOS tarafından taşınır.

**Oturum 3 (varsa):** O2-O4 açık; aşamayı kapatmak sahibin onayına bırakıldı.

**4b yanlışlanabilir test `[karar 2026-08-23]`:** P1 çalışan, kurulup çalıştırılabilir CLI
≤3 çalışma oturumu VEYA 2026-09-30 (hangisi önce). P2 teknik seçimler (depolama biçimi,
CLI çatısı) sahibeye sorulmadan AIOS tarafından kapatılır; DECISIONS'ta ≥2 alternatif +
gerekçeyle kayıtlı olur. P3 dilim boyunca ledger girişi DECISIONS'ta 2–8 bandında, açılan
T-A ≤1. Fren dolarsa negatif bulguyla kapanır. Açılış yeni oturumda, sıfır bağlamla:
yalnızca `ledger/BRIEF.md` okunur.

---

## 3. Çalışan yetenekler

**Kapı (G32/G12)** — `REJECTED.md` + Stop hook. Ateşliyor, okuyor, bloke ediyor; modelin
bilmediği bir reddi yakaladığı **gözlendi** (R-002/Zep). Test 11/11 · 0/12. Uzun oturum
uyarısı: 120k karakter + dışarı yazılmamışsa bir kez. Hook komutu 2026-08-23'te
`uv run --no-project python`'a bağlandı; canlı oturumlarda ateşlendiği gözlendi (canary,
2026-08-23).

**Onarım dedektörü** — `review.py` `Projects/CLAUDE.md` işaretçisini denetler (bir kez
sessizce silinmişti `[gözlendi]`). Vizyon uyum görüntüsü `VISION-ANALYSIS.md`'de.

**Kaydetme** — `tools/reject.py --add|--approve|--status`. Kayıt `PENDING` doğar ve kapıda
etkisizdir; yalnızca sahip aktive eder. 21 gün kayıt yoksa bayatlama uyarısı.

**Görünürlük** — `tools/review.py`: bekleyen onaylar, katmanlar, DANGLING `kapatır:`,
STATE bayatlığı/tavanı, banka sağlığı; sağlıklıyken sessiz. `--files` parmak izi verir.

**İş bölümü:** `DECISIONS.md`'yi Claude Code yazar — sohbetten kopya gönderilmez.
Kod sohbette üretilir, parmak iziyle doğrulanır.

---

## 4. Karar tahtası — WIP 0/3

Açık T-A yok, onay bekleyen yok. **T-A/1** (iş birimi = tek yetenek + yanlışlanabilir test) ve
**T-A/2** (AIOS/PROJECT/ENVIRONMENT sınırı) 2026-08-16'da kapandı.

> Benzer görünen iki liste yan yana durmaz — bir kez birleştirilip bir karar düşürülmüştü `[gözlendi]`.

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
