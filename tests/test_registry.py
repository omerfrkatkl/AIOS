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

class TestYetenekEtki(unittest.TestCase):
    """F12a ileri: yetenek ters-bakışı + G53 etki raporu."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = registry.CARDS
        registry.CARDS = Path(self.tmp.name)
        (registry.CARDS / "a.json").write_text(json.dumps(kart(
            id="tek-kod", yetenekler=["kod"])), encoding="utf-8")
        (registry.CARDS / "b.json").write_text(json.dumps(kart(
            id="coklu", saglayici="Y", model="m2", yetenekler=["kod", "metin"])), encoding="utf-8")
        (registry.CARDS / "c.json").write_text(json.dumps(kart(
            id="pasif-kanal", saglayici="Z", model="m3", durum="pasif",
            yetenekler=["ozet"])), encoding="utf-8")

    def tearDown(self):
        registry.CARDS = self.old
        self.tmp.cleanup()

    def test_yetenek_ters_bakis_aktif_sayisi(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = registry.cmd_yetenek(type("A", (), {"yetenek": "KOD"})())
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("2 sağlayıcı", out)          # pasif hariç
        self.assertNotIn("pasif-kanal", out)

    def test_yetenek_saglayici_yok(self):
        rc = registry.cmd_yetenek(type("A", (), {"yetenek": "gorsel"})())
        self.assertEqual(rc, 1)

    def test_etki_cikarma_yedegi_varsa_zayiflar(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = registry.cmd_etki(type("A", (), {"kanal": "tek-kod"})())
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("KIRILMAZ", out)             # coklu da kod sağlıyor
        self.assertIn("ZAYIFLAR: 'kod' tek sağlayıcıya düşer → coklu", out)

    def test_etki_kirilir_ve_zayiflar_birlikte(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = registry.cmd_etki(type("A", (), {"kanal": "coklu"})())
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("KIRILIR: metin", out)       # metni sağlayan başka yok
        self.assertIn("ZAYIFLAR: 'kod' tek sağlayıcıya düşer → tek-kod", out)

    def test_etki_pasif_nötr(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = registry.cmd_etki(type("A", (), {"kanal": "pasif-kanal"})())
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("PASİF", out)

    def test_etki_kart_yok(self):
        rc = registry.cmd_etki(type("A", (), {"kanal": "yok-boyle"})())
        self.assertEqual(rc, 1)


class TestAracYonlendirme(unittest.TestCase):
    """F12a son madde: calistirma alanı + route --json."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old = registry.CARDS
        registry.CARDS = Path(self.tmp.name)
        (registry.CARDS / "a.json").write_text(json.dumps(kart(
            id="arac-ana", yetenekler=["kod"],
            calistirma="test CLI komutu")), encoding="utf-8")
        (registry.CARDS / "b.json").write_text(json.dumps(kart(
            id="arac-yedek", saglayici="Y", model="m2", yetenekler=["kod"],
            calistirma="yedek komut")), encoding="utf-8")

    def tearDown(self):
        registry.CARDS = self.old
        self.tmp.cleanup()

    def _route(self, **kw):
        ns = {"task": "kod refactor yap", "gizli": False, "json": False}
        ns.update(kw)
        return registry.cmd_route(type("A", (), ns)())

    def test_yurutme_satiri_insanda(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = self._route()
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("YURUTME: test CLI komutu", out)

    def test_json_yapisal(self):
        import io, contextlib, json as _json
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = self._route(json=True)
        data = _json.loads(buf.getvalue())
        self.assertEqual(rc, 0)
        self.assertEqual(data["oneri"]["id"], "arac-ana")
        self.assertEqual(data["oneri"]["yurutme"], "test CLI komutu")
        self.assertEqual(data["alternatifler"], ["arac-yedek"])
        self.assertIn("gerekli_yetenekler", data)



if __name__ == "__main__":
    unittest.main()
