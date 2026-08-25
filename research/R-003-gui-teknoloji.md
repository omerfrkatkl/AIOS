# R-003 · AIOS GUI teknoloji seçimi (F15 ön-hazırlık)

| anahtar | değer |
|---|---|
| id | R-003 |
| tarih | 2026-08-25 |
| tur | kararli |
| tetik | 2027-02-21 |
| guven | yüksek |
| manşet | AIOS GUI birincil adayı **pywebview**: sahibin onaylı pano.html tasarımını WebView2 penceresine sarar, Python-köprüsü mevcut araçları doğrudan çağırır — dil-ekseni filtresinin (Python ekosistemi) doğal sonucu. İkinci aday Flet 1.0 (mobil/çapraz-platform gerekirse). Tauri/Electron elenir: Rust/JS backend ekosistem uyuşmazlığı; tek-kullanıcı yerel araçta boyut kazanımları anlamsız. |
| kaynaklar | 5 |

## Plan

- **Yöntem:** kategori-haritası çapraz-okuma + dil-ekseni filtresi + karşıt-sorgu
- **Kanal önerileri:** tech-insider (benchmark) · youngju (kategori haritası) · startdebugging (Flet) · pywebview repo canlı
- **Kota notu:** 3 tam-çekim + 2 özet-paket; kota içinde
- **Çoklu-getiri:** eleme mantığı ≥2 bağımsız kanalla desteklendi

## Bulgular

### Mimari gerçekler (AIOS bağlamı)

- Mevcut varlık: **pano.html zaten sahibin onayladığı SplitWire-formatında** — GUI işi sıfırdan UI yazmak değil, mevcut HTML'i pencereye sarmak `[gözlendi]`
- Backend tamamen Python (18 araç) → dil-ekseni filtresi: "ekibin dili en güçlü seçici kuvvet" `[raporlandı — K3]; Python ekosistemi → Qt/PySide/webview-sarmalayanlar`
- Windows-tek hedef: "Windows-only'de Electron/Tauri overkill — WinUI/WPF daha doğal; ama mevcut web-varlığı olanlar için webview-sarmalayıcı düşük-riskli yol" `[raporlandı — K3, K1]`

### Aday değerlendirmesi

- **pywebview** — OS-native WebView2 sarmalar (Windows'ta otomatik kurulum), dahili HTTP server + js_api köprüsü, PyInstaller ile ~8–18MB dağıtım `[raporlandı — K4 kendi-beyanı + K6]`; bilinen kusurlar canlı issue'larda: odak-calma (#1822), pythonnet yükleneme (#1817), merkezleme (#1771) — hepsi pencere-yönetimi düzeyi, mimari değil `[ölçüldü — K4]`
- **Flet 1.0** — Flutter-render + Python-mantık; trade-off'ları dürüst belgeli: event-chatter latency, Dart-plugin uyumsuzluğu, split-brain debugging; "güçlü-Python ekibi, iç-araç/dashboards" profiline TAM oturuyor `[ölçüldü — K2]` → ikinci aday (mobil vizyonu belirirse)
- **Tauri 2.x** — teknik olarak üstün boyut/RAM (hello 3.2MB vs Electron 85MB; idle 42 vs 168 MB) `[ölçüldü — K1]` AMA backend Rust: her özel komut Rust yazımı gerektirir; anti-pattern listesinde birebir: "'Tauri çünkü hafif' — Rust-yeteneksiz ekipte başlamak" `[raporlandı — K1, K3]`
- **Electron 43** — JS-backend yine yabancı ekosistem + tek-kullanıcı yerel araçta 85–250MB paket anlamsız `[çıkarım — K1 verisiyle]`
- **PySide6/Qt** — LGPL + widget-paradigması + mevcut HTML tasarımın tamamen atılması → gereksiz maliyet `[raporlandı — K3]`

### Karşıt-bulgu (negatif-arama)

- Flet eleştirisi ciddiye alındı: distributed-app modeli (WebSocket senkronu) basit panolar için gecikme kaynağı olabilir → AIOS'un statik-dominant panosunda düşük risk, etkileşim artarsa yeniden değerlendir `[raporlandı — K2]`
- pywebview içerik-çiftliği kaynakları (johal.in ×2: şüpheli istatistikler) T3'e düşürüldü — manşet desteğine katılmaz `[notlandı — K6]`
- WebView2 olgunluk bağımsız kanıt: Microsoft Teams 2023'te Electron→WebView2 geçiş yaptı (adli-bilişim makalesi 2026-02 analiz ediyor) `[raporlandı — K6]`

### AIOS kararı (G11 gerekçe)

1. **Birincil: pywebview** — pano.html + tools köprüsü; F15'te PoC (pencere + 2 araç-çağrısı) ilk adım
2. **Yedek: Flet 1.0** — yalnız mobil/cross-platform gereksinimi doğarsa
3. **Eleme: Tauri/Electron/PySide6** — dil-ekseni + varlık-yeniden-kullanım maliyeti
4. Kesin framework kararı F15 başında SAHİBİN onayına gelir (T-A: görsel yüzey = geri-dönüşü pahalı)

## Kaynaklar

- **K1** Tech Insider Tauri-vs-Electron (**T2, TAM**, benchmark üçlü-teyitli) — https://tech-insider.org/tauri-vs-electron-2026/
- **K2** Start Debugging: Flet 2026 trade-off'ları (**T2, TAM**) — https://startdebugging.net/2026/01/flet-in-2026...
- **K3** Youngju 11-framework kategori haritası (**T2, TAM**, AI-yardımlı yazarlık beyanlı) — https://www.youngju.dev/blog/culture/2026-05-14...
- **K4** pywebview resmi repo + canlı issues (**T1-kendi-beyanı**, erişim 2026-08-25) — https://github.com/r0x0r/pywebview
- **K6** Destek paketi: pythonguis tutorial · Teams-WebView2 forensic makalesi · johal içerik-çiftliği T3'e düşürüldü — counter sorgusu kayıtlı

## Sınırlar (dürüst)

- pywebview kendi zincirimizde denenmedi — F15 PoC'sinde ölçülecek
- youngju kaynağı AI-yardımlı yazılmış; iddialar referanslarla teyit edilebilir düzeyde, yine de tek-başına manşet taşımadı
- Sahibin estetik onayı pano.html'e verilmiş durumda; yeni-widget paradigması (Flet) bu onayı geçersiz kılar
