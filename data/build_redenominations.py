"""Builds data/redenominations.json from the source table.

Every row below is transcribed from the table "This table lists various
currency redenominations" in the Wikipedia article "Redenomination"
(https://en.wikipedia.org/wiki/Redenomination), read on 30 October 2026.
`rate` is old units per one new unit, as the table prints it. "At par" is 1.
An approximate rate in the source is kept as a string prefixed with "~".

Run:  python3 data/build_redenominations.py
"""

from __future__ import annotations

import json
from pathlib import Path

SOURCE = {
    "title": "Redenomination — Wikipedia",
    "url": "https://en.wikipedia.org/wiki/Redenomination",
    "accessed": "2026-10-30",
}

# (country, year, old currency, new currency, rate)
ROWS = [
    ("Hungary", 1946, "Hungarian pengő", "Hungarian forint", 4e29),
    ("Germany", 1923, "Papiermark", "Rentenmark", 1e12),
    ("Zimbabwe", 2009, "Zimbabwean dollar (3rd)", "Zimbabwean dollar (4th)", 1e12),
    ("Greece", 1944, "Greek drachma (1st)", "Greek drachma (2nd)", 50_000_000_000),
    ("Zimbabwe", 2008, "Zimbabwean dollar (2nd)", "Zimbabwean dollar (3rd)", 10_000_000_000),
    ("Yugoslavia", 1994, "1993 dinara", "Yugoslav 1994 dinar", 1_000_000_000),
    ("Republic of Serbian Krajina", 1994, "2nd Krajina dinar", "3rd Krajina dinar", 1_000_000_000),
    ("China (Republic of China)", 1949, "\"gold\" yuan", "Chinese \"silver\" yuan", 500_000_000),
    ("Hungary", 1946, "Hungarian adópengő", "Hungarian forint", 200_000_000),
    ("Yugoslavia", 1994, "1994 dinara", "Yugoslav novi dinar", 13_000_000),
    ("Nicaragua", 1991, "Nicaraguan córdoba (2nd)", "Nicaraguan córdoba (oro, 3rd)", 5_000_000),
    ("China (Republic of China)", 1948, "(old) yuan", "Chinese \"gold\" yuan", 3_000_000),
    ("DR Congo", 1993, "First Zaïre", "Nouveau zaïre", 3_000_000),
    ("Poland", 1924, "Polish marka", "Polish złoty (2nd)", 1_800_000),
    ("Bolivia", 1985, "Peso boliviano", "Boliviano", 1_000_000),
    ("Peru", 1991, "Peruvian inti", "Peruvian nuevo sol", 1_000_000),
    ("Yugoslavia", 1993, "1992 dinara", "Yugoslav 1993 dinar", 1_000_000),
    ("Republic of Serbian Krajina", 1993, "1st Krajina dinar", "2nd Krajina dinar", 1_000_000),
    ("Georgia", 1995, "Georgian kuponi", "Georgian lari", 1_000_000),
    ("Angola", 1999, "Kwanza reajustado", "Second Kwanza", 1_000_000),
    ("Transnistria", 2001, "Transnistrian ruble (2nd)", "Transnistrian ruble (3rd)", 1_000_000),
    ("Turkey", 2005, "Turkish lira", "Turkish new lira", 1_000_000),
    ("Venezuela", 2021, "Venezuelan bolívar (3rd)", "Venezuelan bolívar (4th)", 1_000_000),
    ("Ukraine", 1996, "3rd Ukrainian karbovanets", "Hryvnia", 100_000),
    ("DR Congo", 1998, "Nouveau zaïre", "Second Congolese franc", 100_000),
    ("Venezuela", 2018, "Bolivar Fuerte", "Bolívar Soberano", 100_000),
    ("Soviet Union", 1924, "3rd Soviet ruble", "4th Soviet ruble", 50_000),
    ("Taiwan (Republic of China)", 1949, "Taiwan dollars", "New Taiwan dollar", 40_000),
    ("Ecuador", 2000, "Sucre", "United States dollar", 25_000),
    ("Hungary", 1927, "Hungarian korona", "Hungarian pengő", 12_500),
    ("Soviet Union", 1922, "1st Soviet ruble", "2nd Soviet ruble", 10_000),
    ("Austria", 1925, "Austrian krone", "Austrian schilling", 10_000),
    ("China (People's Republic of China)", 1955, "First Renminbi yuan", "Second Renminbi yuan", 10_000),
    ("Argentina", 1983, "Peso ley", "Peso argentino", 10_000),
    ("Yugoslavia", 1990, "1966 dinara", "Yugoslav 1990 dinar", 10_000),
    ("Argentina", 1992, "Austral", "Peso (convertible)", 10_000),
    ("Poland", 1995, "3rd Polish złoty", "4th Polish złoty", 10_000),
    ("Romania", 2005, "Romanian leu (3rd)", "Romanian leu (4th)", 10_000),
    ("Ghana", 2007, "Cedi", "New Ghanaian cedi", 10_000),
    ("Belarus", 2016, "Second Belarusian ruble", "Third Belarusian ruble", 10_000),
    ("UN Transitional Administration in East Timor", 1999, "Indonesian rupiah", "United States dollar", "~6900"),
    ("Azerbaijan", 2006, "Second Azerbaijani manat", "Azerbaijani new manat", 5_000),
    ("Turkmenistan", 2009, "(old) manat", "Turkmenistani new manat", 5_000),
    ("Brazil", 1994, "Cruzeiro real", "Real", 2_750),
    ("Brazil", 1942, "Real (old)", "Cruzeiro (antigo)", 1_000),
    ("Greece", 1954, "Greek drachma (2nd)", "Greek drachma (3rd)", 1_000),
    ("Chile", 1960, "First Chilean peso", "Chilean escudo", 1_000),
    ("Bolivia", 1963, "First boliviano", "Peso boliviano", 1_000),
    ("Indonesia", 1965, "First rupiah", "Rupiah (new)", 1_000),
    ("Brazil", 1967, "Cruzeiro (antigo)", "Cruzeiro (novo)", 1_000),
    ("DR Congo", 1967, "First congolese franc", "First zaïre", 1_000),
    ("Uruguay", 1973, "Peso moneda nacional", "Nuevo peso", 1_000),
    ("Chile", 1975, "Chilean escudo", "Chilean peso", 1_000),
    ("Argentina", 1985, "Argentine peso (1983)", "Argentine austral", 1_000),
    ("Peru", 1985, "Peruvian sol (1863)", "Peruvian inti", 1_000),
    ("Brazil", 1986, "Cruzeiro (novo)", "Cruzado", 1_000),
    ("Israel", 1986, "Shekel", "New Shekel", 1_000),
    ("Nicaragua", 1988, "Nicaraguan córdoba (1st)", "Nicaraguan córdoba (2nd)", 1_000),
    ("Brazil", 1989, "Cruzado", "Cruzado Novo", 1_000),
    ("Brazil", 1993, "Cruzeiro (third)", "Cruzeiro real", 1_000),
    ("Mexico", 1993, "Peso mexicano", "Nuevo peso mexicano", 1_000),
    ("Moldova", 1993, "Moldovan cupon", "Moldovan leu", 1_000),
    ("Uruguay", 1993, "Nuevo peso", "Peso uruguayo", 1_000),
    ("Croatia", 1994, "Croatian dinar", "Croatian kuna", 1_000),
    ("Uzbekistan", 1994, "1st Uzbekistani soum", "2nd Uzbekistani soum", 1_000),
    ("Angola", 1995, "Novo kwanza", "Kwanza reajustado", 1_000),
    ("Russia", 1998, "First Russian ruble", "Second Russian ruble", 1_000),
    ("Bulgaria", 1999, "Bulgarian lev", "Bulgarian new lev", 1_000),
    ("Tajikistan", 2000, "Tajikistani ruble", "Tajikistani somoni", 1_000),
    ("Suriname", 2004, "Surinamese guilder", "Surinamese dollar", 1_000),
    ("Mozambique", 2006, "(old) meticais", "New Mozambican metical", 1_000),
    ("Zimbabwe", 2006, "Zimbabwean dollar (1st)", "Zimbabwean dollar (2nd)", 1_000),
    ("Sudan", 2007, "First Sudanese pounds", "Second Sudanese pound", 1_000),
    ("Venezuela", 2008, "(old) Bolivar", "Bolivar Fuerte", 1_000),
    ("Zambia", 2013, "(old) Kwacha", "Zambian kwacha", 1_000),
    ("São Tomé and Príncipe", 2018, "São Tomé and Príncipe dobra (1st)", "São Tomé and Príncipe dobra (2nd)", 1_000),
    ("Sierra Leone", 2021, "(old) Sierra Leonean leone", "Sierra Leonean leone", 1_000),
    ("South Vietnam", 1975, "Đồng", "Liberation đồng", 500),
    ("Turkmenistan", 1993, "7th Soviet ruble", "Turkmenistani manat", 500),
    ("Kazakhstan", 1993, "7th Soviet ruble", "Kazakhstani tenge", 500),
    ("Haiti", 1872, "2nd Haitian gourde", "3rd Haitian gourde", 300),
    ("Latvia", 1993, "2nd Latvian rouble", "2nd Latvian lats", 200),
    ("Kyrgyzstan", 1993, "7th Soviet ruble", "Kyrgyzstani som", 200),
    ("Armenia", 1993, "7th Soviet ruble", "Armenian dram", 200),
    ("Soviet Union", 1923, "2nd Soviet ruble", "3rd Soviet ruble", 100),
    ("Poland", 1949, "2nd Polish złoty", "3rd Polish złoty", 100),
    ("Republic of Korea", 1954, "first South Korean won", "South Korean hwan", 100),
    ("France", 1960, "French Franc", "New French Franc", 100),
    ("Finland", 1963, "Finnish markka", "New Finnish markka", 100),
    ("Yugoslavia", 1966, "1944 dinara", "Yugoslav 1966 dinar", 100),
    ("Argentina", 1970, "Peso moneda nacional", "Peso ley", 100),
    ("Iceland", 1981, "Icelandic króna", "Icelandic króna", 100),
    ("Uganda", 1987, "First Ugandan shilling", "Second Ugandan shilling", 100),
    ("Lithuania", 1993, "Talonas", "Lithuanian litas", 100),
    ("North Macedonia", 1993, "First Macedonian denar", "Second Macedonian denar", 100),
    ("Tajikistan", 1995, "First Russian ruble", "Tajikistani ruble", 100),
    ("Sudan", 2007, "Sudanese dinars", "Second Sudanese pound", 100),
    ("North Korea", 2009, "North Korean won (1st)", "North Korean won (2nd)", 100),
    ("Guinea-Bissau", 1997, "Guinea-Bissau peso", "CFA franc", 65),
    ("Guatemala", 1925, "Guatemalan peso", "Guatemalan quetzal", 60),
    ("Latvia", 1922, "1st Latvian rouble", "1st Latvian lats", 50),
    ("Yugoslavia", 1944, "Independent State of Croatia kuna", "Yugoslav 1944 dinar", 40),
    ("Argentina", 1881, "Peso moneda corriente", "Peso moneda nacional", 25),
    ("Yugoslavia", 1944, "Serbian 1941 dinar", "Yugoslav 1944 dinar", 20),
    ("Nicaragua", 1912, "Nicaraguan peso", "Nicaraguan córdoba (1st)", 12.5),
    ("Haiti", 1870, "1st Haitian gourde", "2nd Haitian gourde", 10),
    ("Soviet Union", 1947, "4th Soviet ruble", "5th Soviet ruble", 10),
    ("Soviet Union", 1961, "5th Soviet ruble", "6th Soviet ruble", 10),
    ("Republic of Korea", 1963, "South Korean hwan", "South Korean won (2nd)", 10),
    ("Guinea", 1971, "Guinean franc (1st)", "Guinean syli", 10),
    ("Israel", 1980, "Israeli pound", "Israeli shekel (1st)", 10),
    ("Lithuania", 1991, "7th Soviet ruble", "Talonas", 10),
    ("Estonia", 1992, "7th Soviet ruble", "Estonian kroon", 10),
    ("Azerbaijan", 1992, "7th Soviet ruble", "Azerbaijani manat (2nd)", 10),
    ("Sudan", 1992, "First Sudanese pounds", "Sudanese dinar", 10),
    ("Yugoslavia", 1992, "1990 dinara", "Yugoslav 1992 dinar", 10),
    ("Belarus", 1994, "7th Soviet ruble", "First Belarusian ruble", 10),
    ("Mauritania", 2018, "First Mauritanian ouguiya", "Second Mauritanian ouguiya", 10),
    ("El Salvador", 2001, "Colón", "United States dollar", 8.75),
    ("Haiti", 1813, "Haitian livre", "1st Haitian gourde", 8.25),
    ("Argentina", 1826, "Real", "Peso moneda corriente", 8),
    ("Mauritania", 1973, "CFA franc", "Ouguiya", 5),
    ("Madagascar", 2005, "Franc malgache", "Ariary", 5),
    ("Equatorial Guinea", 1985, "Ekwele", "CFA franc", 4),
    ("Mali", 1984, "Franc malien", "CFA franc", 2),
    ("Ghana", 1967, "Old cedi", "Ghanaian cedi", 1.2),
    ("Hungary", 1919, "Austro-Hungarian krone", "Hungarian korona", 1),
    ("Austria", 1920, "Austro-Hungarian krone", "Austrian krone", 1),
    ("Mongolia", 1925, "4th Soviet ruble", "Mongolian tögrög", 1),
    ("Guinea", 1959, "CFA franc", "First Guinean franc", 1),
    ("Mali", 1962, "CFA franc", "Franc malien", 1),
    ("Uganda", 1966, "East African shilling", "First Ugandan shilling", 1),
    ("Equatorial Guinea", 1969, "Spanish peseta", "Peseta guineana", 1),
    ("Angola", 1975, "Second Angolan escudo", "First Kwanza", 1),
    ("Equatorial Guinea", 1975, "Peseta guineana", "Ekwele", 1),
    ("Guinea-Bissau", 1975, "Portuguese Guinean escudo", "Guinea-Bissau peso", 1),
    ("Guinea", 1985, "Syli", "Franc guinéen", 1),
    ("Angola", 1990, "First Kwanza", "Novo kwanza", 1),
    ("Brazil", 1990, "Cruzado Novo", "Cruzeiro (third)", 1),
    ("Soviet Union", 1991, "6th Soviet ruble", "7th Soviet ruble", 1),
    ("Croatia", 1991, "Yugoslav 1990 dinar", "Croatian dinar", 1),
    ("Slovenia", 1991, "Yugoslav 1990 dinar", "Slovenian tolar", 1),
    ("Latvia", 1992, "7th Soviet rouble", "2nd Latvian rouble", 1),
    ("Moldova", 1992, "7th Soviet ruble", "Moldovan cupon", 1),
    ("Republic of Serbian Krajina", 1992, "Yugoslav 1992 dinar", "1st Krajina dinar", 1),
    ("Russia", 1992, "7th Soviet ruble", "1st Russian ruble", 1),
    ("North Macedonia", 1992, "Yugoslav 1990 dinar", "First Macedonian denar", 1),
    ("Ukraine", 1992, "7th Soviet ruble", "3rd Ukrainian karbovanets", 1),
    ("Georgia", 1993, "7th Soviet ruble", "Georgian kuponi", 1),
    ("Uzbekistan", 1993, "7th Soviet ruble", "1st Uzbekistani soum", 1),
    ("South Vietnam", 1978, "Liberation đồng", "Đồng (unified)", 0.8),
    ("Austria-Hungary", 1892, "Austro-Hungarian florin", "Austro-Hungarian krone", 0.5),
    ("Iran", 1932, "Iranian Toman", "Iranian Rial", 0.1),
]


def main() -> None:
    rows = []
    for country, year, old, new, rate in ROWS:
        approx = isinstance(rate, str)
        value = float(rate.lstrip("~")) if approx else float(rate)
        rows.append({
            "country": country, "year": year, "old": old, "new": new,
            "rate": value, "approximate": approx, "at_par": value == 1.0,
            "source": SOURCE,
        })
    rows.sort(key=lambda r: (r["year"], r["country"]))
    out = Path(__file__).with_name("redenominations.json")
    out.write_text(json.dumps({"source": SOURCE, "count": len(rows), "rows": rows}, ensure_ascii=False, indent=1))
    print(f"wrote {out} with {len(rows)} rows ({sum(r['year'] >= 1945 for r in rows)} from 1945 on)")


if __name__ == "__main__":
    main()
