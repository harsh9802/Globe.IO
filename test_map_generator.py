from map_generator import MapView
import os

def test_mapview_attributes():
    """Test that the MapView object initializes with the correct country name."""
    mv = MapView("India", 20.5, 78.9, "Hybrid")
    assert mv._country_name == "India"

def test_mapview_latitude():
    """Test that the MapView object stores the correct latitude value."""
    mv = MapView("Brazil", -14.2, -51.9, "Satellite")
    assert mv._latitude == -14.2

def test_mapview_type():
    """Test that the MapView object stores the correct map type."""
    mv = MapView("France", 48.8, 2.3, "Default")
    assert mv._map_type == "Default"

def test_save_map_html(tmp_path):
    """
    Test that the save_map_as method successfully saves a copy of map.html
    to the provided output path.
    """
    mv = MapView("Dummy", 0, 0)
    with open("map.html", "w") as f:
        f.write("<html>Map</html>")
    save_path = tmp_path / "output_map.html"
    mv.save_map_as(str(save_path))
    assert save_path.exists()

def test_generate_map_creates_file():
    """
    Test that the create_map function generates a map.html file
    using valid country information and coordinates.
    """
    from map_generator import create_map
    country_info = {
        "Name": "Italy",
        "Capital": "Rome",
        "Region": "Europe",
        "Population": 60000000,
        "Area": 301340,
        "Currency": "Euro (EUR) €",
        "Timezone": "UTC+1",
        "Flag": "https://flagcdn.com/it.png",
        "Fun Fact": "Italy has many UNESCO sites."
    }
    create_map("Italy", 41.9, 12.5, country_info, "Hybrid")
    assert os.path.exists("map.html")

