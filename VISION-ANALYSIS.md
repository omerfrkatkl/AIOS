# VISION-ANALYSIS — vizyon uygunluk anlık görüntüsü

| | |
|---|---|
| **Amaç** | `vision.md` + `REQUIREMENTS.md` karşısında sistemin o anki durumunu tek sayfada göstermek |
| **Yaşam döngüsü** | Yerinde yeniden yazılır; her yol haritası revizyonunda ve faz planlamasında tazelenir. Anlık görüntüdür, hedef belgesi değildir. |
| **Sahip** | Proje sahibi. Claude yazar, sahip farkı gözden geçirir. |
| **Okuma tetikleyicisi** | Faz/yol haritası planlaması + haftalık gözden geçirme |

> Tarih: **2026-08-23** · Kaynaklar: vision.md §1–29, REQUIREMENTS.md G1–G39/S1–S8, DECISIONS (500 satır), doğrudan makine doğrulaması.

---

## 1. Özet hüküm

Çekirdek mimari sağlam ve vizyonla uyumlu: bilgi mimarisi (S1) kapalı, karar disiplini
(T-A/B/C + kanıt etiketleri) fiilen işliyor, süreklilik dosyaları bağlam taşıyor
(gözlendi, 2026-08-16 testi). G32'nin zorlama katmanı uçtan uca kanıtlandı ama bu
taramada **sessizce kırık bulundu ve onarıldı** — kırılganlığın dersi kaydedildi:
*çalışan mekanizma da periyodik ateşleme kanıtı ister.*

## 2. Kanıtlanmış olanlar

| Alan | Kanıt |
|---|---|
| G32 red geri çağırma — eşleştirme + bloke zinciri | R-002 canlı bloke (2026-08-15); modelin bilmediği red yakalandı |
| G32 — kaydetme yolu + insan onayı | reject.py PENDING→onay akışı çalışıyor; 6 aktif kayıt |
| G4/G5/G6 karar katmanları + görünürlük | review.py; WIP 0/3; dangling-kapatır dedektörü |
| G13–G15 süreklilik | Sıfır-bağlam oturum aşamayı/doğru işi çıkardı (2026-08-16) |
| G22–G25 kanıt disiplini | Etiketler DECISIONS'da fiilen kullanılıyor; O1–O4 eşikleri veri öncesi kilitli |
| G27/G28/G30 tek-yazıcı, dikkat parametreleri | STATE §4–5; sahibin onay akışı |
| S1 depolama mimarisi | Markdown+git kararı kapandı; knowledge graph reddi R-002 ile korunuyor |

## 3. Bu taramada kırık bulunan ve onarılan (2026-08-23)

| Bulgu | Onarım | Durum |
|---|---|---|
| `python` komutu WindowsApps stub'ına çözümleniyordu → Stop hook sessiz ölü | hook komutu `uv run --no-project python` yapıldı; kurulum yeniden yapıldı (8 anahtar korundu) | Komut satırı kanıtlandı (canary FIRED). Claude Code restart sonrası canlı doğrulama bekliyor `[varsayıldı]` |
| `Documents/Projects/CLAUDE.md` işaretçisi silinmişti (2026-08-17 düzeltmesi geri dönmüş) | İşaretçi yeniden yazıldı + review.py'ye üç-vakalı dedektör eklendi (test 3/3) | Kapalı |
| Depo bayat: 3 dosya değişmiş, vision.md takipsiz | Bu taramayla commit+push | Kapalı |

## 4. Vizyonda olup henüz olmayanlar

| Gereksinim | Durum |
|---|---|
| G40–G43 adaptif tanıma/interview | Yalnızca pasif PROFILE gözlemleri; soru mekanizması yol haritasında sonraki aşama |
| G17–G21 araştırma & karar kalitesi makineleri | Aşama 5–8, başlanmadı |
| G35/S3/S4 salt-okunur panel | Aşama 9+; teknoloji seçimi (S3) bilinçli ertelendi |
| G39 kurtarma yolu | Gap olarak kayıtlı; Faz 2b'de yanlışlanabilir testle açılacak |
| G2/G19 tam anlamıyla AI-driven execution | Pilot ölçekli; aşama 5–8 konusu |

## 5. Sahibin yön kararı (2026-08-23, bu oturum)

**"Ana araç yok" ilkesi** — araç değişse sistem unutmadan devam etmeli. Sonuçları:

1. Kapının araca-bağlı tetikleyicisi kabul edilen bir sınır olarak kalıyor (adaptör
   deseni, 2026-08-15) — ama her kullanılan araç için adaptör *gereksinim* haline gelir.
   opencode şu an kullanımda → **Faz 2a: opencode kapı adaptörü spike'ı (≤ yarım gün)**.
2. REQUIREMENTS'ta T4 → gereksinim yükseltmesi önerisi (sahip onayına açık).

**"İkinci yük" kararı (2026-08-23):** sahip KB dilimini paralel kendisi yaptığı için
AIOS-un sürdüğü iş kanıtı zayıftı → `Projects/ledger/` açıldı; iş AIOS tarafından taşınır
(G43'ün ilk gerçek sınavı). Yanlışlanabilir test STATE 4b'de: P1–P3, fren 2026-09-30.

## 6. Açık varsayımlar / riskler

| Varsayım | Etiket | Kapanma koşulu |
|---|---|---|
| Yeni hook komutu canlı Claude Code oturumunda ateşleniyor | `[varsayıldı]` | Restart sonrası ilk Stop'ta canary satırı |
| opencode'un plugin/hook yeteneği kapıyı bloke edebiliyor | `[varsayıldı]` | Faz 2a spike çıktısı |
| uv shim'i PATH'te kalıcı | `[gözlendi]` | Haftalık review'da kapı canary recency kontrolü |
