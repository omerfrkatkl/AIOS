"""F12a registry.py testi — şema doğrulama + yönlendirici determinizmi."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import registry  # noqa: E402


def kart(**over):
    base = {"id": "test", "kanal": "api", "saglayici": "X", "model": "m",
            "gizlilik": "bulut", "yetenekler": ["kod"], "durum": "aktif",
            "dogrulanma": "2026-01-01", "kanit": "gozlem"}
    base.update(over)
    return base


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = registry.CARDS
        registry.CARDS = Path(self.tmp.name)

    def tearDown(self):
        registry.CARDS = self.old
        self.tmp.cleanup()

    def test_gecerli_kart(self):
        errs = registry.validate_card(kart(), set())
        self.assertEqual(errs, [])

    def test_eksik_zorunlu(self):
        c = kart()
        del c["kanit"]
        errs = registry.validate_card(c, set())
        self.assertTrue(any("kanit" in e for e in errs))

    def test_enum_disi(self):
        errs = registry.validate_card(kart(gizlilik="bilinmiyor"), set())
        self.assertTrue(any("gizlilik" in e for e in errs))

    def test_id_tekrari(self):
        seen = {"test"}
        errs = registry.validate_card(kart(), seen)
        self.assertTrue(any("tekrar" in e for e in errs))

    def test_gelecek_tarih(self):
        errs = registry.validate_card(kart(dogrulanma="2999-01-01"), set())
        self.assertTrue(any("gelecekte" in e for e in errs))


class TestRoute(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = registry.CARDS
        registry.CARDS = Path(self.tmp.name)
        (registry.CARDS / "a.json").write_text(json.dumps(
            kart(id="yerel-a", gizlilik="yerel", durum="aktif")), encoding="utf-8")

    def tearDown(self):
        registry.CARDS = self.old
        self.tmp.cleanup()

    def _route_needed(self, task):
        needed = set()
        for cap, words in registry.HINTS.items():
            if any(w in task for w in words):
                needed.add(cap)
        return needed

    def test_ipucu_eslesme(self):
        self.assertEqual(self._route_needed("kod refactor yap"), {"kod"})
        self.assertIn("arastirma", self._route_needed("benchmark karsilastir"))

    def test_bilinmeyen_gorev(self):
        self.assertEqual(self._route_needed("resim ciz"), set())


if __name__ == "__main__":
    unittest.main()
