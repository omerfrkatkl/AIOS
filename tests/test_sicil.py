"""F12d sicil.py testi — kayıt + pivot + eşik-guard + TEST-etiket ayrımı."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import sicil  # noqa: E402


class TestSicil(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = sicil.SICIL
        sicil.SICIL = Path(self.tmp.name) / "sicil.jsonl"

    def tearDown(self):
        sicil.SICIL = self.old
        self.tmp.cleanup()

    def _ekle(self, kanal, gorev, sonuc, test=False):
        ns = type("A", (), {"kanal": kanal, "gorev": gorev, "sonuc": sonuc,
                            "sure": None, "not_": "", "kaynak": "sahip-beyani",
                            "test": test})()
        return sicil.cmd_ekle(ns)

    def test_ekle_ve_yukle(self):
        rc = self._ekle("opencode-cli", "kod", "basari")
        rows = sicil._load()
        self.assertEqual(rc, 0)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["etiket"], "gercek")

    def test_gecersiz_gorev_red(self):
        rc = self._ekle("x", "resim", "basari")
        self.assertEqual(rc, 2)

    def test_ozet_yetersiz_veri_guard(self):
        import io, contextlib
        for _ in range(3):
            self._ekle("a-kanal", "kod", "basari")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sicil.cmd_ozet(type("A", (), {"json": False, "test": False})())
        out = buf.getvalue()
        self.assertIn("yetersiz veri", out)
        self.assertNotIn("%100", out)

    def test_ozet_oran_n_gecmis(self):
        import io, contextlib
        for _ in range(5):
            self._ekle("b-kanal", "ozet", "basari")
        self._ekle("b-kanal", "ozet", "hata")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sicil.cmd_ozet(type("A", (), {"json": False, "test": False})())
        out = buf.getvalue()
        self.assertIn("%83", out)  # 5/6

    def test_test_etiketi_ayriligi(self):
        import io, contextlib
        self._ekle("gerek-kanal", "kod", "basari", test=False)
        self._ekle("test-kanal", "kod", "basari", test=True)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sicil.cmd_ozet(type("A", (), {"json": False, "test": True})())
        out = buf.getvalue()
        self.assertIn("test-kanal", out)
        self.assertNotIn("gerek-kanal", out)

    def test_json_cikti_yeterlilik_bayragi(self):
        import io, contextlib, json as _json
        for _ in range(sicil.MIN_N):
            self._ekle("c-kanal", "metin", "basari")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sicil.cmd_ozet(type("A", (), {"json": True, "test": False})())
        data = _json.loads(buf.getvalue())
        self.assertTrue(data["c-kanal"]["yeterli_veri"])
        self.assertEqual(data["c-kanal"]["basari_orani"], 1.0)


class TestOpenRouterKeyParse(unittest.TestCase):
    """kotu.parse_openrouter_key — R-004 tabanlı kapak-belirleme."""

    def test_ucretsiz_hesap_50(self):
        b = __import__("kotu").parse_openrouter_key(
            {"data": {"is_free_tier": True, "usage_daily": 0.0, "limit_remaining": None}})
        self.assertEqual(b["gunluk_kapak_istek"], 50)
        self.assertTrue(b["is_free_tier"])

    def test_kredili_hesap_1000(self):
        b = __import__("kotu").parse_openrouter_key(
            {"data": {"is_free_tier": False, "usage_daily": 1.5, "limit_remaining": None}})
        self.assertEqual(b["gunluk_kapak_istek"], 1000)
        self.assertFalse(b["is_free_tier"])


if __name__ == "__main__":
    unittest.main()
