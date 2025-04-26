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
