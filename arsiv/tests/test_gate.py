#!/usr/bin/env python3
"""
Kapının EŞLEŞTİRME katmanının yanlışlama testi.

Ölçtüğü: 20 vakada yakalama oranı ve yanlış-pozitif oranı.
Ölçmediği: hook'un Claude Code içinde gerçekten ateşleyip ateşlemediği.
           Onun kanıtı .gate-canary.log dosyasıdır — canlı ortamda kontrol edilir.

Karar kuralı (önceden yazıldı, sonuca bakılmadan):
  - Yakalama < %80  -> tetikleyici/eşleştirme tasarımı yanlış, v2'ye geçme.
  - Yanlış-pozitif > %20 -> mekanizma güvenilmez, insan onayı vazgeçilmez.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from gate import parse_ledger, find_matches  # noqa: E402

LEDGER = Path(__file__).resolve().parents[1] / "REJECTED.md"

# (metin, yakalanmalı mı, açıklama)
CASES = [
    # --- GERÇEK METİN (canlı oturumdan, 2026-08-15 19:14) ---
    ("Şu an CLAUDE.md'de zaten net bir karar var: Topoloji C — AIOS ayrı, projeler kardeş, "
     "iç içe değil. Projeleri AIOS içine almak bu kararı tersine çevirir — geri alması ucuz "
     "değil ve yön/kapsam etkisi var, yani protokole göre T-A ve sahip onayı gerektiriyor.",
     True, "GERÇEK: R-001, 'içine' çekimi — v1 bunu kaçırmıştı"),

    # --- YAKALANMALI (10) ---
    ("Bence yönetilen projeleri AIOS içinde tutalım, tek depo daha temiz olur.",
     True, "R-001 doğrudan"),
    ("Klasör yapısını değiştirip iç içe topoloji kuralım.",
     True, "R-001 farklı ifade"),
    ("Hafıza için knowledge graph tabanlı hafıza katmanı öneriyorum.",
     True, "R-002 doğrudan"),
    ("Zep kullanalım, temporal knowledge graph tam bu iş için.",
     True, "R-002 iki anahtar"),
    ("Kendi makinende self-hosted NIM kurup modelleri oradan çağıralım.",
     True, "R-003 doğrudan"),
    ("NVIDIA NIM kendi sunucumuzda çalışsın, bağımsızlık sağlar.",
     True, "R-003 farklı ifade"),
    ("BMAD METHOD benimseyelim, tüm yaşam döngüsünü kapsıyor.",
     True, "R-004, büyük harf + noktalama"),
    ("Bu iş için agent teams kullanalım, paralel ilerleriz.",
     True, "R-005 doğrudan"),
    ("Paralel ajan takımı kurup dilimleri aynı anda yürütelim.",
     True, "R-005 farklı ifade"),
    ("Projeleri  AIOS   içinde tutmak bakımı kolaylaştırır.",
     True, "R-001, bozuk boşluklu"),

    # --- YAKALANMAMALI (10) ---
    ("Hosted NVIDIA API'yi seyrek ikinci görüş için deneyebiliriz.",
     False, "R-003 kapsamı dışında — hosted vs self-hosted"),
    ("Read-only subagent ile keşif yapalım, yazma ana ajanda kalsın.",
     False, "R-005'in önerdiği alternatif"),
    ("Projects altında AIOS ve knowledge-base kardeş dizinler olarak dursun.",
     False, "R-001'in tam tersi — onaylanmış topoloji"),
    ("SQLite'ı salt-okuma panel için indeks katmanı olarak kullanalım.",
     False, "R-002 kapsamı dışında"),
    ("Graph veri yapıları algoritma tarafında işimize yarayabilir.",
     False, "yakın-ıska: 'graph' geçiyor ama hafıza bağlamı yok"),
    ("Ajanların takım halinde çalışması literatürde tartışmalı bir konu.",
     False, "yakın-ıska: konu geçiyor, öneri değil"),
    ("Stop hook'u yazıp REJECTED bankasını taratalım.",
     False, "tamamen ilgisiz öneri"),
    ("Kullanıcı profilinin ne kadarının her oturumda yükleneceğini ölçelim.",
     False, "açık soru S8, red değil"),
    ("Markdown + git kaynak-of-truth kalsın, Obsidian yalnızca görünüm olsun.",
     False, "onaylanmış karar"),
    ("BMAD'in dosya-tabanlı devir fikrini ödünç alabiliriz.",
     False, "R-004 kapsamı dışında — bütün benimseme değil"),
    ("AIOS için yeni bir proje açalım, adı ne olsun?",
     False, "gevşek eşleştirici tuzağı: proje+aios+için ayrı bağlamda"),
    ("Bu projeler listesini AIOS panelinde göstermek iyi olur.",
     False, "gevşek eşleştirici tuzağı: projeler+aios yakın ama farklı anlam"),
]


def main() -> int:
    records = parse_ledger(LEDGER)
    print(f"Bankada {len(records)} onaylı kayıt bulundu.\n")

    yakalanan = kacan = yanlis_pozitif = dogru_negatif = 0
    hatalar = []

    for metin, beklenen, aciklama in CASES:
        hits = find_matches(metin, records)
        bulundu = bool(hits)
        ids = ",".join(h["id"] for h in hits) or "-"
        dogru = bulundu == beklenen

        if beklenen and bulundu:
            yakalanan += 1
        elif beklenen and not bulundu:
            kacan += 1
            hatalar.append(("KAÇAN", metin, aciklama, ids))
        elif not beklenen and bulundu:
            yanlis_pozitif += 1
            hatalar.append(("YANLIŞ-POZİTİF", metin, aciklama, ids))
        else:
            dogru_negatif += 1

        print(f"{'✓' if dogru else '✗'} [{ids:>7}] {aciklama}")

    pozitif, negatif = yakalanan + kacan, yanlis_pozitif + dogru_negatif
    yakalama_orani = 100 * yakalanan / pozitif
    yp_orani = 100 * yanlis_pozitif / negatif

    print("\n" + "=" * 60)
    print(f"Yakalama oranı   : {yakalanan}/{pozitif}  = %{yakalama_orani:.0f}   (eşik: ≥%80)")
    print(f"Yanlış-pozitif   : {yanlis_pozitif}/{negatif}  = %{yp_orani:.0f}   (eşik: ≤%20)")

    if hatalar:
        print("\nHatalar:")
        for tur, metin, aciklama, ids in hatalar:
            print(f"  {tur}: {aciklama}\n    -> [{ids}] {metin[:70]}")

    gecti = yakalama_orani >= 80 and yp_orani <= 20
    print("\n" + ("SONUÇ: GEÇTİ" if gecti else "SONUÇ: KALDI"))
    return 0 if gecti else 1


if __name__ == "__main__":
    sys.exit(main())
