import folium

def create_map(country_name, latitude, longitude, country_info, view_type="Hybrid"):
    """Generate an interactive map with layers, minimap, and a fun fact modal popup."""
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

    folium.Marker(
        location=[latitude, longitude],
        popup=country_info["Name"],
        tooltip=f"{country_info['Name']} Info",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(country_map)

    folium.LayerControl(position="topright", collapsed=False).add_to(country_map)

    country_map.save("map.html")
