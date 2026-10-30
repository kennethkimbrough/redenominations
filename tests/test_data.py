"""Data integrity checks. `python3 -m unittest` runs them with no dependencies."""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data"))

from build_countries import COUNTRIES, SOURCES, build, key  # noqa: E402

TABLE = json.loads((ROOT / "data" / "redenominations.json").read_text())
TABLE_KEYS = {(r["country"], r["year"], key(r["old"]), key(r["new"])): r for r in TABLE["rows"]}


class TableTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(TABLE["count"], len(TABLE["rows"]))
        self.assertGreaterEqual(TABLE["count"], 150)

    def test_rates_are_positive_and_sourced(self):
        for r in TABLE["rows"]:
            self.assertGreater(r["rate"], 0, r)
            self.assertTrue(r["source"]["url"].startswith("https://"), r)
            self.assertEqual(r["at_par"], r["rate"] == 1.0, r)

    def test_sorted_by_year(self):
        years = [r["year"] for r in TABLE["rows"]]
        self.assertEqual(years, sorted(years))


class ChainTests(unittest.TestCase):
    def test_every_chain_is_unbroken(self):
        for c in COUNTRIES:
            steps = c["steps"]
            years = [s[0] for s in steps]
            self.assertEqual(years, sorted(years), f"{c['name']}: steps out of order")
            for a, b in zip(steps, steps[1:]):
                self.assertEqual(key(a[2]), key(b[1]),
                                 f"{c['name']}: {a[0]} ends in '{a[2]}' but {b[0]} starts from '{b[1]}'")

    def test_sourced_steps_match_the_source_table(self):
        """A step that cites the Wikipedia table must appear in it with the same rate."""
        wiki = SOURCES["wiki"]["url"]
        for c in COUNTRIES:
            for year, old, new, rate, src, _ in c["steps"]:
                if src != "wiki":
                    continue
                match = next((r for (country, y, o, n), r in TABLE_KEYS.items()
                              if y == year and o == key(old) and n == key(new)), None)
                self.assertIsNotNone(match, f"{c['name']} {year} {old} -> {new} is not in the source table")
                self.assertEqual(match["rate"], float(rate), f"{c['name']} {year}: rate differs from the table")
                self.assertEqual(match["source"]["url"], wiki)

    def test_verified_means_fully_cited(self):
        data = build()
        for c in data["countries"]:
            if c["status"] == "verified":
                self.assertEqual(c["unsourced_steps"], 0, c["name"])
                self.assertIsNone(c["gap"], c["name"])
                self.assertTrue(all(s["rate"] for s in c["steps"]), c["name"])
            else:
                self.assertTrue(c["unsourced_steps"] or c["gap"], f"{c['name']} is partial for no reason")

    def test_euro_rates_come_from_the_regulation(self):
        data = build()
        for c in data["countries"]:
            for s in c["steps"]:
                if s["new"] == "Euro" and s["source"]:
                    self.assertTrue("2866/98" in s["source"]["title"] or "ECB press release" in s["source"]["title"], c["name"])

    def test_total_factor(self):
        data = build()
        brazil = next(c for c in data["countries"] if c["iso"] == "BR")
        # four ×1000 steps, one rename at par, then 2750:1
        self.assertAlmostEqual(brazil["total_factor"], 1_000 ** 4 * 2_750)
        hungary = next(c for c in data["countries"] if c["iso"] == "HU")
        self.assertEqual(hungary["total_factor"], 4e29)


class RateTests(unittest.TestCase):
    """rates.json is written by the scheduled job; these checks run only when it exists."""

    def setUp(self):
        path = ROOT / "data" / "rates.json"
        if not path.exists():
            self.skipTest("rates.json not fetched yet")
        self.rates = json.loads(path.read_text())

    def test_every_country_has_a_unit_code(self):
        from fetch_rates import UNITS
        for c in COUNTRIES:
            self.assertIn(c["iso"], UNITS, c["name"])

    def test_rates_are_positive_and_dated(self):
        self.assertRegex(self.rates["date"], r"^\d{4}-\d{2}-\d{2}")
        for code, value in self.rates["rates"].items():
            self.assertGreater(value, 0, code)
        self.assertLessEqual(len(self.rates["missing"]), 8, self.rates["missing"])
        self.assertAlmostEqual(self.rates["rates"].get("EUR", 0.9), 0.9, delta=0.4)


if __name__ == "__main__":
    unittest.main()
