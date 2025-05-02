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
            
def update_recent_list():
    """Refreshes the recent search history UI with flags and country names, allowing users to reselect previous searches."""
    for widget in recent_list_frame.winfo_children():
        widget.destroy()

    def make_click_handler(entry):
        return lambda e: (
            entry_country.delete(0, tk.END),
            entry_country.insert(0, entry)
        )

    for country_name in recent_searches:
        row = tk.Frame(recent_list_frame, bg="#1e293b")
        row.pack(fill="x", pady=3, padx=4)

        try:
            response = requests.get(recent_flags[country_name])
            img_data = Image.open(BytesIO(response.content)).resize((28, 18))
            flag_img = ImageTk.PhotoImage(img_data)
            flag_label = tk.Label(row, image=flag_img, bg="#1e293b")
            flag_label.image = flag_img
            flag_label.pack(side="left", padx=6)
        except:
            flag_label = tk.Label(row, text="🏳️", bg="#1e293b", fg="white")
            flag_label.pack(side="left", padx=6)

        name_label = tk.Label(row, text=country_name, font=("Segoe UI", 11), fg="white", bg="#1e293b", cursor="hand2")
        name_label.pack(side="left", padx=6)
        name_label.bind("<Button-1>", make_click_handler(country_name))
        row.bind("<Button-1>", make_click_handler(country_name))

def update_flag(url):
    """Updates and displays the country flag image in the GUI based on the selected country's flag URL."""
    try:
        response = requests.get(url)
        img_data = Image.open(BytesIO(response.content)).resize((40, 25))
        flag = ImageTk.PhotoImage(img_data)
        flag_img_label.config(image=flag)
        flag_img_label.image = flag
        flag_text_label.configure(text=entry_country.get().title())
    except:
        flag_img_label.config(image="")
        flag_text_label.configure(text=entry_country.get().title())
def save_map():
    """Opens a file dialog to allow the user to save the currently generated interactive map as an HTML file."""
    global current_map_view
    if not current_map_view:
        messagebox.showinfo("Info", "Please explore a country first.")
        return
    filepath = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML file", "*.html")])
    if filepath:
        current_map_view.save_map_as(filepath)
        messagebox.showinfo("Saved", f"Map saved at:\n{filepath}")
        
# UI setup
root = ctk.CTk()
root.title("🌍 Globe IO")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

bg_image = Image.open("planet-earth.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

card = ctk.CTkFrame(root, fg_color="#0f172a", border_color="#38bdf8", border_width=3)
card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5, relheight=0.6)

title = ctk.CTkLabel(card, text="🌐 Globe IO: Interactive Map Explorer", font=ctk.CTkFont(size=35, weight="bold"))
title.pack(pady=15)

entry_country = ctk.CTkEntry(card, width=320, font=ctk.CTkFont(size=13), placeholder_text="Enter Country Name")
entry_country.pack(pady=10)
entry_country.bind("<Return>", lambda event: explore_country())

recent_label = ctk.CTkLabel(card, text="🔘 Recent Searches", font=("Segoe UI",15, "bold"), text_color="white")
recent_label.pack()

# Scrollable recent search frame (narrow)
recent_container = ctk.CTkFrame(card, fg_color="#0f172a")
recent_container.pack(pady=2)

recent_list_outer = tk.Frame(recent_container, bg="#1e293b", height=90, width=250)
recent_list_outer.pack()

recent_canvas = tk.Canvas(recent_list_outer, height=90, width=250, bg="#1e293b", highlightthickness=0)
scrollbar = tk.Scrollbar(recent_list_outer, orient="vertical", command=recent_canvas.yview)
recent_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
recent_canvas.pack(side="left", fill="both", expand=True)

recent_list_frame = tk.Frame(recent_canvas, bg="#1e293b", width=250)
recent_canvas.create_window((0, 0), window=recent_list_frame, anchor="nw")

def on_frame_configure(event):
    """Automatically resizes the scrollable area of the recent search list when its content changes."""
    recent_canvas.configure(scrollregion=recent_canvas.bbox("all"))

recent_list_frame.bind("<Configure>", on_frame_configure)

flag_frame = ctk.CTkFrame(card, fg_color="#0f172a")
flag_frame.pack(pady=4)
flag_img_label = tk.Label(flag_frame, bg="#0f172a")
flag_img_label.pack(side="left", padx=4)
flag_text_label = ctk.CTkLabel(flag_frame, text="", font=ctk.CTkFont(size=13, weight="bold"))
flag_text_label.pack(side="left", padx=4)

mapview_label = ctk.CTkLabel(card, text="🗺️Choose Your Map View Style:", font=("Segoe UI",15, "bold"), text_color="white")
mapview_label.pack(pady=(2, 0))

view_var = ctk.StringVar(value="Hybrid")
view_menu = ctk.CTkOptionMenu(master=card,
                              values=["Default", "Roadmap", "Satellite", "Hybrid"],
                              variable=view_var,
                              width=220,
                              fg_color="#1e293b",
                              button_color="#0ea5e9",
                              button_hover_color="#38bdf8",
                              text_color="white")
view_menu.pack(pady=6)

btn_frame = ctk.CTkFrame(card, fg_color="#0f172a")
btn_frame.pack(pady=10)

explore_btn = ctk.CTkButton(btn_frame, text="🌍Explore with Globe IO", command=explore_country, width=180, height=40, font=ctk.CTkFont(size=13, weight="bold"))
explore_btn.pack(side="left", padx=6)

save_btn = ctk.CTkButton(btn_frame, text="💾Save Map", command=save_map, width=150, height=40, font=ctk.CTkFont(size=13, weight="bold"))
save_btn.pack(side="left", padx=6)

currency_frame = ctk.CTkFrame(card, fg_color="#0f172a")
currency_frame.pack(pady=5, fill="both", expand=False)

root.mainloop()



