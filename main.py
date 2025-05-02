import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import re
import webbrowser
import geopy.geocoders
from country_data import Country, get_currency_conversion
from map_generator import MapView
import requests
from io import BytesIO

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

recent_searches = []
recent_flags = {}
current_map_view = None

def show_currency_conversion_table(base_currency, conversions):
    """Displays the currency conversion rates for a given base currency inside the application's GUI."""
    card.place_configure(relheight=0.85)
    for widget in currency_frame.winfo_children():
        widget.destroy()

    heading = ctk.CTkLabel(currency_frame, text=f"💱 Conversion Rates for 1 {base_currency}",
                           font=ctk.CTkFont(size=14, weight="bold"), text_color="white")
    heading.pack(pady=(0, 5))

    table_frame = ctk.CTkFrame(currency_frame, fg_color="#1e293b")
    table_frame.pack(padx=10, pady=10, fill="x")

    headers = ctk.CTkFrame(table_frame, fg_color="#273447")
    headers.pack(fill="x")
    ctk.CTkLabel(headers, text="Currency", width=150, anchor="w", font=("Segoe UI", 11, "bold")).pack(side="left", padx=1)
    ctk.CTkLabel(headers, text="Rate", width=150, anchor="e", font=("Segoe UI", 11, "bold")).pack(side="left", padx=1)

    for currency, rate in conversions.items():
        row = ctk.CTkFrame(table_frame, fg_color="#1e293b")
        row.pack(fill="x", pady=2)
        ctk.CTkLabel(row, text=currency, width=150, anchor="w", font=("Segoe UI", 11)).pack(side="left", padx=1)
        ctk.CTkLabel(row, text=rate, width=150, anchor="e", font=("Segoe UI", 11)).pack(side="left", padx=1)

def explore_country():
    """Fetches country data, displays the map, flag, currency info, and updates recent searches in the interface."""
    global current_map_view
    card.place_configure(relheight=0.6)

    country_name = entry_country.get().strip()
    if not country_name:
        messagebox.showerror("Input Error", "Enter a country name.")
        return
    if country_name.lower() == "uk":
        country_name = "gb"
    country = Country.fetch_country(country_name)
    if not country:
        messagebox.showerror("Not Found", "Country not found.")
        return

    geolocator = geopy.geocoders.Nominatim(user_agent="geoapi")
    location = geolocator.geocode(country.name)
    if not location:
        messagebox.showerror("Location Error", "Could not locate the country.")
        return

    map_view = MapView(country.name, location.latitude, location.longitude, map_type=view_var.get())
    map_view.generate_map(country)
    map_view.open_in_browser()
    current_map_view = map_view

    if country.name not in recent_searches:
        recent_searches.insert(0, country.name)
        recent_flags[country.name] = country.flag_url
        if len(recent_searches) > 3:
            removed = recent_searches.pop()
            recent_flags.pop(removed, None)

    update_recent_list()
    update_flag(country.flag_url)

    currency_code = re.search(r"\((.*?)\)", country.currency)
    if currency_code:
        conversions = get_currency_conversion(currency_code.group(1))
        if conversions:
            show_currency_conversion_table(currency_code.group(1), conversions)
