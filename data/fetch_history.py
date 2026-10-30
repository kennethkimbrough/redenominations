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


def get_json(url: str, attempts: int = 3):
    last: Exception | None = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "redenominations-history/1.0"})
            with urllib.request.urlopen(req, timeout=90) as resp:  # noqa: S310 - fixed https hosts
                return json.load(resp)
        except Exception as exc:  # noqa: BLE001 - retried
            last = exc
            print(f"::warning::{url}: attempt {i + 1} failed: {exc!r}")
    raise RuntimeError(f"{url}: {last!r}")


def fetch_all(indicator: str) -> list[dict]:
    rows: list[dict] = []
    page = 1
    while True:
        url = f"{API}/country/all/indicator/{indicator}?format=json&per_page=20000&date=1960:{date.today().year}&page={page}"
        body = get_json(url)
        if not isinstance(body, list) or len(body) != 2:
            raise RuntimeError(f"unexpected World Bank response for {indicator}: {str(body)[:200]}")
        meta, data = body
        rows.extend(data or [])
        if page >= int(meta.get("pages", 1)):
            return rows
        page += 1


CURRENCIES_SOURCE = {
    "title": "REST Countries (restcountries.com), currencies field",
    "url": "https://restcountries.com/v3.1/all?fields=cca3,currencies",
}


def fetch_currency_names() -> dict[str, dict]:
    """ISO3 -> {"code", "name"} for each country's current currency. Empty on failure."""
    try:
        rows = get_json(CURRENCIES_SOURCE["url"])
    except Exception as exc:  # noqa: BLE001 - names are optional
        print(f"::warning::currency names unavailable: {exc!r}")
        return {}
    out = {}
    for r in rows:
        cur = r.get("currencies") or {}
        if not cur:
            continue
        code = sorted(cur)[0] if len(cur) > 1 else next(iter(cur))
        out[r["cca3"]] = {"code": code, "name": cur[code].get("name", code)}
    return out


def main() -> int:
    names = fetch_currency_names()
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
        print(f"::error::unexpected response shape: {len(fx)} fx rows, {len(cpi)} cpi rows, {len(countries)} countries")
        return 1

    out = {
        "source": SOURCE,
        "fetched": date.today().isoformat(),
        "note": "Exchange rates are annual averages in local currency units per US dollar as the "
                "World Bank reports them. The World Bank restates countries that redenominated in "
                "the latest unit; see data/history_probe.json and the site's method section.",
        "us_cpi": dict(sorted(us_cpi.items())),
        "currencies_source": CURRENCIES_SOURCE if names else None,
        "countries": {iso: {"name": c["name"], "currency": names.get(iso), "rates": dict(sorted(c["rates"].items()))}
                      for iso, c in sorted(countries.items()) if len(c["rates"]) >= 5},
    }
    path = Path(__file__).with_name("history.json")
    path.write_text(json.dumps(out, separators=(",", ":"), ensure_ascii=False))
    # A probe file the maintainer reads to decide how rebased series are handled.
    probe = {iso: {y: out["countries"][iso]["rates"].get(y) for y in (1965, 1980, 1985, 1990, 1994, 2000, 2023)}
             for iso in ("BRA", "ARG", "IND", "HUN", "TUR", "ZWE", "VEN", "DEU", "FRA", "POL") if iso in out["countries"]}
    Path(__file__).with_name("history_probe.json").write_text(json.dumps(probe, indent=1))
    named = sum(1 for c in out["countries"].values() if c["currency"])
    print(f"wrote {path}: {len(out['countries'])} countries ({named} with a currency name), US CPI {min(us_cpi)}–{max(us_cpi)}")
    print(json.dumps(probe, indent=1))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - surface the cause as a workflow annotation
        print(f"::error::fetch_history failed: {exc!r}")
        sys.exit(1)
