from country_data import normalize_country_name, Country

def test_normalize_name():
    """Test that an ISO alpha-2 country code returns the correct country name."""
    result = normalize_country_name("IN")
    assert result == "India"

def test_normalize_name_invalid():
    """Test that an unrecognized country code returns the original input."""
    result = normalize_country_name("XYZLAND")
    assert result == "XYZLAND"

def test_country_fetch_name():
    """Test that Country.fetch_country returns the correct country name for Japan."""
    country = Country.fetch_country("Japan")
    assert country.name == "Japan"

def test_country_fetch_currency():
    """Test that the fetched country includes 'USD' in its currency for the USA."""
    country = Country.fetch_country("USA")
    assert "USD" in country.currency

def test_country_fetch_population():
    """Test that the population value returned for France is greater than 0."""
    country = Country.fetch_country("France")
    assert country.population > 0
