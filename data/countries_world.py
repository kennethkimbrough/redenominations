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
    "wp-iqd": _wp("Iraqi_dinar", "the dinar since 1932; 2003 notes exchanged at par"),
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
    {"iso": "CM", "name": "Cameroon", "start": 1946, "unit": "CFA franc", "currency": "Central African CFA franc", "steps": [], "basis": "wp-xaf",
     "gap": "Starts at the CFA franc's creation in December 1945. The rate at which French Cameroun's own franc was swapped, the move to the BEAC issue in the 1970s, and the former British Southern Cameroons are not yet cited."},
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
