
import os
import requests
import wikipediaapi
import pycountry
from dotenv import load_dotenv

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
        "Fun Fact": get_fun_fact(display_name)
    }

    return country_info

def get_fun_fact(country_name):
    """Fetch a fun fact from Wikipedia with a proper User-Agent."""
    wiki = wikipediaapi.Wikipedia(
        language="en",
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="GlobeExplorer/1.0 (contact@yourdomain.com)"
    )
    page = wiki.page(country_name)
    return page.summary[:300] + "..." if page.exists() else "No fun facts available."


def get_currency_conversion(base_currency):
    """Convert from base_currency to USD, then use USD → [GBP, JPY, EUR] in one call."""
    # Load the .env file
    load_dotenv()
    # Use the variable
    ACCESS_KEY = os.getenv('API_KEY')
    conversions = {}

    try:
        #  base_currency to USD
        url_to_usd = f"http://api.exchangerate.host/convert?access_key={ACCESS_KEY}&from={base_currency}&to=USD&amount=1"
        response_usd = requests.get(url_to_usd)
        data_usd = response_usd.json()

        if not data_usd.get("success"):
            print("Failed to convert base currency to USD:", data_usd.get("error", "Unknown error"))
            return None

        if "result" not in data_usd:
            print("Unexpected response format - no 'result' field:", data_usd)
            return None

        usd_amount = data_usd["result"]
        conversions["USD"] = round(usd_amount, 4)

        #  USD to GBP, JPY, EUR
        symbols = ["GBP", "JPY", "EUR"]
        for symbol in symbols:
            url = f"http://api.exchangerate.host/convert?access_key={ACCESS_KEY}&from=USD&to={symbol}&amount={usd_amount}"
            response = requests.get(url)
            data = response.json()

            if not data.get("success"):
                print(f"Failed to convert USD to {symbol}:", data.get("error", "Unknown error"))
                continue  # Skip this currency but continue with others

            if "result" in data:
                conversions[symbol] = round(data["result"], 4)
            else:
                print(f"No result for USD→{symbol} conversion:", data)

        return conversions

    except Exception as e:
        print(f"Error in get_currency_conversion: {str(e)}")
        return None


class Country:

    def __init__(self, name, capital, region, population, area, currency, timezone, flag_url, fun_fact):
        """Constructor method for class Country"""
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
