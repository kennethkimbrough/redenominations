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
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from countries_more import MORE, MORE_ALIASES, MORE_UNITS, MORE_WORLD_BANK  # noqa: E402
from countries_world import WORLD_SOURCES  # noqa: E402

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
    "ecb-hr": {
        "title": "ECB press release, 12 July 2022: Croatia to join euro area on 1 January 2023 (kuna fixed at 7.53450 = EUR 1)",
        "url": "https://www.ecb.europa.eu/press/pr/date/2022/html/ecb.pr220712~b97dd38de3.en.html",
        "accessed": "2026-10-30",
    },
    "bundesbank-1948": {
        "title": "Deutsche Bundesbank, \"The economic and currency reform of 1948: the basis for stable money\" (wages and rents converted 1:1; balances at less than 1:10; 60 RM exchanged for 40 DM per head)",
        "url": "https://www.bundesbank.de/en/press/contributions/the-economic-and-currency-reform-of-1948-the-basis-for-stable-money-915302",
        "accessed": "2026-10-30",
    },
    "ecb-bg": {
        "title": "ECB press release, 8 July 2025: Bulgaria to join euro area on 1 January 2026 (lev fixed at 1.95583 = EUR 1)",
        "url": "https://www.ecb.europa.eu/press/pr/date/2025/html/ecb.pr250708~b9676a9fa8.en.html",
        "accessed": "2026-10-30",
    },
    "bog-gh": {
        "title": "Bank of Ghana, \"Evolution of currency in Ghana\" (cedi of 19 July 1965 equal to 8s 4d; new cedi of 1967 at ¢1.20 = N¢1.00)",
        "url": "https://www.bog.gov.gh/bank-notes-coins/evolution-of-currency-in-ghana/",
        "accessed": "2026-10-30",
    },
}


def _wp(title: str, page: str, says: str) -> dict:
    return {"title": f"{title} — Wikipedia ({says})",
            "url": f"https://en.wikipedia.org/wiki/{page}", "accessed": "2026-10-30"}


SOURCES.update({
    "wp-ghpound": _wp("Ghanaian pound", "Ghanaian_pound", "replaced the British West African pound at par in 1958"),
    "wp-leone": _wp("Sierra Leonean leone", "Sierra_Leonean_leone", "introduced 4 August 1964 at 2 leones to the West African pound"),
    "wp-rnpound": _wp("Rhodesia and Nyasaland pound", "Rhodesia_and_Nyasaland_pound", "replaced the Southern Rhodesian pound at par; Zambia's pound at par with it"),
    "wp-zmpound": _wp("Zambian pound", "Zambian_pound", "replaced the Rhodesia and Nyasaland pound at par in 1964; kwacha at £1 = K2 in 1968"),
    "wp-sdpound": _wp("Sudanese pound", "Sudanese_pound", "replaced the Egyptian pound at par after independence"),
    "wp-mzescudo": _wp("Mozambican escudo", "Mozambican_escudo", "currency of Mozambique 1914–1980, replaced by the metical at par"),
    "wp-stescudo": _wp("São Tomé and Príncipe escudo", "S%C3%A3o_Tom%C3%A9_and_Pr%C3%ADncipe_escudo", "currency 1914–1977, replaced at par by the dobra"),
    "wp-cdfranc": _wp("Congolese franc", "Congolese_franc", "the Belgian Congo franc remained the currency after independence in 1960"),
    "wp-vnd": _wp("Vietnamese đồng", "Vietnamese_%C4%91%E1%BB%93ng", "14 September 1985: one new đồng worth 10 old"),
    "wp-ilpound": _wp("Israeli pound", "Israeli_pound", "replaced the Palestine pound in June 1952, keeping its par peg to sterling"),
    "wp-mtlira": _wp("Maltese lira", "Maltese_lira", "at exact 1:1 with sterling until 1971; decimalised in May 1972"),
    "wp-csk": _wp("Czechoslovak koruna", "Czechoslovak_koruna", "1953: 5:1 up to 1,500 korunas, 50:1 beyond; 1993 split at par"),
    "wp-roleu": _wp("Romanian leu", "Romanian_leu", "15 August 1947 at 20,000:1; 1952 at rates from 20 to 400 old lei per new"),
    "wp-bglev": _wp("Bulgarian lev", "Bulgarian_lev", "1952 at 100:1 with other rates for bank accounts and prices; 1962 at 10:1"),
    "wp-atschilling": _wp("Austrian schilling", "Austrian_schilling", "1945 at 1:1 to the Reichsmark up to 150 per person; 1947 at par for the first 150, 3:1 beyond"),
    "wp-byr": _wp("Belarusian ruble", "Belarusian_ruble", "2000: 1 new ruble = 1,000 old"),
})
SOURCES.update(WORLD_SOURCES)

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
    *MORE,
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
            (1948, "Reichsmark", "Deutsche Mark", 10, "bundesbank-1948",
             "No single rate existed: wages, salaries and rents converted 1:1, each person swapped 60 RM for 40 DM (then 20 more), and bank balances converted at less than 1:10. The conventional 10:1 is used here."),
            (1999, "Deutsche Mark", "Euro", 1.95583, "ec2866", None),
        ],
        "gap": "The 1948 reform had several rates, so no single factor is exact for Reichsmark amounts; West Germany only, and the Saarland and East Germany are not covered.",
    },
    {
        "iso": "IL", "name": "Israel", "start": 1948, "unit": "new shekel",
        "steps": [
            (1952, "Palestine pound", "Israeli pound", 1, "wp-ilpound",
             "The Palestine pound stayed in use after independence. The Israeli pound replaced it on 9 June 1952 and kept its peg at par to sterling, so the change was one for one."),
            (1980, "Israeli pound", "Israeli shekel (1st)", 10, "wiki", None),
            (1986, "Shekel", "New Shekel", 1_000, "wiki",
             "The Bank of Israel dates the new shekel to 4 September 1985; the source table lists 1986."),
        ],
    },
    {
        "iso": "RO", "name": "Romania", "start": 1945, "unit": "leu",
        "steps": [
            (1947, "Romanian leu (1st)", "Romanian leu (2nd)", 20_000, "wp-roleu",
             "The \"great stabilisation\" of 15 August 1947, with caps on how much each person could convert."),
            (1952, "Romanian leu (2nd)", "Romanian leu (3rd)", 20, "wp-roleu",
             "Rates ranged from 20 to 400 old lei per new leu depending on the kind and size of holding; the most favourable, 20:1, is used here."),
            (2005, "Romanian leu (3rd)", "Romanian leu (4th)", 10_000, "wiki", None),
        ],
        "gap": "Every step is cited, but the 1952 reform had no single rate (20 to 400 old lei per new), so no one factor is exact.",
    },
    {
        "iso": "BY", "name": "Belarus (and the Soviet Union)", "start": 1945, "unit": "ruble",
        "steps": [
            (1947, "4th Soviet ruble", "5th Soviet ruble", 10, "wiki", None),
            (1961, "5th Soviet ruble", "6th Soviet ruble", 10, "wiki", None),
            (1991, "6th Soviet ruble", "7th Soviet ruble", 1, "wiki", None),
            (1994, "7th Soviet ruble", "First Belarusian ruble", 10, "wiki", None),
            (2000, "First Belarusian ruble", "Second Belarusian ruble", 1_000, "wp-byr",
             "Missing from the redenomination table, so cited from the article on the ruble itself."),
            (2016, "Second Belarusian ruble", "Third Belarusian ruble", 10_000, "wiki", None),
        ],
    },
    {
        "iso": "CD", "name": "DR Congo", "start": 1945, "unit": "franc",
        "steps": [
            (1960, "Belgian Congo franc", "First congolese franc", 1, "wp-cdfranc",
             "Independence: the same franc carried on as the Congolese franc."),
            (1967, "First congolese franc", "First zaïre", 1_000, "wiki", None),
            (1993, "First Zaïre", "Nouveau zaïre", 3_000_000, "wiki", None),
            (1998, "Nouveau zaïre", "Second Congolese franc", 100_000, "wiki", None),
        ],
    },
    {
        "iso": "GH", "name": "Ghana", "start": 1945, "unit": "cedi",
        "steps": [
            (1958, "British West African pound", "Ghanaian pound", 1, "wp-ghpound", None),
            (1965, "Ghanaian pound", "Old cedi", 1 / 2.4, "bog-gh",
             "One cedi was worth eight shillings and four pence, so a pound bought 2.4 cedis; the new unit was the smaller one."),
            (1967, "Old cedi", "Ghanaian cedi", 1.2, "wiki", None),
            (2007, "Cedi", "New Ghanaian cedi", 10_000, "wiki", None),
        ],
    },
    {
        "iso": "HR", "name": "Croatia (and Yugoslavia)", "start": 1945, "unit": "euro",
        "steps": [
            (1966, "1944 dinara", "Yugoslav 1966 dinar", 100, "wiki", None),
            (1990, "1966 dinara", "Yugoslav 1990 dinar", 10_000, "wiki", None),
            (1991, "Yugoslav 1990 dinar", "Croatian dinar", 1, "wiki", None),
            (1994, "Croatian dinar", "Croatian kuna", 1_000, "wiki", None),
            (2023, "Croatian kuna", "Euro", 7.5345, "ecb-hr", None),
        ],
    },
    {
        "iso": "BG", "name": "Bulgaria", "start": 1945, "unit": "euro",
        "steps": [
            (1952, "Bulgarian lev (2nd)", "Bulgarian lev (3rd)", 100, "wp-bglev",
             "100:1 for cash; bank accounts converted at rates from 100:3 to 200:1, and prices at 25:1."),
            (1962, "Bulgarian lev (3rd)", "Bulgarian lev (4th)", 10, "wp-bglev", None),
            (1999, "Bulgarian lev", "Bulgarian new lev", 1_000, "wiki", None),
            (2026, "Bulgarian new lev", "Euro", 1.95583, "ecb-bg", "The lev had been pegged at this rate to the mark, then the euro, since 1997."),
        ],
        "gap": "Every step is cited, but the 1952 reform converted cash, bank accounts and prices at different rates, so no one factor is exact.",
    },
]


# World Bank ISO3 code for each chain, and the year of the unit the World Bank series is
# restated in where that is not the current unit (Venezuela: the 2008 bolívar fuerte).
WORLD_BANK = {
    "HU": "HUN", "VE": "VEN", "BR": "BRA", "AR": "ARG", "TR": "TUR", "PL": "POL", "RU": "RUS",
    "UA": "UKR", "PE": "PER", "BO": "BOL", "FR": "FRA", "FI": "FIN", "GR": "GRC", "NI": "NIC",
    "RS": "SRB", "MX": "MEX", "AO": "AGO", "CL": "CHL", "UY": "URY", "DE": "DEU", "IL": "ISR",
    "RO": "ROU", "BY": "BLR", "CD": "COD", "GH": "GHA", "HR": "HRV", "BG": "BGR", "ZW": "ZWE",
}
WORLD_BANK_UNIT_YEAR = {"VE": 2008}
WORLD_BANK_UNSUPPORTED = {"ZW": "The World Bank series mixes several Zimbabwean currencies without a consistent restatement."}


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


for _a, _b in MORE_ALIASES.items():
    ALIASES[normalise(_a)] = normalise(_b)
WORLD_BANK = {**WORLD_BANK, **MORE_WORLD_BANK}


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
        # A country with no currency change since its start year cites one source for that
        # continuity ("basis"); without one it cannot be verified.
        basis = SOURCES[c["basis"]] if c.get("basis") else None
        if not steps and not basis:
            unsourced = [None]
        total_factor = 1.0
        for s in steps:
            if s["rate"]:
                total_factor *= s["rate"]
        out.append({
            "iso": c["iso"], "name": c["name"], "start": c["start"], "unit": c["unit"],
            "currency": c.get("currency") or steps[0]["old"], "basis": basis,
            "status": "verified" if not unsourced and not c.get("gap") else "partial",
            "unsourced_steps": len(unsourced),
            "gap": c.get("gap"),
            "steps": steps,
            "total_factor": total_factor,
            "wb": WORLD_BANK.get(c["iso"]),
            "wb_unit_year": WORLD_BANK_UNIT_YEAR.get(c["iso"]),
            "wb_unsupported": WORLD_BANK_UNSUPPORTED.get(c["iso"]),
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
