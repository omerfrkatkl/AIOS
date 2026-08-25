"""F12c kotu.py testi — pencere matematiği + durum eşikleri + dolu-kanal filtresi."""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import kotu  # noqa: E402


class TestPencere(unittest.TestCase):
    def test_ayin_ortasi(self):
        start, end = kotu.window_bounds(date(2026, 8, 15), 1)
        self.assertEqual((start.isoformat(), end.isoformat()),
                         ("2026-08-01", "2026-08-31"))

    def test_gun_1_baslangic(self):
        start, end = kotu.window_bounds(date(2026, 3, 10), 10)
        self.assertEqual(start.isoformat(), "2026-03-10")
        self.assertEqual(end.isoformat(), "2026-04-09")

    def test_yil_devri(self):
        start, end = kotu.window_bounds(date(2027, 1, 5), 25)
        self.assertEqual((start.isoformat(), end.isoformat()),
                         ("2026-12-25", "2027-01-24"))

    def test_31_subatta(self):
        # gun=31 subat yok: onceki olusum ocak 31'i, sonraki olusum subat sonu (clamp)
        start, end = kotu.window_bounds(date(2026, 2, 20), 31)
        self.assertEqual((start.isoformat(), end.isoformat()),
                         ("2026-01-31", "2026-02-27"))

    def test_pencere_baslamadan(self):
        # ayin 25'i henuz gelmedi: pencere gecen ayin 25'i
        start, end = kotu.window_bounds(date(2026, 8, 10), 25)
        self.assertEqual((start.isoformat(), end.isoformat()),
                         ("2026-07-25", "2026-08-24"))


class TestDurum(unittest.TestCase):
    def test_esikler(self):
        self.assertEqual(kotu.status_for(None), "tanimsiz")
        self.assertEqual(kotu.status_for(0), "saglikli")
        self.assertEqual(kotu.status_for(79.9), "saglikli")
        self.assertEqual(kotu.status_for(80), "uyari")
        self.assertEqual(kotu.status_for(99.9), "uyari")
        self.assertEqual(kotu.status_for(100), "DOLU")
        self.assertEqual(kotu.status_for(150), "DOLU")


if __name__ == "__main__":
    unittest.main()
