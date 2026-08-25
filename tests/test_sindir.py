"""F10 sindir.py v2 testi — normalizasyon, iddia, çelişki, güven, check."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import sindir  # noqa: E402


class TestNorm(unittest.TestCase):
    def test_yuzde_isaretli(self):
        self.assertEqual(sindir.norm_percent("96%"), 96.0)
        self.assertEqual(sindir.norm_percent("80.6%"), 80.6)

    def test_kesir_formu(self):
        self.assertEqual(sindir.norm_percent("0.950"), 95.0)

    def test_ciplak_sayi(self):
        self.assertEqual(sindir.norm_percent("96.0"), 96.0)

    def test_gecersiz(self):
        self.assertIsNone(sindir.norm_percent("yok"))


class TestClaim(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        # report_path glob'unu geçici dizine yönlendir
        self.old_research = sindir.RESEARCH
        sindir.RESEARCH = Path(self.tmp.name)
        (sindir.RESEARCH / "R-001-test.md").write_text(
            "| **id** | R-001 |\n| **tetik** | 2099-01-01 |\n", encoding="utf-8")

    def tearDown(self):
        sindir.RESEARCH = self.old_research
        self.tmp.cleanup()

    def _claim(self, model, metrik, deger, obs="2026-08-20", harness=""):
        return {"model": model, "metrik": metrik, "deger": deger,
                "obs": obs, "harness": harness, "kaynak": "", "derece": "", "not": ""}

    def test_conflict_ayni_harness(self):
        rows = [self._claim("Opus5", "SWE-v", 96.0, harness="resmi"),
                self._claim("opus 5", "swe-v", 82.0, harness="Resmi")]
        out = sindir.detect_conflicts(rows)
        self.assertEqual(len(out), 1)

    def test_no_conflict_farkli_harness(self):
        rows = [self._claim("Opus5", "SWE-v", 96.0, harness="A"),
                self._claim("opus 5", "swe-v", 82.0, harness="B")]
        self.assertEqual(sindir.detect_conflicts(rows), [])

    def test_no_conflict_kucuk_delta(self):
        rows = [self._claim("X", "M", 95.0, harness="A"),
                self._claim("x", "m", 94.0, harness="A")]
        self.assertEqual(sindir.detect_conflicts(rows), [])


class TestGuven(unittest.TestCase):
    def test_t3_only_dusuk(self):
        tiers = {"T3": {"u"}}
        self.assertEqual(sindir.compute_guven(True, False, False, tiers), "düşük")

    def test_stale_dusuk(self):
        self.assertEqual(sindir.compute_guven(True, True, False, {"T2": {"u"}}), "düşük")

    def test_desteksiz_orta(self):
        self.assertEqual(sindir.compute_guven(False, False, False, {"T2": {f"u{i}" for i in range(2)}}), "orta")

    def test_tam_yuksek(self):
        tiers = {"T1-nötr": {"u1"}, "T2": {"u2", "u3", "u4"}}
        self.assertEqual(sindir.compute_guven(True, False, False, tiers), "yüksek")


class TestQhash(unittest.TestCase):
    def test_turkce_fold(self):
        self.assertEqual(sindir.qhash("güçlü model"), sindir.qhash("guclu model"))

    def test_match_baslik_zorunlu(self):
        self.assertEqual(sindir.match_ledger("claude mentioned in passing here"), [])


if __name__ == "__main__":
    unittest.main()
