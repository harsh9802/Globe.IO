
# 🌍 Globe IO — Interactive Map Explorer

## 📌 Project Overview

**Globe IO** is a Python GUI-based application that allows users to explore any country in the world interactively using live map rendering, Wikipedia facts, national flags, and real-time currency exchange rates and saving a map functionality.

It utilizes multiple APIs (REST Countries, Wikipedia, ExchangeRate), interactive Folium maps, and modern `customtkinter` design, fulfilling all course project requirements including GUI, advanced module usage, file organization, and unit testing.

---

## 🧩 Key Features

- 🌐 Live map for any country with satellite/roadmap/hybrid view  
- 🧠 Wikipedia-powered fun facts with flip card on marker click  
- 🇺🇸 Flag preview beside the country name  
- 💱 Currency exchange conversion (USD, GBP, JPY, EUR)  
- 🔁 Recent country search history with flag icons  
- 💾 Save map as `.html`  
- 🧪 Fully tested using `pytest`  

---

## 🎯 GUI Interactivity

The GUI is built with `customtkinter` and includes:

- Entry box for country input  
- Dropdown menu for map view  
- Explore button to render map and info  
- Save map button  
- Scrollable list of recent searches  
- Currency conversion table  
- Flag image and name displayed on the UI

> Total: ✅ **8 interactive elements**

---

## 🧠 Technologies & Advanced Modules

| Technology         | Purpose                            |
|-------------------|------------------------------------|
| `customtkinter`   | Modern GUI layout and widgets       |
| `folium`        | Map rendering (Advanced module)     |
| `requests`        | API calls to REST and ExchangeRate  |
| `pycountry`       | Normalize country names and codes   |
| `wikipediaapi`    | Fetch Wikipedia summary for country |
| `Pillow` (PIL)    | Flag image loading and display      |
| `dotenv`          | Load environment variables          |
| `pytest`          | Unit testing                        |

✅ `folium` is the **advanced module**, used for interactive mapping.

---

## 📁 File Structure

```
GlobeIO/
├── main.py                  # Main GUI logic
├── country_data.py          # Country data class, API logic
├── map_generator.py         # Map rendering logic
├── test_country_data.py     # Unit tests for data logic
├── test_map_generator.py    # Unit tests for map logic
├── planet-earth.png         # Background image
├── .env                # Contains API key for currency API
├── README.md                # This file
```

---

## 🏗️ Classes & Modular Design

- `Country` (in `country_data.py`):  
  Stores all country attributes and fun facts.

- `MapView` (in `map_generator.py`):  
  Handles rendering and saving maps for each country.

All logic is divided cleanly across modules.

---

## 🧪 Pytest Testing

We have created **5+ tests** for the project:

-  `test_country_data.py`:  
  - Name normalization  
  - Country object instantiation  
  - Currency and population checks

-  `test_map_generator.py`:  
  - MapView attributes  
  - Map file generation  
  - HTML save test

To run tests:
```bash
pytest test_country_data.py
pytest test_map_generator.py
```

---

## 🔐 API Setup (.env)

You must create a `.env` file to load your **ExchangeRate.host API key**:

### 📄 `.env`
```
API_KEY="your_api_key_here"
```

This key is used in `country_data.py` to perform currency conversion using:
```python
from dotenv import load_dotenv
ACCESS_KEY = os.getenv('API_KEY')
```

---

## 🚀 How to Run

1. **Clone the project**:
```bash
git clone https://github.com/harsh9802/Globe.IO
cd Globe.IO
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python main.py
```

---
