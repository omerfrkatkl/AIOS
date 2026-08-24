#!/usr/bin/env python3
"""
Gate MATCHING-layer falsification test (ported from arsiv/tests/test_gate.py).

Measures   : catch rate and false-positive rate over 23 cases.
Does NOT   : measure whether the hook actually fires inside an agent tool.
             That proof is logs/aios.jsonl (gate events) - checked live.

Decision rule (written before the run, never adjusted after):
  - catch  < 80%  -> matcher design is wrong
  - FP     > 20%  -> mechanism unreliable
Ported set historically achieves 100% / 0%.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "hooks"))
from gate import parse_ledger, find_matches  # noqa: E402

LEDGER = Path(__file__).resolve().parents[1] / "LEDGER.md"

# (metin, yakalanmalı mı, açıklama) - vaka metinleri arşivden GERÇEK/taşınmış
CASES = [
    # --- GERÇEK METİN (canlı oturumdan, 2026-08-15 19:14) ---
    ("Şu an CLAUDE.md'de zaten net bir karar var: Topoloji C — AIOS ayrı, projeler kardeş, "
     "iç içe değil. Projeleri AIOS içine almak bu kararı tersine çevirir — geri alması ucuz "
     "değil ve yön/kapsam etkisi var, yani protokole göre T-A ve sahip onayı gerektiriyor.",
     True, "GERÇEK: L-001, 'içine' çekimi — v1 bunu kaçırmıştı"),

    # --- YAKALANMALI (10) ---
    ("Bence yönetilen projeleri AIOS içinde tutalım, tek depo daha temiz olur.",
     True, "L-001 doğrudan"),
    ("Klasör yapısını değiştirip iç içe topoloji kuralım.",
     True, "L-001 farklı ifade"),
    ("Hafıza için knowledge graph tabanlı hafıza katmanı öneriyorum.",
     True, "L-002 doğrudan"),
    ("Zep kullanalım, temporal knowledge graph tam bu iş için.",
     True, "L-002 iki anahtar"),
    ("Kendi makinende self-hosted NIM kurup modelleri oradan çağıralım.",
     True, "L-003 doğrudan"),
    ("NVIDIA NIM kendi sunucumuzda çalışsın, bağımsızlık sağlar.",
     True, "L-003 farklı ifade"),
    ("BMAD METHOD benimseyelim, tüm yaşam döngüsünü kapsıyor.",
     True, "L-004, büyük harf + noktalama"),
    ("Bu iş için agent teams kullanalım, paralel ilerleriz.",
     True, "L-005 doğrudan"),
    ("Paralel ajan takımı kurup dilimleri aynı anda yürütelim.",
     True, "L-005 farklı ifade"),
    ("Projeleri  AIOS   içinde tutmak bakımı kolaylaştırır.",
     True, "L-001, bozuk boşluklu"),

    # --- YAKALANMAMALI (12) ---
    ("Hosted NVIDIA API'yi seyrek ikinci görüş için deneyebiliriz.",
     False, "L-003 kapsamı dışında — hosted vs self-hosted"),
    ("Read-only subagent ile keşif yapalım, yazma ana ajanda kalsın.",
     False, "L-005'in önerdiği alternatif"),
    ("Projects altında AIOS ve knowledge-base kardeş dizinler olarak dursun.",
     False, "L-001'in tam tersi — onaylanmış topoloji"),
    ("SQLite'ı salt-okuma panel için indeks katmanı olarak kullanalım.",
     False, "L-002 kapsamı dışında"),
    ("Graph veri yapıları algoritma tarafında işimize yarayabilir.",
     False, "yakın-ıska: 'graph' geçiyor ama hafıza bağlamı yok"),
    ("Ajanların takım halinde çalışması literatürde tartışmalı bir konu.",
     False, "yakın-ıska: konu geçiyor, öneri değil"),
    ("Stop hook'u yazıp LEDGER bankasını taratalım.",
     False, "tamamen ilgisiz öneri"),
    ("Kullanıcı profilinin ne kadarının her oturumda yükleneceğini ölçelim.",
     False, "açık soru S8, red değil"),
    ("Markdown + git kaynak-of-truth kalsın, Obsidian yalnızca görünüm olsun.",
     False, "onaylanmış karar"),
    ("BMAD'in dosya-tabanlı devir fikrini ödünç alabiliriz.",
     False, "L-004 kapsamı dışında — bütün benimseme değil"),
    ("AIOS için yeni bir proje açalım, adı ne olsun?",
     False, "gevşek eşleştirici tuzağı: proje+aios+için ayrı bağlamda"),
    ("Bu projeler listesini AIOS panelinde göstermek iyi olur.",
     False, "gevşek eşleştirici tuzağı: projeler+aios yakın ama farklı anlam"),
]


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ledger = parse_ledger(LEDGER)
    records = ledger["reject"] + ledger["defer"]
    print(f"Kütükte {len(records)} aktif kayıt bulundu "
          f"({len(ledger['reject'])} rejected, {len(ledger['defer'])} deferred).\n")

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
