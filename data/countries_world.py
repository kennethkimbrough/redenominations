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
]

WORLD_ALIASES = {}

WORLD_WORLD_BANK = {
    "GB": "GBR", "AU": "AUS", "NZ": "NZL", "ZA": "ZAF", "NG": "NGA", "KE": "KEN", "TZ": "TZA",
    "JM": "JAM", "MW": "MWI", "GM": "GMB", "IR": "IRN", "AF": "AFG", "KH": "KHM", "LA": "LAO",
}

WORLD_UNITS = {
    "GB": "GBP", "AU": "AUD", "NZ": "NZD", "ZA": "ZAR", "NG": "NGN", "KE": "KES", "TZ": "TZS",
    "JM": "JMD", "MW": "MWK", "GM": "GMD", "IR": "IRR", "AF": "AFN", "KH": "KHR", "LA": "LAK",
}
