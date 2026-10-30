"""Fetches today's US-dollar exchange rates for the current unit of every
country in countries.json and writes data/rates.json.

Runs on a schedule in GitHub Actions (see .github/workflows/rates.yml) and
needs no API key. Two sources, tried in order:

1. The open-source currency-api dataset published daily to jsDelivr
   (https://github.com/fawazahmed0/exchange-api), which covers 200+
   currencies including thinly traded ones.
2. open.er-api.com, a free tier of ExchangeRate-API.

Rates are "units of local currency per 1 USD" on the day given. For countries
with a gap between the official and the street rate (Venezuela and Argentina
have had one for years) this is whatever rate the source publishes, and the
site says so.

Run:  python3 data/fetch_rates.py
"""

from __future__ import annotations

import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

# Current unit of each country chain -> ISO 4217 code. Serbia's novi dinar
# became the Serbian dinar at par in 2003; the chain ends at the rename.
UNITS = {
    "HU": "HUF", "VE": "VES", "BR": "BRL", "AR": "ARS", "TR": "TRY", "PL": "PLN",
    "RU": "RUB", "UA": "UAH", "PE": "PEN", "BO": "BOB", "FR": "EUR", "FI": "EUR",
    "GR": "EUR", "NI": "NIO", "RS": "RSD", "MX": "MXN", "AO": "AOA", "CL": "CLP",
    "UY": "UYU", "DE": "EUR", "IL": "ILS", "RO": "RON", "BY": "BYN", "CD": "CDF",
    "GH": "GHS", "HR": "EUR", "BG": "EUR", "ZW": "ZWG",
}

sys.path.insert(0, str(Path(__file__).parent))
from countries_more import MORE_UNITS  # noqa: E402
UNITS = {**UNITS, **MORE_UNITS}

SOURCES = [
    {
        "name": "currency-api (fawazahmed0/exchange-api) via jsDelivr",
        "url": "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.min.json",
        "page": "https://github.com/fawazahmed0/exchange-api",
        "pick": lambda d: (d.get("date"), {k.upper(): v for k, v in d["usd"].items()}),
    },
    {
        "name": "open.er-api.com (ExchangeRate-API free tier)",
        "url": "https://open.er-api.com/v6/latest/USD",
        "page": "https://www.exchangerate-api.com/docs/free",
        "pick": lambda d: (d.get("time_last_update_utc", "")[:16], d["rates"]),
    },
]


def fetch(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "redenominations-rates/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 - fixed https URLs above
        return json.load(resp)


def main() -> int:
    needed = sorted(set(UNITS.values()))
    for src in SOURCES:
        try:
            day, rates = src["pick"](fetch(src["url"]))
        except Exception as exc:  # noqa: BLE001 - try the next source
            print(f"{src['name']}: {exc!r}", file=sys.stderr)
            continue
        found = {code: float(rates[code]) for code in needed if code in rates and rates[code]}
        missing = [c for c in needed if c not in found]
        out = {
            "base": "USD",
            "date": day or date.today().isoformat(),
            "fetched": date.today().isoformat(),
            "source": {"title": src["name"], "url": src["page"]},
            "note": "Units of local currency per 1 US dollar. Published market/official rates; "
                    "where a parallel (street) rate exists, this is not it.",
            "rates": found,
            "missing": missing,
            "units": UNITS,
        }
        path = Path(__file__).with_name("rates.json")
        path.write_text(json.dumps(out, indent=1, sort_keys=True))
        print(f"wrote {path} from {src['name']} dated {out['date']}: {len(found)} rates, missing {missing}")
        return 0
    print("no rate source answered", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
