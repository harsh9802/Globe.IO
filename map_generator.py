import folium
from folium import IFrame
import shutil
import webbrowser
from folium.plugins import MiniMap

def create_map(country_name, latitude, longitude, country_info, view_type="Hybrid"):
    """Generates an interactive HTML map using Folium with a marker, country details, fun fact card, minimap, and tile layer."""
    tiles_dict = {
        "Roadmap": "http://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        "Satellite": "http://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        "Hybrid": "http://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        "Default": "OpenStreetMap"
    }
    selected_tile = tiles_dict.get(view_type, "OpenStreetMap")

    country_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=6,
        tiles=selected_tile if view_type == "Default" else None,
        min_zoom=2,
        max_zoom=18,
        max_bounds=True,
        no_wrap=True
    )

    if view_type != "Default":
        folium.TileLayer(
            tiles=selected_tile,
            attr="Google Maps",
            name=f"{view_type} View",
            control=True,
            no_wrap=True
        ).add_to(country_map)
    minimap = MiniMap(toggle_display=True, position="bottomright", width=150, height=150)
    country_map.add_child(minimap)
    flag_url = country_info.get("Flag", "")
    flag_img_html = f'<div style="text-align:center;"><img src="{flag_url}" alt="Flag" style="width:80px;margin:8px auto;border-radius:4px;"></div>' if flag_url.startswith("http") else ""
    wiki_url = f"https://en.wikipedia.org/wiki/{country_info['Name'].replace(' ', '_')}"
    fun_fact = country_info.get("Fun Fact", "No fun fact available.")
    card_html = f'''
    <html>
    <head>
    <style>
    /* Blue close button styling for Leaflet popup */
    .leaflet-popup-close-button {{
      color: #0078d7 !important;
      font-size: 20px !important;
      font-weight: bold !important;
      padding-right: 6px;
    }}
    .leaflet-popup-close-button:hover {{
      color: #005a9e !important;
    }}

    html, body {{
      margin: 0;
      padding: 0;
    }}
    .flip-card {{
      width: 260px;
      height: 360px;
      perspective: 1000px;
      margin: 0 auto;
    }}
    .flip-card-inner {{
      width: 100%;
      height: 100%;
      transition: transform 0.8s;
      transform-style: preserve-3d;
      position: relative;
    }}
    .flip-card-front, .flip-card-back {{
      position: absolute;
      width: 100%;
      height: 100%;
      backface-visibility: hidden;
      border-radius: 10px;
      box-sizing: border-box;
      padding: 12px;
      font-family: 'Segoe UI', sans-serif;
      box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}
    .flip-card-front {{
      background-color: white;
      color: black;
      border: 2px solid #003366;
    }}
    .flip-card-back {{
      background-color: #f0f8ff;
      transform: rotateY(180deg);
      border: 2px solid #003366;
    }}
    h4 {{
      font-size: 16px;
      text-align: center;
      margin: 4px 0;
      color: #003366;
      font-weight: bold;
    }}
    p {{
      font-size:15px;
      margin: 4px 0;
      padding: 2px;
    }}
    .flip-btn {{
      display: block;
      margin: 12px auto 0;
      padding: 6px 10px;
      font-size: 12px;
      width:95%;
      background: #000080;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
    }}
    a {{
      font-size: 12px;
      color: #1e90ff;
      font-weight: bold;
      text-decoration: none;
    }}
    </style>
    <script>
    function flipCard(btn) {{
        const cardInner = btn.closest('.flip-card').querySelector('.flip-card-inner');
        cardInner.style.transform = 
          cardInner.style.transform === "rotateY(180deg)" ? "rotateY(0deg)" : "rotateY(180deg)";
    }}
    </script>
    </head>
    <body>
    <div class="flip-card">
      <div class="flip-card-inner">
        <div class="flip-card-front">
          {flag_img_html}
          <h4>{country_info['Name']}</h4>
          <p><b>Capital:</b> {country_info['Capital']}</p>
          <p><b>Region:</b> {country_info['Region']}</p>
          <p><b>Population:</b> {country_info['Population']:,}</p>
          <p><b>Area:</b> {country_info['Area']} km²</p>
          <p><b>Currency:</b> {country_info['Currency']}</p>
          <p><b>Timezone:</b> {country_info['Timezone']}</p>
          <button class="flip-btn" onclick="flipCard(this)">Show Fun Fact</button>
        </div>
        <div class="flip-card-back">
          <h4><u>Fun Fact</u></h4>
          <p>{fun_fact}</p>
          <p style="text-align:right;"><a href="{wiki_url}" target="_blank">📚 Read More On Wikipedia</a></p>
          <button class="flip-btn" onclick="flipCard(this)">Back</button>
        </div>
      </div>
    </div>
    </body>
    </html>
    '''
    iframe = IFrame(card_html, width=280, height=390)
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(iframe),
        tooltip=f"{country_info['Name']} Info",
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(country_map)

    folium.LayerControl(position="topright", collapsed=False).add_to(country_map)
    country_map.save("map.html")


# NEW CLASS: MapView
class MapView:
    """Handles map generation and rendering logic for a country."""

    def __init__(self, country_name, latitude, longitude, map_type="Hybrid"):
        self._country_name = country_name
        self._latitude = latitude
        self._longitude = longitude
        self._map_type = map_type

