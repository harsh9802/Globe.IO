import requests
import wikipediaapi
import pycountry

def normalize_country_name(input_name):
    """Convert ISO codes or common abbreviations to official country names using pycountry."""
    input_cleaned = input_name.strip().lower()
    for country in pycountry.countries:
        if input_cleaned == country.alpha_2.lower() or input_cleaned == country.alpha_3.lower():
            return country.name
        if input_cleaned == country.name.lower():
            return country.name
        if hasattr(country, "common_name") and input_cleaned == country.common_name.lower():
            return country.name
    return input_name

def get_country_data(country_input):
    """Fetch accurate country data from REST Countries API."""
    normalized_name = normalize_country_name(country_input)

    url = f"https://restcountries.com/v3.1/name/{normalized_name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    results = response.json()

    match = None
    for country in results:
        common = country.get("name", {}).get("common", "").lower()
        official = country.get("name", {}).get("official", "").lower()
        alt_spellings = [s.lower() for s in country.get("altSpellings", [])]

        if normalized_name.lower() in (common, official) or normalized_name.lower() in alt_spellings:
            match = country
            break

    data = match or results[0]

    currencies = data.get("currencies", {})
    first_currency = list(currencies.keys())[0] if currencies else "N/A"
    currency_name = currencies.get(first_currency, {}).get("name", "N/A")
    currency_symbol = currencies.get(first_currency, {}).get("symbol", "N/A")

    timezone = data.get("timezones", ["N/A"])[0]

    display_name = data.get("name", {}).get("common", normalized_name)

    country_info = {
        "Name": display_name,
        "Capital": data.get("capital", ["N/A"])[0],
        "Region": data.get("region", "N/A"),
        "Population": data.get("population", "N/A"),
        "Area": data.get("area", "N/A"),
        "Currency": f"{currency_name} ({first_currency}) {currency_symbol}",
        "Timezone": timezone,
        "Flag": match.get("flags", {}).get("png", ""),
    }

    return country_info


class Country:
    """Represents a country and its metadata, flag, and fun fact."""

    def __init__(self, name, capital, region, population, area, currency, timezone, flag_url, fun_fact):
        self.name = name
        self.capital = capital
        self.region = region
        self.population = population
        self.area = area
        self.currency = currency
        self.timezone = timezone
        self.flag_url = flag_url
        self.fun_fact = fun_fact

    def fetch_country(name):
        """Fetch country info and return a Country object."""
        info = get_country_data(name)
        if not info:
            return None
        return Country(
            name=info["Name"],
            capital=info["Capital"],
            region=info["Region"],
            population=info["Population"],
            area=info["Area"],
            currency=info["Currency"],
            timezone=info["Timezone"],
            flag_url=info["Flag"],
            fun_fact=info["Fun Fact"]
        )

