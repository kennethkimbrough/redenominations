"""Fetches annual exchange rates for every country (local units per US dollar,
period average) from 1960 on, plus the US consumer price index, from the
World Bank's open API. No key needed. Writes data/history.json.

Indicators:
  PA.NUS.FCRF  Official exchange rate (LCU per US$, period average)
  FP.CPI.TOTL  Consumer price index (2010 = 100), used for the United States only

Run:  python3 data/fetch_history.py
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

API = "https://api.worldbank.org/v2"
SOURCE = {
    "title": "World Bank, World Development Indicators: official exchange rate (PA.NUS.FCRF) and consumer price index (FP.CPI.TOTL)",
    "url": "https://data.worldbank.org/indicator/PA.NUS.FCRF",
}


def fetch_all(indicator: str) -> list[dict]:
    rows: list[dict] = []
    page = 1
    while True:
        url = f"{API}/country/all/indicator/{indicator}?format=json&per_page=20000&date=1960:{date.today().year}&page={page}"
        req = urllib.request.Request(url, headers={"User-Agent": "redenominations-history/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:  # noqa: S310 - fixed https host
            meta, data = json.load(resp)
        rows.extend(data or [])
        if page >= int(meta.get("pages", 1)):
            return rows
        page += 1


def main() -> int:
    fx = fetch_all("PA.NUS.FCRF")
    cpi = fetch_all("FP.CPI.TOTL")

    countries: dict[str, dict] = {}
    for r in fx:
        iso = r["countryiso3code"]
        if not iso or r["value"] is None:
            continue
        c = countries.setdefault(iso, {"name": r["country"]["value"], "rates": {}})
        c["rates"][int(r["date"])] = float(r["value"])
    # Aggregates (regions, income groups) have no 3-letter ISO country code of their own
    # in the same sense; drop entries whose code is not in the country list.
    us_cpi = {int(r["date"]): float(r["value"]) for r in cpi
              if r["countryiso3code"] == "USA" and r["value"] is not None}
    if not us_cpi or "IND" not in countries or "BRA" not in countries:
        print("unexpected response shape", file=sys.stderr)
        return 1

    out = {
        "source": SOURCE,
        "fetched": date.today().isoformat(),
        "note": "Exchange rates are annual averages in local currency units per US dollar as the "
                "World Bank reports them. The World Bank restates countries that redenominated in "
                "the latest unit; see data/history_probe.json and the site's method section.",
        "us_cpi": dict(sorted(us_cpi.items())),
        "countries": {iso: {"name": c["name"], "rates": dict(sorted(c["rates"].items()))}
                      for iso, c in sorted(countries.items()) if len(c["rates"]) >= 5},
    }
    path = Path(__file__).with_name("history.json")
    path.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    # A probe file the maintainer reads to decide how rebased series are handled.
    probe = {iso: {y: out["countries"][iso]["rates"].get(y) for y in (1965, 1980, 1985, 1990, 1994, 2000, 2023)}
             for iso in ("BRA", "ARG", "IND", "HUN", "TUR", "ZWE", "VEN", "DEU", "FRA", "POL") if iso in out["countries"]}
    Path(__file__).with_name("history_probe.json").write_text(json.dumps(probe, indent=1))
    print(f"wrote {path}: {len(out['countries'])} countries, US CPI {min(us_cpi)}–{max(us_cpi)}")
    print(json.dumps(probe, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
