"""Additional country chains, built only from sources already checked:
the Wikipedia redenomination table ("wiki"), Council Regulation 2866/98
("ec2866"), and the per-currency sources listed in SOURCES in build_countries.py.

Imported by build_countries.py. Same step format:
(year, old currency, new currency, old units per new unit, source key, note).
"""

SOVIET = [
    (1947, "4th Soviet ruble", "5th Soviet ruble", 10, "wiki", None),
    (1961, "5th Soviet ruble", "6th Soviet ruble", 10, "wiki", None),
    (1991, "6th Soviet ruble", "7th Soviet ruble", 1, "wiki", None),
]
YUGOSLAV = [
    (1966, "1944 dinara", "Yugoslav 1966 dinar", 100, "wiki", None),
    (1990, "1966 dinara", "Yugoslav 1990 dinar", 10_000, "wiki", None),
]


def soviet(iso, name, unit, steps):
    return {"iso": iso, "name": f"{name} (and the Soviet Union)", "start": 1945, "unit": unit, "steps": SOVIET + steps}


def euro(iso, name, start, currency, rate, year, gap=None):
    c = {"iso": iso, "name": name, "start": start, "unit": "euro",
         "steps": [(year, currency, "Euro", rate, "ec2866", None)]}
    if gap:
        c["gap"] = gap
    return c


MORE = [
    soviet("GE", "Georgia", "lari", [
        (1993, "7th Soviet ruble", "Georgian kuponi", 1, "wiki", None),
        (1995, "Georgian kuponi", "Georgian lari", 1_000_000, "wiki", None)]),
    soviet("KZ", "Kazakhstan", "tenge", [(1993, "7th Soviet ruble", "Kazakhstani tenge", 500, "wiki", None)]),
    soviet("KG", "Kyrgyzstan", "som", [(1993, "7th Soviet ruble", "Kyrgyzstani som", 200, "wiki", None)]),
    soviet("AM", "Armenia", "dram", [(1993, "7th Soviet ruble", "Armenian dram", 200, "wiki", None)]),
    soviet("AZ", "Azerbaijan", "manat", [
        (1992, "7th Soviet ruble", "Azerbaijani manat (2nd)", 10, "wiki", None),
        (2006, "Second Azerbaijani manat", "Azerbaijani new manat", 5_000, "wiki", None)]),
    soviet("TM", "Turkmenistan", "manat", [
        (1993, "7th Soviet ruble", "Turkmenistani manat", 500, "wiki", None),
        (2009, "(old) manat", "Turkmenistani new manat", 5_000, "wiki", None)]),
    soviet("TJ", "Tajikistan", "somoni", [
        (1992, "7th Soviet ruble", "1st Russian ruble", 1, "wiki", "Tajikistan kept the Russian ruble after independence."),
        (1995, "First Russian ruble", "Tajikistani ruble", 100, "wiki", None),
        (2000, "Tajikistani ruble", "Tajikistani somoni", 1_000, "wiki", None)]),
    soviet("UZ", "Uzbekistan", "soum", [
        (1993, "7th Soviet ruble", "1st Uzbekistani soum", 1, "wiki", None),
        (1994, "1st Uzbekistani soum", "2nd Uzbekistani soum", 1_000, "wiki", None)]),
    soviet("MD", "Moldova", "leu", [
        (1992, "7th Soviet ruble", "Moldovan cupon", 1, "wiki", None),
        (1993, "Moldovan cupon", "Moldovan leu", 1_000, "wiki", None)]),
    soviet("LT", "Lithuania", "euro", [
        (1991, "7th Soviet ruble", "Talonas", 10, "wiki", None),
        (1993, "Talonas", "Lithuanian litas", 100, "wiki", None),
        (2015, "Lithuanian litas", "Euro", 3.4528, "ec2866", None)]),
    soviet("LV", "Latvia", "euro", [
        (1992, "7th Soviet rouble", "2nd Latvian rouble", 1, "wiki", None),
        (1993, "2nd Latvian rouble", "2nd Latvian lats", 200, "wiki", None),
        (2014, "2nd Latvian lats", "Euro", 0.702804, "ec2866", None)]),
    soviet("EE", "Estonia", "euro", [
        (1992, "7th Soviet ruble", "Estonian kroon", 10, "wiki", None),
        (2011, "Estonian kroon", "Euro", 15.6466, "ec2866", None)]),
    {"iso": "SI", "name": "Slovenia (and Yugoslavia)", "start": 1945, "unit": "euro", "steps": YUGOSLAV + [
        (1991, "Yugoslav 1990 dinar", "Slovenian tolar", 1, "wiki", None),
        (2007, "Slovenian tolar", "Euro", 239.64, "ec2866", None)]},
    {"iso": "MK", "name": "North Macedonia (and Yugoslavia)", "start": 1945, "unit": "denar", "steps": YUGOSLAV + [
        (1992, "Yugoslav 1990 dinar", "First Macedonian denar", 1, "wiki", None),
        (1993, "First Macedonian denar", "Second Macedonian denar", 100, "wiki", None)]},
    euro("IT", "Italy", 1945, "Italian lira", 1936.27, 1999),
    euro("ES", "Spain", 1945, "Spanish peseta", 166.386, 1999),
    euro("PT", "Portugal", 1945, "Portuguese escudo", 200.482, 1999),
    euro("NL", "Netherlands", 1945, "Dutch guilder", 2.20371, 1999),
    euro("BE", "Belgium", 1945, "Belgian franc", 40.3399, 1999),
    euro("LU", "Luxembourg", 1945, "Luxembourg franc", 40.3399, 1999),
    euro("IE", "Ireland", 1945, "Irish pound", 0.787564, 1999),
    {"iso": "AT", "name": "Austria", "start": 1945, "unit": "euro", "steps": [
        (1945, "Reichsmark", "Austrian schilling", 1, "wp-atschilling",
         "1:1, but only up to 150 per person. In 1947 old schilling notes were exchanged at par for the first 150 and at 3:1 beyond."),
        (1999, "Austrian schilling", "Euro", 13.7603, "ec2866", None)],
     "gap": "Every step is cited, but the 1945 and 1947 exchanges were capped per person with worse rates above the cap, so the factor holds only for small amounts."},
    euro("CY", "Cyprus", 1960, "Cyprus pound", 0.585274, 2008),
    {"iso": "MT", "name": "Malta", "start": 1945, "unit": "euro", "steps": [
        (1972, "Maltese pound", "Maltese lira", 1, "wp-mtlira",
         "Not a redenomination: the pound, kept at exactly one pound sterling until 1971, was decimalised in May 1972 and later called the lira."),
        (2008, "Maltese lira", "Euro", 0.4293, "ec2866", None)]},
    {"iso": "SK", "name": "Slovakia (and Czechoslovakia)", "start": 1945, "unit": "euro", "steps": [
        (1953, "Czechoslovak koruna", "Czechoslovak koruna (1953)", 5, "wp-csk",
         "5 old for 1 new on the first 1,500 korunas per person, 50 for 1 on the rest. The 5:1 rate is used here."),
        (1993, "Czechoslovak koruna (1953)", "Slovak koruna", 1, "wp-csk", "The split of 8 February 1993, at par."),
        (2009, "Slovak koruna", "Euro", 30.126, "ec2866", None)],
     "gap": "Every step is cited, but the 1953 reform used two rates (5:1 up to a limit, 50:1 beyond), so the factor holds only for small amounts."},
    {"iso": "ID", "name": "Indonesia", "start": 1949, "unit": "rupiah", "steps": [
        (1965, "First rupiah", "Rupiah (new)", 1_000, "wiki", None)]},
    {"iso": "KR", "name": "South Korea", "start": 1945, "unit": "won", "steps": [
        (1954, "first South Korean won", "South Korean hwan", 100, "wiki", None),
        (1963, "South Korean hwan", "South Korean won (2nd)", 10, "wiki", None)]},
    {"iso": "TW", "name": "Taiwan", "start": 1946, "unit": "New Taiwan dollar", "steps": [
        (1949, "Taiwan dollars", "New Taiwan dollar", 40_000, "wiki", None)]},
    {"iso": "CN", "name": "China", "start": 1948, "unit": "renminbi yuan", "steps": [
        (1955, "First Renminbi yuan", "Second Renminbi yuan", 10_000, "wiki", None)]},
    {"iso": "IS", "name": "Iceland", "start": 1945, "unit": "króna", "steps": [
        (1981, "Icelandic króna", "Icelandic króna", 100, "wiki", None)]},
    {"iso": "MZ", "name": "Mozambique", "start": 1945, "unit": "metical", "steps": [
        (1980, "Mozambican escudo", "(old) meticais", 1, "wp-mzescudo", None),
        (2006, "(old) meticais", "New Mozambican metical", 1_000, "wiki", None)]},
    {"iso": "ZM", "name": "Zambia", "start": 1945, "unit": "kwacha", "steps": [
        (1955, "Southern Rhodesian pound", "Rhodesia and Nyasaland pound", 1, "wp-rnpound",
         "Northern Rhodesia used the Southern Rhodesian pound until the federation's own pound replaced it."),
        (1964, "Rhodesia and Nyasaland pound", "Zambian pound", 1, "wp-zmpound", None),
        (1968, "Zambian pound", "(old) Kwacha", 0.5, "wp-zmpound", "Decimalisation: two kwacha to the pound."),
        (2013, "(old) Kwacha", "Zambian kwacha", 1_000, "wiki", None)]},
    {"iso": "SD", "name": "Sudan", "start": 1945, "unit": "pound", "steps": [
        (1956, "Egyptian pound", "First Sudanese pounds", 1, "wp-sdpound", "Created when Anglo-Egyptian rule ended on 1 January 1956; the first notes followed in April 1957."),
        (1992, "First Sudanese pounds", "Sudanese dinar", 10, "wiki", None),
        (2007, "Sudanese dinars", "Second Sudanese pound", 100, "wiki", None)]},
    {"iso": "UG", "name": "Uganda", "start": 1945, "unit": "shilling", "steps": [
        (1966, "East African shilling", "First Ugandan shilling", 1, "wiki", None),
        (1987, "First Ugandan shilling", "Second Ugandan shilling", 100, "wiki", None)]},
    {"iso": "SR", "name": "Suriname", "start": 1945, "unit": "dollar", "steps": [
        (2004, "Surinamese guilder", "Surinamese dollar", 1_000, "wiki", None)]},
    {"iso": "SL", "name": "Sierra Leone", "start": 1945, "unit": "leone", "steps": [
        (1964, "British West African pound", "(old) Sierra Leonean leone", 0.5, "wp-leone",
         "Two leones to the pound; the new unit was the smaller one."),
        (2021, "(old) Sierra Leonean leone", "Sierra Leonean leone", 1_000, "wiki", None)]},
    {"iso": "ST", "name": "São Tomé and Príncipe", "start": 1945, "unit": "dobra", "steps": [
        (1977, "São Tomé and Príncipe escudo", "São Tomé and Príncipe dobra (1st)", 1, "wp-stescudo", None),
        (2018, "São Tomé and Príncipe dobra (1st)", "São Tomé and Príncipe dobra (2nd)", 1_000, "wiki", None)]},
    {"iso": "MR", "name": "Mauritania", "start": 1960, "unit": "ouguiya", "steps": [
        (1973, "CFA franc", "Ouguiya", 5, "wiki", None),
        (2018, "First Mauritanian ouguiya", "Second Mauritanian ouguiya", 10, "wiki", None)]},
    {"iso": "MG", "name": "Madagascar", "start": 1945, "unit": "ariary", "steps": [
        (2005, "Franc malgache", "Ariary", 5, "wiki", None)]},
    {"iso": "EC", "name": "Ecuador", "start": 1945, "unit": "US dollar", "steps": [
        (2000, "Sucre", "United States dollar", 25_000, "wiki", "Dollarised; the sucre was withdrawn.")]},
    {"iso": "SV", "name": "El Salvador", "start": 1945, "unit": "US dollar", "steps": [
        (2001, "Colón", "United States dollar", 8.75, "wiki", "Dollarised; the colón was withdrawn.")]},
    {"iso": "GN", "name": "Guinea", "start": 1945, "unit": "franc", "steps": [
        (1959, "CFA franc", "First Guinean franc", 1, "wiki", None),
        (1971, "Guinean franc (1st)", "Guinean syli", 10, "wiki", None),
        (1985, "Syli", "Franc guinéen", 1, "wiki", None)]},
    {"iso": "ML", "name": "Mali", "start": 1945, "unit": "CFA franc", "steps": [
        (1962, "CFA franc", "Franc malien", 1, "wiki", None),
        (1984, "Franc malien", "CFA franc", 2, "wiki", None)]},
    {"iso": "GQ", "name": "Equatorial Guinea", "start": 1945, "unit": "CFA franc", "steps": [
        (1969, "Spanish peseta", "Peseta guineana", 1, "wiki", None),
        (1975, "Peseta guineana", "Ekwele", 1, "wiki", None),
        (1985, "Ekwele", "CFA franc", 4, "wiki", None)]},
    {"iso": "GW", "name": "Guinea-Bissau", "start": 1945, "unit": "CFA franc", "steps": [
        (1975, "Portuguese Guinean escudo", "Guinea-Bissau peso", 1, "wiki", None),
        (1997, "Guinea-Bissau peso", "CFA franc", 65, "wiki", None)]},
]

MORE += [
    {"iso": "VN", "name": "Vietnam (from South Vietnam)", "start": 1955, "unit": "đồng", "steps": [
        (1975, "Đồng", "Liberation đồng", 500, "wiki", "The South Vietnamese đồng after the fall of Saigon."),
        (1978, "Liberation đồng", "Đồng (unified)", 0.8, "wiki", "Unification of the two Vietnamese currencies; the new unit was the larger one. A northern đồng converted one for one."),
        (1985, "Đồng (unified)", "Đồng (1985)", 10, "wp-vnd", "14 September 1985: one new đồng for ten old. Missing from the redenomination table, so cited from the article on the đồng.")]},
    {"iso": "TL", "name": "Timor-Leste", "start": 1976, "unit": "US dollar", "steps": [
        (1999, "Indonesian rupiah", "United States dollar", 6900, "wiki", "An approximate market rate at the time, as the source gives it; the dollar was adopted by the UN administration in 2000 and there was no fixed conversion.")],
     "gap": "The rupiah-to-dollar figure is approximate, not a fixed legal rate; the Portuguese Timor escudo before 1976 is not covered."},
]

MORE_ALIASES = {
    "Second Azerbaijani manat": "Azerbaijani manat (2nd)",
    "(old) manat": "Turkmenistani manat",
    "Sudanese dinars": "Sudanese dinar",
    "Syli": "Guinean syli",
    "First Mauritanian ouguiya": "Ouguiya",
    "7th Soviet rouble": "7th Soviet ruble",
    "First Guinean franc": "Guinean franc (1st)",
}

MORE_WORLD_BANK = {
    "GE": "GEO", "KZ": "KAZ", "KG": "KGZ", "AM": "ARM", "AZ": "AZE", "TM": "TKM", "TJ": "TJK",
    "UZ": "UZB", "MD": "MDA", "LT": "LTU", "LV": "LVA", "EE": "EST", "SI": "SVN", "MK": "MKD",
    "IT": "ITA", "ES": "ESP", "PT": "PRT", "NL": "NLD", "BE": "BEL", "LU": "LUX", "IE": "IRL",
    "AT": "AUT", "CY": "CYP", "MT": "MLT", "SK": "SVK", "ID": "IDN", "KR": "KOR", "TW": None,
    "CN": "CHN", "IS": "ISL", "MZ": "MOZ", "ZM": "ZMB", "SD": "SDN", "UG": "UGA", "SR": "SUR",
    "SL": "SLE", "ST": "STP", "MR": "MRT", "MG": "MDG", "EC": "ECU", "SV": "SLV", "GN": "GIN",
    "ML": "MLI", "GQ": "GNQ", "GW": "GNB", "VN": "VNM", "TL": "TLS",
}

MORE_UNITS = {
    "GE": "GEL", "KZ": "KZT", "KG": "KGS", "AM": "AMD", "AZ": "AZN", "TM": "TMT", "TJ": "TJS",
    "UZ": "UZS", "MD": "MDL", "LT": "EUR", "LV": "EUR", "EE": "EUR", "SI": "EUR", "MK": "MKD",
    "IT": "EUR", "ES": "EUR", "PT": "EUR", "NL": "EUR", "BE": "EUR", "LU": "EUR", "IE": "EUR",
    "AT": "EUR", "CY": "EUR", "MT": "EUR", "SK": "EUR", "ID": "IDR", "KR": "KRW", "TW": "TWD",
    "CN": "CNY", "IS": "ISK", "MZ": "MZN", "ZM": "ZMW", "SD": "SDG", "UG": "UGX", "SR": "SRD",
    "SL": "SLE", "ST": "STN", "MR": "MRU", "MG": "MGA", "EC": "USD", "SV": "USD", "GN": "GNF",
    "ML": "XOF", "GQ": "XAF", "GW": "XOF", "VN": "VND", "TL": "USD",
}

# Countries outside the redenomination table (see countries_world.py).
from countries_world import WORLD, WORLD_ALIASES, WORLD_UNITS, WORLD_WORLD_BANK  # noqa: E402

MORE += WORLD
MORE_ALIASES.update(WORLD_ALIASES)
MORE_UNITS.update(WORLD_UNITS)
MORE_WORLD_BANK.update(WORLD_WORLD_BANK)
