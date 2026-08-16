# PROFILE — proje sahibi

| | |
|---|---|
| **Amaç** | Sahibin nasıl çalıştığını tutmak; her oturumda yeniden keşfedilmesin |
| **Yaşam döngüsü** | Yerinde güncellenir. Gözlem yanlışlanırsa düzeltilir, silinmez. **Tavan ~400 kelime** — büyürse her oturumun taban maliyeti artar (§3 vs §17 gerilimi) |
| **Sahip** | Proje sahibi. Claude gözlem ekleyebilir, sahip düzeltir. |
| **Okuma tetikleyicisi** | Her oturum başında, `STATE.md` ile birlikte |

> Bu bir form değil. §3 gereği tanıma zamanla sürer; her satır bir gözleme dayanır ve
> yanlışlanabilir. `[gözlendi]` gerçekten görüldü · `[varsayıldı]` çıkarım, doğrulanmadı.

## Çalışma biçimi

- **Kararları toplu onaylar** `[gözlendi]` — beş T-A'yı tek mesajda onayladı. Tek tek onay
  istemek dikkat bütçesini boşa harcar.
- **Komut çalıştırır, belge yazmaz** `[gözlendi]` — açıkça söyledi. Ona metin dikte etme;
  ya dosyayı üret ya komutu üret.
- **Kendi ifadesiyle "basit komut çalıştırabilirim"** `[gözlendi]` — çok adımlı, dallanan
  yönergeler yerine kopyala-yapıştır tek blok ver.
- **Sonucu istenen biçimde raporlar** `[gözlendi]` — biçim verildiğinde uyuyor, verilmediğinde
  eksik alan geliyor. Rapor biçimini her seferinde yaz.

## Beklentileri

- **İtiraz edilmek istiyor** `[gözlendi]` — ilk mesajından beri: "sırf benim söylediğim için
  doğru kabul etme". Cowork, Obsidian ve AIOS'u pilot yapma önerilerinde bu tekrar işe yaradı.
- **Yanlış olduğunda düzeltilmeyi bekliyor, hemen** `[gözlendi]` — hata sahiplenildiğinde
  ilerlemeye devam etti, savunma yapıldığında değil.
- **Yönlendirici çıktı istiyor** `[gözlendi]` — "şunu yap, bunu yap, sonucu şu biçimde getir"
  diye açıkça talep etti.
- **Uzun açıklamadan çok yoğun açıklama** `[varsayıldı]` — uzun turlarda soruları kısaldı.

## Korktukları

- **Aşırı planlayıp inşa edememek** `[gözlendi]` — önceki proje 16 revizyonla battı; bunu ilk
  mesajında sınır olarak koydu.
- **Projenin kontrolünü kaybetmek** `[gözlendi]` — hızdan çok bu. Görünürlük onun için
  onaydan önce gelir.
- **Gereksiz kararla boğulmak** `[gözlendi]` — G43'ü kendisi yazdırdı: teknik kararlar geri
  itilmemeli.

## Ortam ve tercihler

Windows · Scoop ile merkezî araç yönetimi · WSL mevcut ama tercih edilmiyor · Python, git,
Claude Code kurulu · `Documents/Projects/` altında kardeş dizinler · GitHub public depo
(gizlilik bedeli bilerek kabul edildi) · günlük 60+ dk inceleme bütçesi `[gözlendi]`.

Konuşma Türkçe, makineye bakan her şey İngilizce.

## Henüz sorulmamışlar

Bunlar açık uçlar; sorulunca buraya taşınır, **tekrar sorulmaz** (G41).

- Hangi saatlerde/ritimde çalışıyor — günlük mü, hafta sonu yoğun mu?
- Hangi tür kararlarda kendisi karar vermek ister, hangilerinde AIOS karar versin?
- Bu projeden sonra AIOS ile yönetmek istediği başka projeler neler?
- Bir işi "bitmiş" saymak için kişisel ölçütü ne?
- Daha önce hangi araçları deneyip bıraktı, neden?
