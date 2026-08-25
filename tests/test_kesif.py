"""F12b kesif.py testi — diff + merdiven mantığı (fixture tabanlı, ağsız)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import kesif  # noqa: E402


def m(mid, free=False, pp=None, cp=0.0, ctx=8192):
    return {"id": mid, "name": mid, "ctx": ctx,
            "pp": 0.0 if free else (pp if pp is not None else 0.000001),
            "cp": cp, "free": free}


class TestDiff(unittest.TestCase):
    def test_yeni_ve_kaldi(self):
        old = [m("a/old")]
        new = [m("a/new"), m("b/x")]
        tur = {c["tur"] for c in kesif.diff_snapshots(old, new)}
        ids = {c["id"] for c in kesif.diff_snapshots(old, new)}
        self.assertIn("YENI", tur)
        self.assertIn("KALDI", tur)
        self.assertEqual({"a/new", "b/x", "a/old"}, ids)

    def test_ucretsiz_oldu(self):
        old = [m("x/y", pp=0.000002)]
        new = [m("x/y", free=True)]
        out = kesif.diff_snapshots(old, new)
        self.assertEqual(out[0]["tur"], "UCRETSIZ-OLDU")

    def test_fiyat_degisti(self):
        old = [m("x/y", pp=0.001)]
        new = [m("x/y", pp=0.002)]
        self.assertEqual(kesif.diff_snapshots(old, new)[0]["tur"], "FIYAT")

    def test_ctx_degisti(self):
        old = [m("x/y", ctx=8192)]
        new = [m("x/y", ctx=16384)]
        self.assertEqual(kesif.diff_snapshots(old, new)[0]["tur"], "CTX")

    def test_degisiklik_yok(self):
        same = [m("x/y", pp=0.001), m("z/w", free=True)]
        self.assertEqual(kesif.diff_snapshots(same, same), [])


class TestMerdiven(unittest.TestCase):
    def test_l2_ucretsiz_yeni(self):
        notes = kesif.ladder([{"tur": "YENI", "id": "q/qwq:free", "detay": "",
                               "free": True, "ctx": 1}], [])
        self.assertTrue(any("L2" in n and "ucretsiz" in n for n in notes))

    def test_l3_kart_etki(self):
        card = {"id": "kart-1", "model": "eski-model-v1 (abonelik)"}
        ch = [{"tur": "KALDI", "id": "saglayici/eski-model-v1", "detay": ""}]
        notes = kesif.ladder(ch, [card])
        self.assertTrue(any("L3 KART-ETKI" in n and "kart-1" in n for n in notes))

    def test_l3_vurmaz_alakasizsa(self):
        card = {"id": "kart-1", "model": "Opus ailesi"}
        ch = [{"tur": "KALDI", "id": "saglayici/baska-sey", "detay": ""}]
        self.assertEqual(kesif.ladder(ch, [card]), [])

    def test_l2_buyuk_saglayici(self):
        notes = kesif.ladder([{"tur": "YENI", "id": "anthropic/claude-yeni",
                               "detay": "", "free": False, "ctx": 1}], [])
        self.assertTrue(any("L2" in n for n in notes))


if __name__ == "__main__":
    unittest.main()
