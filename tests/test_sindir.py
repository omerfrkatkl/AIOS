"""F10 sindir.py duman testi — qhash normalizasyonu + LEDGER eşik davranışı."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import sindir  # noqa: E402


class TestSindir(unittest.TestCase):
    def test_qhash_turkce_ascii_esit(self):
        self.assertEqual(sindir.qhash("güçlü model karşılaştırma"),
                         sindir.qhash("guclu model karsilastirma"))

    def test_qhash_sira_bagimsiz(self):
        self.assertEqual(sindir.qhash("model benchmark 2026"),
                         sindir.qhash("2026 benchmark model"))

    def test_match_baslik_kelimesi_zorunlu(self):
        # 'Claude' geçiyor ama hiçbir başlık kelimesi vurmiyor -> eslesme YOK
        hits = sindir.match_ledger("claude mentioned in passing here")
        self.assertEqual(hits, [])

    def test_extract_claims_bos_girdi(self):
        self.assertEqual(sindir.extract_claims(["kisa", "satirlar"]), [])


if __name__ == "__main__":
    unittest.main()
