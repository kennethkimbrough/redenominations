"""Builds data/countries.json: one unbroken chain of currency changes per
country, from the first post-1945 currency to the present.

Each step cites one of the SOURCES below, or `None` when no citation has been
checked yet. A country is "verified" only if every step has a source and the
chain is unbroken (each step's new currency is the next step's old currency).
Otherwise it is "partial", and the site says so.

Run:  python3 data/build_countries.py
"""

from __future__ import annotations

import json
from pathlib import Path

SOURCES = {
    "wiki": {
        "title": "Redenomination — Wikipedia (table of currency redenominations)",
        "url": "https://en.wikipedia.org/wiki/Redenomination",
        "accessed": "2026-10-30",
    },
    "ec2866": {
        "title": "Council Regulation (EC) No 2866/98 on the conversion rates between the euro and the currencies of the Member States adopting the euro, Article 1 (as amended)",
        "url": "https://www.legislation.gov.uk/eur/1998/2866/data.html",
        "accessed": "2026-10-30",
    },
}

# Each country: iso, name, the currency in use at the start year, then steps.
# Step: (year, old currency, new currency, old units per new unit, source key, note)
COUNTRIES = [
    {
        "iso": "HU", "name": "Hungary", "start": 1945, "unit": "forint",
        "steps": [
            (1946, "Hungarian pengő", "Hungarian forint", 4e29, "wiki",
             "The largest redenomination on record. The pengő's 1946 hyperinflation peaked at prices doubling roughly every 15 hours."),
        ],
    },
    {
        "iso": "VE", "name": "Venezuela", "start": 1945, "unit": "bolívar digital",
        "steps": [
            (2008, "(old) Bolivar", "Bolivar Fuerte", 1_000, "wiki", None),
            (2018, "Bolivar Fuerte", "Bolívar Soberano", 100_000, "wiki", None),
            (2021, "Venezuelan bolívar (3rd)", "Venezuelan bolívar (4th)", 1_000_000, "wiki",
             "Fourteen zeros removed across the three reforms."),
        ],
    },
    {
        "iso": "BR", "name": "Brazil", "start": 1945, "unit": "real",
        "steps": [
            (1967, "Cruzeiro (antigo)", "Cruzeiro (novo)", 1_000, "wiki", None),
            (1986, "Cruzeiro (novo)", "Cruzado", 1_000, "wiki", None),
            (1989, "Cruzado", "Cruzado Novo", 1_000, "wiki", None),
            (1990, "Cruzado Novo", "Cruzeiro (third)", 1, "wiki", "A rename at par."),
            (1993, "Cruzeiro (third)", "Cruzeiro real", 1_000, "wiki", None),
            (1994, "Cruzeiro real", "Real", 2_750, "wiki",
             "The Plano Real. The only step in this dataset with a rate that is not a power of ten."),
        ],
    },
    {
        "iso": "AR", "name": "Argentina", "start": 1945, "unit": "peso",
        "steps": [
            (1970, "Peso moneda nacional", "Peso ley", 100, "wiki", None),
            (1983, "Peso ley", "Peso argentino", 10_000, "wiki", None),
            (1985, "Argentine peso (1983)", "Argentine austral", 1_000, "wiki", None),
            (1992, "Austral", "Peso (convertible)", 10_000, "wiki",
             "Thirteen zeros removed between 1970 and 1992."),
        ],
    },
    {
        "iso": "TR", "name": "Turkey", "start": 1945, "unit": "lira",
        "steps": [
            (2005, "Turkish lira", "Turkish new lira", 1_000_000, "wiki",
             "The word \"new\" was dropped again in 2009."),
        ],
    },
    {
        "iso": "PL", "name": "Poland", "start": 1945, "unit": "złoty",
        "steps": [
            (1949, "2nd Polish złoty", "3rd Polish złoty", 100, "wiki", None),
            (1995, "3rd Polish złoty", "4th Polish złoty", 10_000, "wiki", None),
        ],
    },
    {
        "iso": "RU", "name": "Russia (and the Soviet Union)", "start": 1945, "unit": "ruble",
        "steps": [
            (1947, "4th Soviet ruble", "5th Soviet ruble", 10, "wiki", None),
            (1961, "5th Soviet ruble", "6th Soviet ruble", 10, "wiki", None),
            (1991, "6th Soviet ruble", "7th Soviet ruble", 1, "wiki", None),
            (1992, "7th Soviet ruble", "1st Russian ruble", 1, "wiki", None),
            (1998, "First Russian ruble", "Second Russian ruble", 1_000, "wiki", None),
        ],
    },
    {
        "iso": "UA", "name": "Ukraine (and the Soviet Union)", "start": 1945, "unit": "hryvnia",
        "steps": [
            (1947, "4th Soviet ruble", "5th Soviet ruble", 10, "wiki", None),
            (1961, "5th Soviet ruble", "6th Soviet ruble", 10, "wiki", None),
            (1991, "6th Soviet ruble", "7th Soviet ruble", 1, "wiki", None),
            (1992, "7th Soviet ruble", "3rd Ukrainian karbovanets", 1, "wiki", None),
            (1996, "3rd Ukrainian karbovanets", "Hryvnia", 100_000, "wiki", None),
        ],
    },
    {
        "iso": "PE", "name": "Peru", "start": 1945, "unit": "sol",
        "steps": [
            (1985, "Peruvian sol (1863)", "Peruvian inti", 1_000, "wiki", None),
            (1991, "Peruvian inti", "Peruvian nuevo sol", 1_000_000, "wiki",
             "Renamed simply \"sol\" in 2015."),
        ],
    },
    {
        "iso": "BO", "name": "Bolivia", "start": 1945, "unit": "boliviano",
        "steps": [
            (1963, "First boliviano", "Peso boliviano", 1_000, "wiki", None),
            (1985, "Peso boliviano", "Boliviano", 1_000_000, "wiki", None),
        ],
    },
    {
        "iso": "FR", "name": "France", "start": 1945, "unit": "euro",
        "steps": [
            (1960, "French Franc", "New French Franc", 100, "wiki", None),
            (1999, "New French Franc", "Euro", 6.55957, "ec2866",
             "Euro conversion rate fixed on 31 December 1998; notes and coins followed in 2002."),
        ],
    },
    {
        "iso": "FI", "name": "Finland", "start": 1945, "unit": "euro",
        "steps": [
            (1963, "Finnish markka", "New Finnish markka", 100, "wiki", None),
            (1999, "New Finnish markka", "Euro", 5.94573, "ec2866", None),
        ],
    },
    {
        "iso": "GR", "name": "Greece", "start": 1945, "unit": "euro",
        "steps": [
            (1954, "Greek drachma (2nd)", "Greek drachma (3rd)", 1_000, "wiki", None),
            (2001, "Greek drachma (3rd)", "Euro", 340.75, "ec2866", None),
        ],
    },
    {
        "iso": "NI", "name": "Nicaragua", "start": 1945, "unit": "córdoba",
        "steps": [
            (1988, "Nicaraguan córdoba (1st)", "Nicaraguan córdoba (2nd)", 1_000, "wiki", None),
            (1991, "Nicaraguan córdoba (2nd)", "Nicaraguan córdoba (oro, 3rd)", 5_000_000, "wiki", None),
        ],
    },
    {
        "iso": "RS", "name": "Serbia (and Yugoslavia)", "start": 1945, "unit": "dinar",
        "steps": [
            (1966, "1944 dinara", "Yugoslav 1966 dinar", 100, "wiki", None),
            (1990, "1966 dinara", "Yugoslav 1990 dinar", 10_000, "wiki", None),
            (1992, "1990 dinara", "Yugoslav 1992 dinar", 10, "wiki", None),
            (1993, "1992 dinara", "Yugoslav 1993 dinar", 1_000_000, "wiki", None),
            (1994, "1993 dinara", "Yugoslav 1994 dinar", 1_000_000_000, "wiki", "January 1994."),
            (1994, "1994 dinara", "Yugoslav novi dinar", 13_000_000, "wiki",
             "Two reforms in one month: 22 zeros removed within 1993–94."),
        ],
    },
    {
        "iso": "MX", "name": "Mexico", "start": 1945, "unit": "peso",
        "steps": [
            (1993, "Peso mexicano", "Nuevo peso mexicano", 1_000, "wiki", "\"Nuevo\" was dropped in 1996."),
        ],
    },
    {
        "iso": "AO", "name": "Angola", "start": 1945, "unit": "kwanza",
        "steps": [
            (1975, "Second Angolan escudo", "First Kwanza", 1, "wiki", None),
            (1990, "First Kwanza", "Novo kwanza", 1, "wiki", None),
            (1995, "Novo kwanza", "Kwanza reajustado", 1_000, "wiki", None),
            (1999, "Kwanza reajustado", "Second Kwanza", 1_000_000, "wiki", None),
        ],
    },
    {
        "iso": "CL", "name": "Chile", "start": 1945, "unit": "peso",
        "steps": [
            (1960, "First Chilean peso", "Chilean escudo", 1_000, "wiki", None),
            (1975, "Chilean escudo", "Chilean peso", 1_000, "wiki", None),
        ],
    },
    {
        "iso": "UY", "name": "Uruguay", "start": 1945, "unit": "peso",
        "steps": [
            (1973, "Peso moneda nacional", "Nuevo peso", 1_000, "wiki", None),
            (1993, "Nuevo peso", "Peso uruguayo", 1_000, "wiki", None),
        ],
    },
    # ---- Partial chains: at least one step still needs a checked citation ----
    {
        "iso": "ZW", "name": "Zimbabwe", "start": 1980, "unit": "ZiG",
        "steps": [
            (2006, "Zimbabwean dollar (1st)", "Zimbabwean dollar (2nd)", 1_000, "wiki", None),
            (2008, "Zimbabwean dollar (2nd)", "Zimbabwean dollar (3rd)", 10_000_000_000, "wiki", None),
            (2009, "Zimbabwean dollar (3rd)", "Zimbabwean dollar (4th)", 1_000_000_000_000, "wiki",
             "25 zeros removed in three years. The 4th dollar was abandoned within weeks."),
            (2009, "Zimbabwean dollar (4th)", "United States dollar", None, None,
             "Multi-currency period; no fixed conversion. Later the RTGS dollar (2019) and ZiG (2024). Not yet cited."),
        ],
    },
    {
        "iso": "DE", "name": "Germany", "start": 1945, "unit": "euro",
        "steps": [
            (1948, "Reichsmark", "Deutsche Mark", 10, None,
             "The 1948 currency reform used different rates for cash, wages and savings; 10:1 is the headline rate. Not yet cited."),
            (1999, "Deutsche Mark", "Euro", 1.95583, "ec2866", None),
        ],
    },
    {
        "iso": "IL", "name": "Israel", "start": 1948, "unit": "new shekel",
        "steps": [
            (1980, "Israeli pound", "Israeli shekel (1st)", 10, "wiki", None),
            (1986, "Shekel", "New Shekel", 1_000, "wiki", None),
        ],
        "gap": "Starts at the Israeli pound of 1948; the Palestine pound it replaced at par is not yet cited.",
    },
    {
        "iso": "RO", "name": "Romania", "start": 1945, "unit": "leu",
        "steps": [
            (1947, "Romanian leu (1st)", "Romanian leu (2nd)", 20_000, None, "Not yet cited."),
            (1952, "Romanian leu (2nd)", "Romanian leu (3rd)", 20, None,
             "The 1952 reform used several rates; 20:1 was the main cash rate. Not yet cited."),
            (2005, "Romanian leu (3rd)", "Romanian leu (4th)", 10_000, "wiki", None),
        ],
    },
    {
        "iso": "BY", "name": "Belarus (and the Soviet Union)", "start": 1945, "unit": "ruble",
        "steps": [
            (1947, "4th Soviet ruble", "5th Soviet ruble", 10, "wiki", None),
            (1961, "5th Soviet ruble", "6th Soviet ruble", 10, "wiki", None),
            (1991, "6th Soviet ruble", "7th Soviet ruble", 1, "wiki", None),
            (1994, "7th Soviet ruble", "First Belarusian ruble", 10, "wiki", None),
            (2000, "First Belarusian ruble", "Second Belarusian ruble", 1_000, None,
             "Missing from the source table. Not yet cited."),
            (2016, "Second Belarusian ruble", "Third Belarusian ruble", 10_000, "wiki", None),
        ],
    },
    {
        "iso": "CD", "name": "DR Congo", "start": 1960, "unit": "franc",
        "steps": [
            (1967, "First congolese franc", "First zaïre", 1_000, "wiki", None),
            (1993, "First Zaïre", "Nouveau zaïre", 3_000_000, "wiki", None),
            (1998, "Nouveau zaïre", "Second Congolese franc", 100_000, "wiki", None),
        ],
        "gap": "Starts at independence in 1960; the Belgian Congo franc before it is not yet cited.",
    },
    {
        "iso": "GH", "name": "Ghana", "start": 1965, "unit": "cedi",
        "steps": [
            (1967, "Old cedi", "Ghanaian cedi", 1.2, "wiki", None),
            (2007, "Cedi", "New Ghanaian cedi", 10_000, "wiki", None),
        ],
        "gap": "Starts at the 1965 cedi; the Ghanaian pound and the West African pound before it are not yet cited.",
    },
    {
        "iso": "HR", "name": "Croatia (and Yugoslavia)", "start": 1945, "unit": "euro",
        "steps": [
            (1966, "1944 dinara", "Yugoslav 1966 dinar", 100, "wiki", None),
            (1990, "1966 dinara", "Yugoslav 1990 dinar", 10_000, "wiki", None),
            (1991, "Yugoslav 1990 dinar", "Croatian dinar", 1, "wiki", None),
            (1994, "Croatian dinar", "Croatian kuna", 1_000, "wiki", None),
            (2023, "Croatian kuna", "Euro", 7.5345, None, "Not yet cited."),
        ],
    },
    {
        "iso": "BG", "name": "Bulgaria", "start": 1945, "unit": "euro",
        "steps": [
            (1952, "Bulgarian lev (2nd)", "Bulgarian lev (3rd)", 100, None, "Not yet cited."),
            (1962, "Bulgarian lev (3rd)", "Bulgarian lev (4th)", 10, None, "Not yet cited."),
            (1999, "Bulgarian lev", "Bulgarian new lev", 1_000, "wiki", None),
            (2026, "Bulgarian new lev", "Euro", 1.95583, None, "Not yet cited."),
        ],
    },
]


def normalise(name: str) -> str:
    """Currency names in the source table are not perfectly consistent between rows
    ("Peso argentino" vs "Argentine peso (1983)"), so chain continuity is checked on a
    loose key: lowercase, letters and digits only."""
    return "".join(ch for ch in name.lower() if ch.isalnum())


# Pairs the source table spells differently but that are the same currency.
ALIASES = {
    normalise("Argentine peso (1983)"): normalise("Peso argentino"),
    normalise("Austral"): normalise("Argentine austral"),
    normalise("Shekel"): normalise("Israeli shekel (1st)"),
    normalise("Cedi"): normalise("Ghanaian cedi"),
    normalise("First Russian ruble"): normalise("1st Russian ruble"),
    normalise("1966 dinara"): normalise("Yugoslav 1966 dinar"),
    normalise("1990 dinara"): normalise("Yugoslav 1990 dinar"),
    normalise("1992 dinara"): normalise("Yugoslav 1992 dinar"),
    normalise("1993 dinara"): normalise("Yugoslav 1993 dinar"),
    normalise("1994 dinara"): normalise("Yugoslav 1994 dinar"),
    normalise("First Zaïre"): normalise("First zaïre"),
    normalise("Bulgarian lev"): normalise("Bulgarian lev (4th)"),
    normalise("Bolívar Soberano"): normalise("Venezuelan bolívar (3rd)"),
    normalise("Peso (convertible)"): normalise("Peso (convertible)"),
}


def key(name: str) -> str:
    k = normalise(name)
    return ALIASES.get(k, k)


def build() -> dict:
    out = []
    for c in COUNTRIES:
        steps = []
        for year, old, new, rate, src, note in c["steps"]:
            steps.append({"year": year, "old": old, "new": new, "rate": rate,
                          "source": SOURCES[src] if src else None, "note": note})
        unsourced = [s for s in steps if s["source"] is None]
        total_factor = 1.0
        for s in steps:
            if s["rate"]:
                total_factor *= s["rate"]
        out.append({
            "iso": c["iso"], "name": c["name"], "start": c["start"], "unit": c["unit"],
            "status": "verified" if not unsourced and not c.get("gap") else "partial",
            "unsourced_steps": len(unsourced),
            "gap": c.get("gap"),
            "steps": steps,
            "total_factor": total_factor,
        })
    out.sort(key=lambda c: (c["status"] != "verified", -c["total_factor"]))
    return {"sources": SOURCES, "countries": out,
            "verified": sum(c["status"] == "verified" for c in out),
            "partial": sum(c["status"] == "partial" for c in out)}


if __name__ == "__main__":
    data = build()
    path = Path(__file__).with_name("countries.json")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    print(f"wrote {path}: {data['verified']} verified, {data['partial']} partial")
