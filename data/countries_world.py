"""Chains for countries outside the redenomination table: currency changes
since 1945 that did not strike zeros (pound to decimal dollar at 2:1, colonial
currency to national currency at par), plus countries whose currency has not
changed at all. Every step cites the article on the currency in question.

Imported by countries_more.py. Same step format as build_countries.py:
(year, old currency, new currency, old units per new unit, source key, note).
A country with no steps names its currency and cites a "basis" source for it.
"""


def _wp(page: str, says: str) -> dict:
    title = page.replace("_", " ").replace("%27", "'")
    return {"title": f"{title} — Wikipedia ({says})",
            "url": f"https://en.wikipedia.org/wiki/{page}", "accessed": "2026-10-30"}


WORLD_SOURCES = {
    "wp-decimal-day": _wp("Decimal_Day", "1971: the pound was retained, divided into 100 new pence"),
    "wp-aud": _wp("Australian_dollar", "1966: two dollars to the pound"),
    "wp-nzd": _wp("New_Zealand_dollar", "1967: two dollars to one pound"),
    "wp-zar": _wp("South_African_rand", "1961: 2 rand to 1 pound"),
    "wp-zapound": _wp("South_African_pound", "currency of South Africa from 1910"),
    "wp-bwapound": _wp("British_West_African_pound", "table of successor currencies, each at a conversion of 1"),
    "wp-ngn": _wp("Nigerian_naira", "1 January 1973: £1 = ₦2"),
    "wp-kes": _wp("Kenyan_shilling", "replaced the East African shilling in 1966 at par"),
    "wp-tzs": _wp("Tanzanian_shilling", "replaced the East African shilling on 14 June 1966 at par"),
    "wp-jmd": _wp("Jamaican_dollar", "1969: a dollar worth 10 shillings replaced the pound"),
    "wp-mwpound": _wp("Malawian_pound", "Southern Rhodesian pound from 1932; kwacha in 1971 at 2 to the pound"),
    "wp-rnpound2": _wp("Rhodesia_and_Nyasaland_pound", "replaced the Southern Rhodesian pound at par; successor pounds at par"),
    "wp-gmpound": _wp("Gambian_pound", "own currency issued 5 October 1964"),
    "wp-gmd": _wp("Gambian_dalasi", "1971: 5 dalasis to the pound"),
    "wp-irr": _wp("Iranian_toman", "rial since 1932; a new rial of 10,000 old approved in 2025"),
    "wp-afn": _wp("Afghan_afghani", "2002: 1,000 old afghanis per new, 2,000 for Dostum issues"),
    "wp-khr": _wp("Cambodian_riel", "1953 at par with the piastre; abolished 1975; re-established 20 March 1980"),
    "wp-lak": _wp("Lao_kip", "1953 at par with the piastre; 1976 at 20:1; 1979 at 100:1"),
    "wp-usd": _wp("United_States_dollar", "the dollar has been the base unit since the Coinage Act of 1792"),
    "wp-cad": _wp("Canadian_dollar", "the Uniform Currency Act of 1871"),
    "wp-cop": _wp("Colombian_peso", "the current peso since 1837; a 2018 plan to drop three zeros was not adopted"),
    "wp-pyg": _wp("Paraguayan_guaran%C3%AD", "created 1943, first issued 1944; a 2011 plan for a new guaraní is suspended"),
    "wp-dop": _wp("Dominican_peso", "peso oro at par with the US dollar from 1937; the dollar used alongside it until 1947"),
    "wp-gtq": _wp("Guatemalan_quetzal", "introduced in 1925"),
    "wp-crc": _wp("Costa_Rican_col%C3%B3n", "introduced in 1896"),
    "wp-chf": _wp("Swiss_franc", "the franc as the monetary unit since 1850"),
    "wp-sek": _wp("Swedish_krona", "introduced 1873 with the Scandinavian Monetary Union"),
    "wp-nok": _wp("Norwegian_krone", "introduced in 1875"),
    "wp-dkk": _wp("Danish_krone", "introduced as the currency of Denmark in January 1875"),
    "wp-bmk": _wp("Bohemian_and_Moravian_koruna", "replaced by the reconstituted Czechoslovak koruna at par"),
    "wp-csk2": _wp("Czechoslovak_koruna", "1953: 5:1 up to 1,500 korunas, 50:1 beyond; 1993 split at par"),
    "wp-mad": _wp("Moroccan_dirham", "1960: 1 dirham = 100 francs"),
    "wp-tnd": _wp("Tunisian_dinar", "unit of account 1958, issued 1960, at 1,000 francs"),
    "wp-dzf": _wp("Algerian_franc", "1960: 100 old francs = 1 new franc"),
    "wp-dzd": _wp("Algerian_dinar", "1 April 1964, replacing the new franc at par"),
    "wp-etb": _wp("Ethiopian_birr", "reintroduced 23 July 1945 at 1 birr per 2 East African shillings"),
    "wp-xaf": _wp("CFA_franc", "created 26 December 1945"),
    "wp-inr": _wp("History_of_the_rupee", "1957 decimalisation: the rupee kept its value, divided into 100 paisa"),
    "wp-pkr": _wp("Pakistani_rupee", "Indian and Pakistani rupees at parity; Indian notes supplied until 30 June 1948"),
    "wp-bdt": _wp("Bangladeshi_taka", "4 March 1972: the taka replaced the Pakistani rupee at par"),
    "boj-newyen": {"title": "Bank of Japan, \"Why do we use the yen?\" (the 1946 conversion to the \"new yen\", a forced exchange of notes in the same unit)",
                   "url": "https://www.boj.or.jp/en/announcements/education/oshiete/money/c07.htm", "accessed": "2026-10-30"},
    "ph-eo25": {"title": "Executive Order No. 25, 18 November 1944 (Japanese-issued money not legal tender; pre-war Philippine Treasury certificates and coins continue as legal tender)",
                "url": "https://batasnatin.com/laws/eo-25-6", "accessed": "2026-10-30"},
    "wp-thb": _wp("Thai_baht", "the baht since before 1945, with no change of unit"),
    "wp-mbbd": _wp("Malaya_and_British_Borneo_dollar", "1953: replaced the Malayan dollar at par; 1967: replaced at par by the ringgit and the Singapore dollar"),
    "wp-lkr": _wp("Sri_Lankan_rupee", "known until 1972 as the Ceylon rupee"),
    "wp-mmk": _wp("Myanmar_kyat", "introduced 1 July 1952, replacing the rupee at par"),
    "wp-iqd": _wp("Iraqi_dinar", "the dinar since 1932; in 2003–04 notes were exchanged at par, except the older Swiss dinar notes still used in the Kurdish north, at 150 new dinars each"),
    "wp-sar": _wp("Saudi_riyal", "the riyal since before 1945; only its subdivisions changed"),
    "wp-egp": _wp("Egyptian_pound", "the pound since before 1945"),
    "wp-npr": _wp("Nepalese_rupee", "the rupee since 1932; the Indian rupee ceased to be legal tender in Nepal in 1966"),
    "wp-mnt": _wp("Mongolian_t%C3%B6gr%C3%B6g", "introduced 9 December 1925"),
    "wp-krwyen": _wp("Korean_yen", "replaced at par by the North Korean won"),
    "wp-kpw": _wp("North_Korean_won", "1959: new won equal to 100 old; 2009: 100 to 1, with exchange limits"),
}

WORLD = [
    {"iso": "GB", "name": "United Kingdom", "start": 1945, "unit": "pound", "currency": "Pound sterling",
     "steps": [], "basis": "wp-decimal-day"},
    {"iso": "AU", "name": "Australia", "start": 1945, "unit": "dollar", "steps": [
        (1966, "Australian pound", "Australian dollar", 0.5, "wp-aud", "Decimalisation: two dollars to the pound.")]},
    {"iso": "NZ", "name": "New Zealand", "start": 1945, "unit": "dollar", "steps": [
        (1967, "New Zealand pound", "New Zealand dollar", 0.5, "wp-nzd", "Decimalisation: two dollars to the pound.")]},
    {"iso": "ZA", "name": "South Africa", "start": 1945, "unit": "rand", "steps": [
        (1961, "South African pound", "South African rand", 0.5, "wp-zar", "Decimalisation: two rand to the pound.")]},
    {"iso": "NG", "name": "Nigeria", "start": 1945, "unit": "naira", "steps": [
        (1958, "British West African pound", "Nigerian pound", 1, "wp-bwapound", None),
        (1973, "Nigerian pound", "Nigerian naira", 0.5, "wp-ngn", "Decimalisation: two naira to the pound.")]},
    {"iso": "KE", "name": "Kenya", "start": 1945, "unit": "shilling", "steps": [
        (1966, "East African shilling", "Kenyan shilling", 1, "wp-kes", None)]},
    {"iso": "TZ", "name": "Tanzania", "start": 1945, "unit": "shilling", "steps": [
        (1966, "East African shilling", "Tanzanian shilling", 1, "wp-tzs", None)]},
    {"iso": "JM", "name": "Jamaica", "start": 1945, "unit": "dollar", "steps": [
        (1969, "Jamaican pound", "Jamaican dollar", 0.5, "wp-jmd", "Decimalisation: a dollar worth ten shillings, so two to the pound.")]},
    {"iso": "MW", "name": "Malawi", "start": 1945, "unit": "kwacha", "steps": [
        (1955, "Southern Rhodesian pound", "Rhodesia and Nyasaland pound", 1, "wp-rnpound2",
         "Nyasaland had used the Southern Rhodesian pound since 1932."),
        (1964, "Rhodesia and Nyasaland pound", "Malawian pound", 1, "wp-rnpound2", None),
        (1971, "Malawian pound", "Malawian kwacha", 0.5, "wp-mwpound", "Decimalisation: two kwacha to the pound.")]},
    {"iso": "GM", "name": "The Gambia", "start": 1945, "unit": "dalasi", "steps": [
        (1964, "British West African pound", "Gambian pound", 1, "wp-bwapound",
         "The Gambian pound was issued on 5 October 1964; the West African pound article's table dates it 1965."),
        (1971, "Gambian pound", "Gambian dalasi", 0.2, "wp-gmd", "Five dalasis to the pound.")]},
    {"iso": "IR", "name": "Iran", "start": 1945, "unit": "rial", "currency": "Iranian rial",
     "steps": [], "basis": "wp-irr",
     "gap": "A new rial worth 10,000 of the current ones was approved in 2025 with a transition of several years; whether the new notes are in use yet is not confirmed, so it is not applied."},
    {"iso": "AF", "name": "Afghanistan", "start": 1945, "unit": "afghani", "steps": [
        (2002, "Afghani (1925)", "Afghan afghani", 1_000, "wp-afn",
         "1,000 old afghanis per new; notes issued by Dostum in the north were exchanged at 2,000 per new.")],
     "gap": "Every step is cited, but the 2002 exchange used two rates depending on who had issued the notes."},
    {"iso": "KH", "name": "Cambodia", "start": 1945, "unit": "riel", "steps": [
        (1953, "French Indochinese piastre", "Cambodian riel (1953)", 1, "wp-khr", "Notes were issued in both units, the riel at par with the piastre."),
        (1975, "Cambodian riel (1953)", "No currency", None, "wp-khr", "The Khmer Rouge abolished money."),
        (1980, "No currency", "Cambodian riel", None, "wp-khr", "The riel was re-established on 20 March 1980 and handed out by the government, not exchanged for anything.")],
     "gap": "Money was abolished in 1975 and the riel re-created from nothing in 1980, so nothing before 1980 converts to today's riel."},
    {"iso": "LA", "name": "Laos", "start": 1945, "unit": "kip", "steps": [
        (1953, "French Indochinese piastre", "Royal kip", 1, "wp-lak", None),
        (1976, "Royal kip", "Liberation kip", 20, "wp-lak",
         "People could exchange up to 100,000 royal kip and businesses up to a million; the rest had to be deposited in state banks."),
        (1979, "Liberation kip", "Lao kip", 100, "wp-lak", "16 December 1979.")]},
    {"iso": "US", "name": "United States", "start": 1945, "unit": "dollar", "currency": "United States dollar", "steps": [], "basis": "wp-usd"},
    {"iso": "CA", "name": "Canada", "start": 1945, "unit": "dollar", "currency": "Canadian dollar", "steps": [], "basis": "wp-cad"},
    {"iso": "CO", "name": "Colombia", "start": 1945, "unit": "peso", "currency": "Colombian peso", "steps": [], "basis": "wp-cop"},
    {"iso": "PY", "name": "Paraguay", "start": 1945, "unit": "guaraní", "currency": "Paraguayan guaraní", "steps": [], "basis": "wp-pyg"},
    {"iso": "GT", "name": "Guatemala", "start": 1945, "unit": "quetzal", "currency": "Guatemalan quetzal", "steps": [], "basis": "wp-gtq"},
    {"iso": "CR", "name": "Costa Rica", "start": 1945, "unit": "colón", "currency": "Costa Rican colón", "steps": [], "basis": "wp-crc"},
    {"iso": "CH", "name": "Switzerland", "start": 1945, "unit": "franc", "currency": "Swiss franc", "steps": [], "basis": "wp-chf"},
    {"iso": "SE", "name": "Sweden", "start": 1945, "unit": "krona", "currency": "Swedish krona", "steps": [], "basis": "wp-sek"},
    {"iso": "NO", "name": "Norway", "start": 1945, "unit": "krone", "currency": "Norwegian krone", "steps": [], "basis": "wp-nok"},
    {"iso": "DK", "name": "Denmark", "start": 1945, "unit": "krone", "currency": "Danish krone", "steps": [], "basis": "wp-dkk"},
    {"iso": "DO", "name": "Dominican Republic", "start": 1945, "unit": "peso", "steps": [
        (1947, "United States dollar", "Dominican peso", 1, "wp-dop",
         "The peso oro, at par with the dollar, had circulated since 1937; the dollar stopped being used alongside it in 1947.")]},
    {"iso": "CZ", "name": "Czech Republic (and Czechoslovakia)", "start": 1945, "unit": "koruna", "steps": [
        (1945, "Bohemian and Moravian koruna", "Czechoslovak koruna", 1, "wp-bmk", None),
        (1953, "Czechoslovak koruna", "Czechoslovak koruna (1953)", 5, "wp-csk2",
         "5 old for 1 new on the first 1,500 korunas per person, 50 for 1 on the rest. The 5:1 rate is used here."),
        (1993, "Czechoslovak koruna (1953)", "Czech koruna", 1, "wp-csk2", "The split of 8 February 1993, at par.")],
     "gap": "Every step is cited, but the 1953 reform used two rates (5:1 up to a limit, 50:1 beyond), so the factor holds only for small amounts."},
    {"iso": "MA", "name": "Morocco", "start": 1945, "unit": "dirham", "steps": [
        (1960, "Moroccan franc", "Moroccan dirham", 100, "wp-mad",
         "Follows the former French zone. The former Spanish zone had switched from the peseta to the franc at 10 francs per peseta after reunification.")]},
    {"iso": "TN", "name": "Tunisia", "start": 1945, "unit": "dinar", "steps": [
        (1958, "Tunisian franc", "Tunisian dinar", 1_000, "wp-tnd", "A unit of account from 1958; notes and coins from 1960.")]},
    {"iso": "DZ", "name": "Algeria", "start": 1945, "unit": "dinar", "steps": [
        (1960, "Algerian franc", "Algerian new franc", 100, "wp-dzf", None),
        (1964, "Algerian new franc", "Algerian dinar", 1, "wp-dzd", None)]},
    {"iso": "ET", "name": "Ethiopia", "start": 1945, "unit": "birr", "steps": [
        (1945, "East African shilling", "Ethiopian birr", 2, "wp-etb",
         "23 July 1945. Called the Ethiopian dollar in English until 1976, when birr became the name in every language.")]},
    {"iso": "IN", "name": "India", "start": 1945, "unit": "rupee", "currency": "Indian rupee", "steps": [], "basis": "wp-inr"},
    {"iso": "JP", "name": "Japan", "start": 1945, "unit": "yen", "currency": "Japanese yen", "steps": [], "basis": "boj-newyen"},
    {"iso": "PH", "name": "Philippines", "start": 1945, "unit": "peso", "currency": "Philippine peso", "steps": [], "basis": "ph-eo25"},
    {"iso": "TH", "name": "Thailand", "start": 1945, "unit": "baht", "currency": "Thai baht", "steps": [], "basis": "wp-thb"},
    {"iso": "LK", "name": "Sri Lanka", "start": 1945, "unit": "rupee", "currency": "Sri Lankan rupee", "steps": [], "basis": "wp-lkr"},
    {"iso": "IQ", "name": "Iraq", "start": 1945, "unit": "dinar", "currency": "Iraqi dinar", "steps": [], "basis": "wp-iqd"},
    {"iso": "SA", "name": "Saudi Arabia", "start": 1945, "unit": "riyal", "currency": "Saudi riyal", "steps": [], "basis": "wp-sar"},
    {"iso": "EG", "name": "Egypt", "start": 1945, "unit": "pound", "currency": "Egyptian pound", "steps": [], "basis": "wp-egp"},
    {"iso": "NP", "name": "Nepal", "start": 1945, "unit": "rupee", "currency": "Nepalese rupee", "steps": [], "basis": "wp-npr"},
    {"iso": "MN", "name": "Mongolia", "start": 1945, "unit": "tögrög", "currency": "Mongolian tögrög", "steps": [], "basis": "wp-mnt"},
    {"iso": "PK", "name": "Pakistan", "start": 1945, "unit": "rupee", "steps": [
        (1948, "Indian rupee", "Pakistani rupee", 1, "wp-pkr", "Pakistan's own notes replaced Indian ones after independence, at parity.")]},
    {"iso": "BD", "name": "Bangladesh", "start": 1945, "unit": "taka", "steps": [
        (1948, "Indian rupee", "Pakistani rupee", 1, "wp-pkr", "As East Pakistan."),
        (1972, "Pakistani rupee", "Bangladeshi taka", 1, "wp-bdt", None)]},
    {"iso": "MY", "name": "Malaysia", "start": 1945, "unit": "ringgit", "steps": [
        (1953, "Malayan dollar", "Malaya and British Borneo dollar", 1, "wp-mbbd",
         "The Japanese occupation dollar was declared worthless in 1945 and the pre-war dollar restored."),
        (1967, "Malaya and British Borneo dollar", "Malaysian ringgit", 1, "wp-mbbd", None)]},
    {"iso": "SG", "name": "Singapore", "start": 1945, "unit": "dollar", "steps": [
        (1953, "Malayan dollar", "Malaya and British Borneo dollar", 1, "wp-mbbd",
         "The Japanese occupation dollar was declared worthless in 1945 and the pre-war dollar restored."),
        (1967, "Malaya and British Borneo dollar", "Singapore dollar", 1, "wp-mbbd", None)]},
    {"iso": "MM", "name": "Myanmar", "start": 1945, "unit": "kyat", "steps": [
        (1952, "Burmese rupee", "Myanmar kyat", 1, "wp-mmk",
         "The Japanese occupation kyat became worthless in 1945. Later note withdrawals (1964, 1985, 1987) cancelled notes without changing the unit.")]},
    {"iso": "KP", "name": "North Korea", "start": 1945, "unit": "won", "steps": [
        (1947, "Korean yen", "North Korean won (1947)", 1, "wp-krwyen", "6 December 1947."),
        (1959, "North Korean won (1947)", "North Korean won (1959)", 100, "wp-kpw", None),
        (2009, "North Korean won (1959)", "North Korean won", 100, "wp-kpw",
         "Each person could exchange only a limited amount (first 100,000, later up to 500,000 old won); the rest could not be converted.")]},
    {"iso": "CM", "name": "Cameroon", "start": 1946, "unit": "CFA franc", "currency": "Central African CFA franc", "steps": [], "basis": "wp-xaf-c"},
]

WORLD_ALIASES = {}

WORLD_WORLD_BANK = {
    "GB": "GBR", "AU": "AUS", "NZ": "NZL", "ZA": "ZAF", "NG": "NGA", "KE": "KEN", "TZ": "TZA",
    "JM": "JAM", "MW": "MWI", "GM": "GMB", "IR": "IRN", "AF": "AFG", "KH": "KHM", "LA": "LAO",
    "US": "USA", "CA": "CAN", "CO": "COL", "PY": "PRY", "GT": "GTM", "CR": "CRI", "CH": "CHE",
    "SE": "SWE", "NO": "NOR", "DK": "DNK", "DO": "DOM", "CZ": "CZE", "MA": "MAR", "TN": "TUN",
    "DZ": "DZA", "ET": "ETH", "CM": "CMR",
    "IN": "IND", "PK": "PAK", "BD": "BGD", "JP": "JPN", "PH": "PHL", "TH": "THA", "MY": "MYS",
    "SG": "SGP", "LK": "LKA", "MM": "MMR", "IQ": "IRQ", "SA": "SAU", "EG": "EGY", "NP": "NPL",
    "KP": None, "MN": "MNG",
}

WORLD_UNITS = {
    "GB": "GBP", "AU": "AUD", "NZ": "NZD", "ZA": "ZAR", "NG": "NGN", "KE": "KES", "TZ": "TZS",
    "JM": "JMD", "MW": "MWK", "GM": "GMD", "IR": "IRR", "AF": "AFN", "KH": "KHR", "LA": "LAK",
    "US": "USD", "CA": "CAD", "CO": "COP", "PY": "PYG", "GT": "GTQ", "CR": "CRC", "CH": "CHF",
    "SE": "SEK", "NO": "NOK", "DK": "DKK", "DO": "DOP", "CZ": "CZK", "MA": "MAD", "TN": "TND",
    "DZ": "DZD", "ET": "ETB", "CM": "XAF",
    "IN": "INR", "PK": "PKR", "BD": "BDT", "JP": "JPY", "PH": "PHP", "TH": "THB", "MY": "MYR",
    "SG": "SGD", "LK": "LKR", "MM": "MMK", "IQ": "IQD", "SA": "SAR", "EG": "EGP", "NP": "NPR",
    "KP": "KPW", "MN": "MNT",
}


# ---------- Caribbean and Central America ----------
WORLD_SOURCES.update({
    "wp-bspound": _wp("Bahamian_pound", "1966: 7 shillings = $1"),
    "wp-bwi": _wp("British_West_Indies_dollar", "introduced 1949 at the existing $4.80 per pound sterling; replaced at par by the East Caribbean dollar"),
    "wp-xcd": _wp("Eastern_Caribbean_dollar", "replaced the BWI dollar at par in 1965; Grenada used the Trinidad and Tobago dollar 1964–1968"),
    "wp-bbd": _wp("Barbadian_dollar", "BWI dollar from 1949; Barbados dollar replaced the East Caribbean dollar at par in 1973"),
    "wp-bzd": _wp("Belize_dollar", "known until 1973 as the British Honduras dollar"),
    "wp-gyd": _wp("Guyanese_dollar", "dollar worth 4s 2d; BWI notes from 1951; EC dollar 1965; Guyanese dollar at par 1966"),
    "wp-ttd": _wp("Trinidad_and_Tobago_dollar", "dollar of 4s 2d from 1934; BWI dollar from 1949; own dollar again in 1964"),
    "wp-htg": _wp("Haitian_gourde", "last revalued in 1872"),
    "wp-hnl": _wp("Honduran_lempira", "introduced in 1931"),
    "wp-pab": _wp("Panamanian_balboa", "at 1:1 with the US dollar since its introduction; the dollar also legal tender"),
    "wp-cup": _wp("Cuban_peso", "the peso throughout; the parallel convertible peso (1994–2021) was converted at 24 pesos each"),
})

_EC = [(1949, "Pound sterling", "British West Indies dollar", 1 / 4.8, "wp-bwi",
        "Accounts moved from sterling to the BWI dollar at the existing $4.80 to the pound."),
       (1965, "British West Indies dollar", "Eastern Caribbean dollar", 1, "wp-xcd", None)]

WORLD += [
    {"iso": "BS", "name": "Bahamas", "start": 1945, "unit": "dollar", "steps": [
        (1966, "Bahamian pound", "Bahamian dollar", 0.35, "wp-bspound", "Seven shillings to the dollar.")]},
    *[{"iso": iso, "name": name, "start": 1945, "unit": "East Caribbean dollar", "steps": list(_EC)}
      for iso, name in [("AG", "Antigua and Barbuda"), ("DM", "Dominica"), ("KN", "Saint Kitts and Nevis"),
                        ("LC", "Saint Lucia"), ("VC", "Saint Vincent and the Grenadines")]],
    {"iso": "GD", "name": "Grenada", "start": 1945, "unit": "East Caribbean dollar", "steps": [
        _EC[0],
        (1964, "British West Indies dollar", "Trinidad and Tobago dollar", 1, None, "Grenada used the Trinidad and Tobago dollar from 1964; presumably at par, but no source states the rate."),
        (1968, "Trinidad and Tobago dollar", "Eastern Caribbean dollar", 1, None, "Grenada rejoined the common currency in 1968; the rate is not stated.")]},
    {"iso": "BB", "name": "Barbados", "start": 1949, "unit": "dollar", "currency": "British West Indies dollar", "steps": [
        (1965, "British West Indies dollar", "Eastern Caribbean dollar", 1, "wp-bwi", None),
        (1973, "Eastern Caribbean dollar", "Barbadian dollar", 1, "wp-bbd", None)],
     "gap": "Starts at the BWI dollar of 1949. Before it, sterling and government dollar notes circulated together and no source says which was legal tender."},
    {"iso": "BZ", "name": "Belize", "start": 1945, "unit": "dollar", "currency": "Belize dollar", "steps": [], "basis": "wp-bzd"},
    {"iso": "GY", "name": "Guyana", "start": 1945, "unit": "dollar", "steps": [
        (1951, "British Guiana dollar", "British West Indies dollar", 1, "wp-gyd",
         "Local notes were replaced by BWI notes; both dollars were worth four shillings and two pence."),
        (1965, "British West Indies dollar", "Eastern Caribbean dollar", 1, "wp-bwi", None),
        (1966, "Eastern Caribbean dollar", "Guyanese dollar", 1, "wp-gyd", None)]},
    {"iso": "TT", "name": "Trinidad and Tobago", "start": 1945, "unit": "dollar", "steps": [
        (1949, "Trinidad and Tobago dollar (1934)", "British West Indies dollar", 1, "wp-ttd",
         "Both were worth four shillings and two pence, $4.80 to the pound."),
        (1964, "British West Indies dollar", "Trinidad and Tobago dollar", 1, None,
         "The Central Bank's own dollar from December 1964; presumably at par, but no source states the rate.")]},
    {"iso": "HT", "name": "Haiti", "start": 1945, "unit": "gourde", "currency": "Haitian gourde", "steps": [], "basis": "wp-htg"},
    {"iso": "HN", "name": "Honduras", "start": 1945, "unit": "lempira", "currency": "Honduran lempira", "steps": [], "basis": "wp-hnl"},
    {"iso": "PA", "name": "Panama", "start": 1945, "unit": "balboa", "currency": "Panamanian balboa", "steps": [], "basis": "wp-pab"},
    {"iso": "CU", "name": "Cuba", "start": 1945, "unit": "peso", "currency": "Cuban peso", "steps": [], "basis": "wp-cup"},
]
WORLD_WORLD_BANK.update({"BS": "BHS", "AG": "ATG", "DM": "DMA", "KN": "KNA", "LC": "LCA", "VC": "VCT", "GD": "GRD",
                         "BB": "BRB", "BZ": "BLZ", "GY": "GUY", "TT": "TTO", "HT": "HTI", "HN": "HND", "PA": "PAN", "CU": "CUB"})
WORLD_UNITS.update({"BS": "BSD", "AG": "XCD", "DM": "XCD", "KN": "XCD", "LC": "XCD", "VC": "XCD", "GD": "XCD",
                    "BB": "BBD", "BZ": "BZD", "GY": "GYD", "TT": "TTD", "HT": "HTG", "HN": "HNL", "PA": "PAB", "CU": "CUP"})


# ---------- West, Central and East Africa ----------
WORLD_SOURCES.update({
    "wp-xof": _wp("West_African_CFA_franc", "introduced in 1945, replacing the French West African franc; no swap rate is stated"),
    "wp-xaf-c": _wp("Central_African_CFA_franc", "introduced in 1945, replacing the French Equatorial African franc; kept at independence; no swap rate is stated"),
    "wp-tgf": _wp("Togolese_franc", "Togo has used the West African CFA franc since 1945"),
    "wp-kmf": _wp("Comorian_franc", "Madagascar-Comores CFA franc from 1945; notes overstamped COMORES from 1962"),
    "wp-djf": _wp("Djiboutian_franc", "an independent Djibouti franc from 1949"),
    "wp-cve": _wp("Cape_Verdean_escudo", "the escudo since 1914, equal to the Portuguese escudo until 1975"),
    "wp-lrd": _wp("Liberian_dollar", "the currency since 1943; the 2000 unified notes were exchanged at par for J. J. notes and at 1:2 for Liberty notes"),
    "aacb-rw": {"title": "Association of African Central Banks, monetary history of Rwanda (1960: one Rwanda and Burundi franc against one Congolese franc)",
                "url": "https://aacb.org/fr/book/export/html/374", "accessed": "2026-10-30"},
    "wp-bif": _wp("Burundian_franc", "Burundi began issuing its own francs in 1964"),
    "wp-rwf": _wp("Rwandan_franc", "Rwanda began issuing the Rwandan franc in 1964"),
    "wp-somalo": _wp("Somalo", "replaced the East African shilling at par in 1950; replaced at par by the Somali shilling on 15 December 1962"),
    "wp-ern": _wp("Eritrean_nakfa", "introduced 15 November 1997 to replace the birr at par"),
    "wp-eas": _wp("East_African_shilling", "Eritrea adopted the Ethiopian dollar on federation in 1952"),
})

WORLD += [
    *[{"iso": iso, "name": name, "start": 1946, "unit": "CFA franc", "currency": "West African CFA franc", "steps": [], "basis": "wp-xof"}
      for iso, name in [("BJ", "Benin"), ("BF", "Burkina Faso"), ("CI", "Côte d'Ivoire"), ("NE", "Niger"), ("SN", "Senegal")]],
    {"iso": "TG", "name": "Togo", "start": 1946, "unit": "CFA franc", "currency": "West African CFA franc", "steps": [], "basis": "wp-tgf"},
    *[{"iso": iso, "name": name, "start": 1946, "unit": "CFA franc", "currency": "Central African CFA franc", "steps": [], "basis": "wp-xaf-c"}
      for iso, name in [("CF", "Central African Republic"), ("TD", "Chad"), ("CG", "Republic of the Congo"), ("GA", "Gabon")]],
    {"iso": "KM", "name": "Comoros", "start": 1946, "unit": "Comorian franc", "currency": "Comorian franc", "steps": [], "basis": "wp-kmf",
     "gap": "Started as the Madagascar-Comores CFA franc of 1945; when and at what rate the Comorian franc separated from it is not stated."},
    {"iso": "DJ", "name": "Djibouti", "start": 1949, "unit": "franc", "currency": "Djiboutian franc", "steps": [], "basis": "wp-djf"},
    {"iso": "CV", "name": "Cabo Verde", "start": 1945, "unit": "escudo", "currency": "Cape Verdean escudo", "steps": [], "basis": "wp-cve"},
    {"iso": "LR", "name": "Liberia", "start": 1945, "unit": "dollar", "currency": "Liberian dollar", "steps": [], "basis": "wp-lrd"},
    *[{"iso": iso, "name": name, "start": 1945, "unit": "franc", "steps": [
        (1960, "Belgian Congo franc", "Rwanda and Burundi franc", 1, "aacb-rw", None),
        (1964, "Rwanda and Burundi franc", cur, 1, None, "Own francs from 1964; presumably at par, but no source states the rate.")]}
      for iso, name, cur in [("BI", "Burundi", "Burundian franc"), ("RW", "Rwanda", "Rwandan franc")]],
    {"iso": "SO", "name": "Somalia", "start": 1945, "unit": "shilling", "steps": [
        (1950, "East African shilling", "Somalo", 1, "wp-somalo", "In the former Italian south; the north kept the East African shilling until 1962."),
        (1962, "Somalo", "Somali shilling", 1, "wp-somalo", "An attempted 100-to-1 reform in 1990 is not known to have taken effect.")]},
    {"iso": "ER", "name": "Eritrea", "start": 1945, "unit": "nakfa", "steps": [
        (1952, "East African shilling", "Ethiopian birr", 2, None,
         "Adopted on federation with Ethiopia in 1952. Ethiopia's own rate was two shillings to the dollar; the rate used in Eritrea is not stated."),
        (1997, "Ethiopian birr", "Eritrean nakfa", 1, "wp-ern", None)]},
]
WORLD_WORLD_BANK.update({"BJ": "BEN", "BF": "BFA", "CI": "CIV", "NE": "NER", "SN": "SEN", "TG": "TGO", "CF": "CAF", "TD": "TCD",
                         "CG": "COG", "GA": "GAB", "KM": "COM", "DJ": "DJI", "CV": "CPV", "LR": "LBR", "BI": "BDI", "RW": "RWA",
                         "SO": "SOM", "ER": "ERI"})
WORLD_UNITS.update({"BJ": "XOF", "BF": "XOF", "CI": "XOF", "NE": "XOF", "SN": "XOF", "TG": "XOF", "CF": "XAF", "TD": "XAF",
                    "CG": "XAF", "GA": "XAF", "KM": "KMF", "DJ": "DJF", "CV": "CVE", "LR": "LRD", "BI": "BIF", "RW": "RWF",
                    "SO": "SOS", "ER": "ERN"})


# ---------- Southern Africa, Indian Ocean, Gulf, Levant ----------
WORLD_SOURCES.update({
    "wp-bwp": _wp("Botswana_pula", "introduced 23 August 1976, replacing the rand at par"),
    "wp-szl": _wp("Swazi_lilangeni", "introduced in 1974 at par with the rand"),
    "wp-lsl": _wp("Lesotho_loti", "pegged 1:1 to the rand; circulating coins from 1979–80 to replace the rand"),
    "wp-nad": _wp("Namibian_dollar", "first notes 15 September 1993, at par with the rand"),
    "wp-zar-users": _wp("South_African_rand", "South West Africa used the rand from 1961"),
    "wp-mur": _wp("Mauritian_rupee", "the rupee throughout, with only new coin and note issues since 1945"),
    "wp-scr": _wp("Seychellois_rupee", "currency of Seychelles since 1914"),
    "wp-sdd": _wp("Sudanese_dinar", "1992 at 10 pounds per dinar; 2007 second pound at 100 dinars"),
    "wp-ssp": _wp("South_Sudanese_pound", "introduced 18 July 2011, replacing the Sudanese pound at par"),
    "wp-mvr": _wp("Maldivian_rufiyaa", "rufiyaa notes from 1947, equal in value to the Ceylonese rupee"),
    "wp-gulfrupee": _wp("Gulf_rupee", "issued 1959, equivalent to the Indian rupee"),
    "wp-bhd": _wp("Bahraini_dinar", "1965, at 10 Gulf rupees to the dinar"),
    "wp-kwd": _wp("Kuwaiti_dinar", "1961, at 13⅓ rupees to the dinar"),
    "wp-omr": _wp("Omani_rial", "Saidi rial of 1970 at 21 Gulf rupees; renamed Omani rial at par in 1972"),
    "wp-qar": _wp("Qatari_riyal", "1966: Saudi riyal at 1.065 Gulf rupees, then the Qatar and Dubai riyal; Qatari riyal at par in 1973"),
    "wp-aed": _wp("United_Arab_Emirates_dirham", "Abu Dhabi: Bahraini dinar at 10 Gulf rupees in 1966; dirham at 10 to the dinar in 1973"),
    "wp-yer-n": _wp("North_Yemeni_rial", "replaced at par by the Yemeni rial after unification"),
    "wp-jod": _wp("Jordanian_dinar", "issued from 1949, exchangeable for Palestine pounds at parity"),
    "wp-lbp": _wp("Lebanese_pound", "the Lebanese pound since its 1939 separation from Syria's"),
    "wp-syp": _wp("Syrian_pound", "1 January 2026: 100 old pounds for one new pound"),
    "wp-btn": _wp("Bhutanese_ngultrum", "1974, at par with the Indian rupee"),
})

_RAND = [(1961, "South African pound", "South African rand", 0.5, "wp-zar", "Decimalisation: two rand to the pound.")]
_GULF = [(1959, "Indian rupee", "Gulf rupee", 1, "wp-gulfrupee", None)]

WORLD += [
    {"iso": "BW", "name": "Botswana", "start": 1945, "unit": "pula", "steps": _RAND + [
        (1976, "South African rand", "Botswana pula", 1, "wp-bwp", None)]},
    {"iso": "SZ", "name": "Eswatini", "start": 1945, "unit": "lilangeni", "steps": _RAND + [
        (1974, "South African rand", "Swazi lilangeni", 1, "wp-szl", None)]},
    {"iso": "LS", "name": "Lesotho", "start": 1945, "unit": "loti", "steps": _RAND + [
        (1980, "South African rand", "Lesotho loti", 1, "wp-lsl", "Issued from 1966 as an accounting unit, in circulation from 1980; the rand is still legal tender.")]},
    {"iso": "NA", "name": "Namibia", "start": 1961, "unit": "dollar", "currency": "South African rand", "steps": [
        (1993, "South African rand", "Namibian dollar", 1, "wp-nad", "The rand is still legal tender.")]},
    {"iso": "MU", "name": "Mauritius", "start": 1945, "unit": "rupee", "currency": "Mauritian rupee", "steps": [], "basis": "wp-mur"},
    {"iso": "SC", "name": "Seychelles", "start": 1945, "unit": "rupee", "currency": "Seychellois rupee", "steps": [], "basis": "wp-scr"},
    {"iso": "SS", "name": "South Sudan", "start": 1945, "unit": "pound", "steps": [
        (1956, "Egyptian pound", "First Sudanese pounds", 1, "wp-sdpound", "Created on 1 January 1956; the first notes followed in April 1957."),
        (1992, "First Sudanese pounds", "Sudanese dinar", 10, "wiki", "In the south, prices were often still set in pounds, and Kenyan shillings were widely used."),
        (2007, "Sudanese dinars", "Second Sudanese pound", 100, "wiki", None),
        (2011, "Second Sudanese pound", "South Sudanese pound", 1, "wp-ssp", "Independence.")]},
    {"iso": "MV", "name": "Maldives", "start": 1945, "unit": "rufiyaa", "steps": [
        (1947, "Ceylon rupee", "Maldivian rufiyaa", 1, "wp-mvr", "Rufiyaa notes, equal in value to the rupee, circulated alongside it at first.")]},
    {"iso": "BH", "name": "Bahrain", "start": 1945, "unit": "dinar", "steps": _GULF + [
        (1965, "Gulf rupee", "Bahraini dinar", 10, "wp-bhd", None)]},
    {"iso": "KW", "name": "Kuwait", "start": 1945, "unit": "dinar", "steps": _GULF + [
        (1961, "Gulf rupee", "Kuwaiti dinar", 40 / 3, "wp-kwd", "During the Iraqi occupation of 1990–91 the Iraqi dinar was imposed; the Kuwaiti dinar was then restored at its pre-war value.")]},
    {"iso": "OM", "name": "Oman", "start": 1945, "unit": "rial", "steps": _GULF + [
        (1970, "Gulf rupee", "Saidi rial", 21, "wp-omr", "7 May 1970. The Gulf rupee article gives 13⅓ rupees to the rial instead."),
        (1972, "Saidi rial", "Omani rial", 1, "wp-omr", "A renaming, at par.")],
     "gap": "Every step is cited, but sources disagree on the 1970 rate (21 or 13⅓ Gulf rupees per rial)."},
    {"iso": "QA", "name": "Qatar", "start": 1945, "unit": "riyal", "steps": _GULF + [
        (1966, "Gulf rupee", "Saudi riyal", 1.065, "wp-qar", "Adopted briefly after India devalued the Gulf rupee."),
        (1966, "Saudi riyal", "Qatar and Dubai riyal", None, "wp-qar", "Introduced in September 1966; no rate against the Saudi riyal is stated."),
        (1973, "Qatar and Dubai riyal", "Qatari riyal", 1, "wp-qar", None)],
     "gap": "The 1966 switch from the Saudi riyal to the Qatar and Dubai riyal has no stated rate, so amounts from before September 1966 do not convert."},
    {"iso": "AE", "name": "United Arab Emirates", "start": 1945, "unit": "dirham", "steps": _GULF + [
        (1966, "Gulf rupee", "Bahraini dinar", 10, "wp-aed", "Follows Abu Dhabi. Dubai and the northern emirates used the Saudi riyal and then the Qatar and Dubai riyal, exchanged for the dirham at par."),
        (1973, "Bahraini dinar", "United Arab Emirates dirham", 0.1, "wp-aed", "Ten dirhams to the dinar.")]},
    {"iso": "YE", "name": "Yemen", "start": 1945, "unit": "rial", "steps": [
        (1990, "North Yemeni rial", "Yemeni rial", 1, "wp-yer-n",
         "Follows the north. In the south, the South Yemeni dinar was exchanged at 26 rials until 1996.")]},
    {"iso": "JO", "name": "Jordan", "start": 1945, "unit": "dinar", "steps": [
        (1950, "Palestine pound", "Jordanian dinar", 1, "wp-jod", "Legal tender from 1 July 1950.")]},
    {"iso": "LB", "name": "Lebanon", "start": 1945, "unit": "pound", "currency": "Lebanese pound", "steps": [], "basis": "wp-lbp"},
    {"iso": "SY", "name": "Syria", "start": 1945, "unit": "pound", "steps": [
        (2026, "Syrian pound", "New Syrian pound", 100, "wp-syp", "1 January 2026. Old notes could be exchanged until 30 July 2026.")]},
    {"iso": "BT", "name": "Bhutan", "start": 1945, "unit": "ngultrum", "steps": [
        (1974, "Indian rupee", "Bhutanese ngultrum", 1, "wp-btn", "The Indian rupee still circulates at par.")]},
]
WORLD_WORLD_BANK.update({"BW": "BWA", "SZ": "SWZ", "LS": "LSO", "NA": "NAM", "MU": "MUS", "SC": "SYC", "SS": "SSD", "MV": "MDV",
                         "BH": "BHR", "KW": "KWT", "OM": "OMN", "QA": "QAT", "AE": "ARE", "YE": "YEM", "JO": "JOR", "LB": "LBN",
                         "SY": "SYR", "BT": "BTN"})
WORLD_UNITS.update({"BW": "BWP", "SZ": "SZL", "LS": "LSL", "NA": "NAD", "MU": "MUR", "SC": "SCR", "SS": "SSP", "MV": "MVR",
                    "BH": "BHD", "KW": "KWD", "OM": "OMR", "QA": "QAR", "AE": "AED", "YE": "YER", "JO": "JOD", "LB": "LBP",
                    "SY": "SYP", "BT": "BTN"})


# ---------- Europe, the Pacific, Libya ----------
WORLD_SOURCES.update({
    "ec2866w": {"title": "Council Regulation (EC) No 2866/98 on the conversion rates between the euro and the currencies of the Member States adopting the euro, Article 1 (as amended)",
                "url": "https://www.legislation.gov.uk/eur/1998/2866/data.html", "accessed": "2026-10-30"},
    "wp-all": _wp("Albanian_lek", "1965: a confiscatory monetary reform at 10:1"),
    "wp-bad": _wp("Bosnia_and_Herzegovina_dinar", "July 1992 at 10 Yugoslav dinars; August 1994 at 10,000 old; pegged at 100 dinars to the Deutsche Mark"),
    "wp-bam": _wp("Bosnia_and_Herzegovina_convertible_mark", "single currency from 1998, replacing the dinar, kuna and Yugoslav novi dinar"),
    "bqk-euro": {"title": "Central Bank of the Republic of Kosovo, conversion to the euro (Deutsche Mark permitted from 1999; accounts converted on 1 January 2002 at DEM 1.95583 per euro)",
                 "url": "https://bqk-kos.org/operacionet-bankare/paraja-ne-qarkullim/konvertimi-ne-euro/?lang=en", "accessed": "2026-10-30"},
    "cbcg-euro": {"title": "Central Bank of Montenegro, euroisation (Deutsche Mark legal tender alongside the dinar from 2 November 1999, floating; euro from 2002)",
                  "url": "https://cbcg.me/en/core-functions/monetary-policy/euroisation", "accessed": "2026-10-30"},
    "wp-ad": _wp("Andorra_and_the_euro", "the French franc and Spanish peseta were both used; no official currency before the euro"),
    "wp-li": _wp("Liechtenstein_franc", "the Swiss franc has been the currency of Liechtenstein since 1920"),
    "wp-mcf": _wp("Mon%C3%A9gasque_franc", "at par with the French franc; revalued 100:1 in 1960; euro at 6.55957"),
    "wp-sml": _wp("Sammarinese_lira", "pegged to the Italian lira; replaced by the euro at 1,936.27"),
    "wp-bnd": _wp("Brunei_dollar", "1967: replaced the Malaya and British Borneo dollar at par"),
    "wp-fjd": _wp("Fijian_pound", "1969: £1 = FJ$2"),
    "wp-ki": _wp("Kiribati_dollar", "the Australian pound in use since the First World War; own coins at par with the Australian dollar from 1979"),
    "wp-tv": _wp("Tuvaluan_dollar", "officially the Australian dollar from 1966; own coins alongside it from 1976"),
    "wp-oceanian": _wp("Japanese_government-issued_Oceanian_pound", "abolished after the war, replaced by the Australian pound or the US dollar; no rate stated"),
    "wp-pgk": _wp("Papua_New_Guinean_kina", "19 April 1975, equal in value to the Australian dollar"),
    "wp-sbd": _wp("Solomon_Islands_dollar", "1977, replacing the Australian dollar at par"),
    "wp-wst": _wp("Western_Samoan_pound", "1967: 1 pound = 2 tala"),
    "wp-top": _wp("Tongan_pound", "1967: £1 = T$2"),
    "wp-vuv": _wp("Vanuatu_vatu", "1981, replacing the New Hebrides franc at par"),
    "wp-ttpi": _wp("Trust_Territory_of_the_Pacific_Islands", "the US dollar served as the currency"),
    "wp-lyp": _wp("Libyan_pound", "1951–52: £L1 = 480 lire = 980 francs; dinar at par in 1971"),
})

_YU = [(1966, "1944 dinara", "Yugoslav 1966 dinar", 100, "wiki", None),
       (1990, "1966 dinara", "Yugoslav 1990 dinar", 10_000, "wiki", None)]
_YU94 = _YU + [(1992, "1990 dinara", "Yugoslav 1992 dinar", 10, "wiki", None),
               (1993, "1992 dinara", "Yugoslav 1993 dinar", 1_000_000, "wiki", None),
               (1994, "1993 dinara", "Yugoslav 1994 dinar", 1_000_000_000, "wiki", "January 1994."),
               (1994, "1994 dinara", "Yugoslav novi dinar", 13_000_000, "wiki", None)]
_FR = [(1960, "French Franc", "New French Franc", 100, "wiki", None),
       (1999, "New French Franc", "Euro", 6.55957, "ec2866w", None)]
_AUD = [(1966, "Australian pound", "Australian dollar", 0.5, "wp-aud", "Decimalisation: two dollars to the pound.")]

WORLD += [
    {"iso": "AL", "name": "Albania", "start": 1945, "unit": "lek", "steps": [
        (1965, "Albanian lek", "Albanian lek (1965)", 10, "wp-all", "A confiscatory reform: ten old lek for one new.")]},
    {"iso": "BA", "name": "Bosnia and Herzegovina (and Yugoslavia)", "start": 1945, "unit": "convertible mark", "steps": _YU + [
        (1992, "Yugoslav 1990 dinar", "Bosnia and Herzegovina dinar", 10, "wp-bad", "July 1992."),
        (1994, "Bosnia and Herzegovina dinar", "Bosnia and Herzegovina dinar (1994)", 10_000, "wp-bad", "August 1994."),
        (1998, "Bosnia and Herzegovina dinar (1994)", "Bosnia and Herzegovina convertible mark", 100, None,
         "The dinar was pegged at 100 to the Deutsche Mark, which the convertible mark equalled, but no source states the 1998 conversion rate.")],
     "gap": "Follows the government-held areas; Serb-held areas used their own dinars. The 1998 rate to the convertible mark is implied by a peg, not stated."},
    {"iso": "XK", "name": "Kosovo (and Yugoslavia)", "start": 1945, "unit": "euro", "steps": _YU94 + [
        (1999, "Yugoslav novi dinar", "Deutsche Mark", None, "bqk-euro", "The Deutsche Mark was permitted from 1999 alongside the dinar, with no fixed conversion."),
        (2002, "Deutsche Mark", "Euro", 1.95583, "ec2866w", "Accounts converted on 1 January 2002.")],
     "gap": "The move from the dinar to the Deutsche Mark in 1999 had no fixed rate, so amounts from before 1999 do not convert."},
    {"iso": "ME", "name": "Montenegro (and Yugoslavia)", "start": 1945, "unit": "euro", "steps": _YU94 + [
        (1999, "Yugoslav novi dinar", "Deutsche Mark", None, "cbcg-euro", "From 2 November 1999 the Deutsche Mark floated alongside the dinar; it became the only legal tender in 2001."),
        (2002, "Deutsche Mark", "Euro", 1.95583, "ec2866w", None)],
     "gap": "The move from the dinar to the Deutsche Mark in 1999 had no fixed rate, so amounts from before 1999 do not convert."},
    {"iso": "AD", "name": "Andorra", "start": 1945, "unit": "euro", "steps": [
        (1960, "French Franc", "New French Franc", 100, "wiki", "Andorra had no currency of its own; follows the French franc. The Spanish peseta, also used, went to the euro at 166.386."),
        _FR[1]]},
    {"iso": "LI", "name": "Liechtenstein", "start": 1945, "unit": "Swiss franc", "currency": "Swiss franc", "steps": [], "basis": "wp-li"},
    {"iso": "MC", "name": "Monaco", "start": 1945, "unit": "euro", "steps": [
        (1960, "French Franc", "New French Franc", 100, "wiki", "The Monégasque franc circulated at par with the French franc and followed its revaluation."),
        (1999, "New French Franc", "Euro", 6.55957, "ec2866w", "Monaco uses the euro at the French conversion rate under its monetary agreement.")]},
    {"iso": "SM", "name": "San Marino", "start": 1945, "unit": "euro", "steps": [
        (1999, "Italian lira", "Euro", 1936.27, "ec2866w", "The Sammarinese lira was pegged to the Italian lira; euro notes and coins from 1 January 2002.")]},
    {"iso": "BN", "name": "Brunei", "start": 1945, "unit": "dollar", "steps": [
        (1953, "Malayan dollar", "Malaya and British Borneo dollar", 1, "wp-mbbd",
         "The Japanese occupation dollar was declared worthless in 1945 and the pre-war dollar restored."),
        (1967, "Malaya and British Borneo dollar", "Brunei dollar", 1, "wp-bnd", None)]},
    {"iso": "FJ", "name": "Fiji", "start": 1945, "unit": "dollar", "steps": [
        (1969, "Fijian pound", "Fijian dollar", 0.5, "wp-fjd", "Decimalisation: two dollars to the pound.")]},
    {"iso": "KI", "name": "Kiribati", "start": 1945, "unit": "Australian dollar", "steps": [
        (1966, "Australian pound", "Australian dollar", 0.5, "wp-ki", "Kiribati has issued its own coins at par with the Australian dollar since 1979.")]},
    {"iso": "TV", "name": "Tuvalu", "start": 1945, "unit": "Australian dollar", "steps": [
        (1966, "Australian pound", "Australian dollar", 0.5, "wp-tv", "Tuvalu has issued its own coins alongside Australian ones since 1976.")]},
    {"iso": "NR", "name": "Nauru", "start": 1946, "unit": "Australian dollar", "steps": _AUD,
     "gap": "Starts after the war; Nauru was under Japanese occupation in 1945 and the swap of the occupation pound for the Australian pound has no stated rate."},
    {"iso": "PG", "name": "Papua New Guinea", "start": 1945, "unit": "kina", "steps": _AUD + [
        (1975, "Australian dollar", "Papua New Guinean kina", 1, "wp-pgk", "19 April 1975; the two circulated together until the end of 1975.")]},
    {"iso": "SB", "name": "Solomon Islands", "start": 1945, "unit": "dollar", "steps": _AUD + [
        (1977, "Australian dollar", "Solomon Islands dollar", 1, "wp-sbd", None)]},
    {"iso": "WS", "name": "Samoa", "start": 1945, "unit": "tālā", "steps": [
        (1967, "Western Samoan pound", "Samoan tālā", 0.5, "wp-wst", "Two tālā to the pound.")]},
    {"iso": "TO", "name": "Tonga", "start": 1945, "unit": "paʻanga", "steps": [
        (1967, "Tongan pound", "Tongan paʻanga", 0.5, "wp-top", "Two paʻanga to the pound.")]},
    {"iso": "VU", "name": "Vanuatu", "start": 1946, "unit": "vatu", "currency": "CFP franc", "steps": [
        (1969, "CFP franc", "New Hebrides franc", 1, None, "A separate New Hebrides franc from 1969; no source states the rate."),
        (1981, "New Hebrides franc", "Vanuatu vatu", 1, "wp-vuv", None)],
     "gap": "Follows the franc side of the condominium; British and Australian money also circulated until 1983."},
    *[{"iso": iso, "name": name, "start": 1946, "unit": "US dollar", "currency": "United States dollar", "steps": [], "basis": "wp-ttpi"}
      for iso, name in [("MH", "Marshall Islands"), ("FM", "Micronesia"), ("PW", "Palau")]],
    {"iso": "LY", "name": "Libya", "start": 1945, "unit": "dinar", "steps": [
        (1952, "Tripolitanian lira", "Libyan pound", 480, "wp-lyp",
         "Follows Tripolitania. In the Fezzan the Algerian franc went at 980 per pound; in Cyrenaica the Egyptian pound was redeemed in sterling, at about 0.975, though no source states that rate."),
        (1971, "Libyan pound", "Libyan dinar", 1, "wp-lyp", None)]},
]
WORLD_WORLD_BANK.update({"AL": "ALB", "BA": "BIH", "XK": "XKX", "ME": "MNE", "AD": "AND", "LI": "LIE", "MC": "MCO", "SM": "SMR",
                         "BN": "BRN", "FJ": "FJI", "KI": "KIR", "TV": "TUV", "NR": "NRU", "PG": "PNG", "SB": "SLB", "WS": "WSM",
                         "TO": "TON", "VU": "VUT", "MH": "MHL", "FM": "FSM", "PW": "PLW", "LY": "LBY"})
WORLD_UNITS.update({"AL": "ALL", "BA": "BAM", "XK": "EUR", "ME": "EUR", "AD": "EUR", "LI": "CHF", "MC": "EUR", "SM": "EUR",
                    "BN": "BND", "FJ": "FJD", "KI": "AUD", "TV": "AUD", "NR": "AUD", "PG": "PGK", "SB": "SBD", "WS": "WST",
                    "TO": "TOP", "VU": "VUV", "MH": "USD", "FM": "USD", "PW": "USD", "LY": "LYD"})
