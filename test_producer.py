import requests
import json
import time

API_KEY = "8ea38794feb15127d37452b4dafe7226"

MIASTA = [
    # Warszawa i okolice
    {"name": "Warszawa",  "lat": 52.23, "lon": 21.01},
    {"name": "Piaseczno", "lat": 52.08, "lon": 21.02},
    {"name": "Legionowo", "lat": 52.40, "lon": 20.93},

    # Krakow i okolice
    {"name": "Krakow",      "lat": 50.06, "lon": 19.94},
    {"name": "Wieliczka",   "lat": 49.99, "lon": 20.07},
    {"name": "Niepolomice", "lat": 50.06, "lon": 20.22},

    # Gdansk i okolice
    {"name": "Gdansk", "lat": 54.35, "lon": 18.65},
    {"name": "Gdynia", "lat": 54.52, "lon": 18.53},
    {"name": "Sopot",  "lat": 54.44, "lon": 18.56},

    # Wroclaw i okolice
    {"name": "Wroclaw",   "lat": 51.11, "lon": 17.04},
    {"name": "Dlugoleka", "lat": 51.18, "lon": 17.18},
    {"name": "Sobotka",   "lat": 50.91, "lon": 16.74},

    # Poznan i okolice
    {"name": "Poznan",   "lat": 52.41, "lon": 16.93},
    {"name": "Swarzedz", "lat": 52.41, "lon": 17.08},
    {"name": "Mosina",   "lat": 52.25, "lon": 16.85},

    # Szczecin i okolice
    {"name": "Szczecin", "lat": 53.43, "lon": 14.55},
    {"name": "Police",   "lat": 53.55, "lon": 14.57},
    {"name": "Stargard", "lat": 53.34, "lon": 15.05},
]

def pobierz_pogode(miasto):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": miasto["lat"],
        "lon": miasto["lon"],
        "appid": API_KEY,
        "units": "metric",
        "lang": "pl"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"blad dla {miasto['name']}: {response.status_code}")
        return None
    return response.json()

def parsuj_dane(raw, nazwa_miasta):
    dane = {
        "city":                nazwa_miasta,
        "lat":                 raw["coord"]["lat"],
        "lon":                 raw["coord"]["lon"],
        "timestamp":           time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(raw["dt"])),
        "temp":                raw["main"]["temp"],
        "feels_like":          raw["main"]["feels_like"],
        "humidity":            raw["main"]["humidity"],
        "pressure":            raw["main"]["pressure"],
        "weather_main":        raw["weather"][0]["main"],
        "weather_description": raw["weather"][0]["description"],
        "wind_speed":          raw["wind"]["speed"],
        "wind_gust":           raw["wind"].get("gust", 0),
        "rain_1h":             raw.get("rain", {}).get("1h", 0),
        "snow_1h":             raw.get("snow", {}).get("1h", 0),
        "clouds":              raw["clouds"]["all"],
        "visibility":          raw.get("visibility", 0),
    }
    return dane

for miasto in MIASTA:
    raw = pobierz_pogode(miasto)
    if raw is None:
        continue
    dane = parsuj_dane(raw, miasto["name"])
    print(f"miasto:       {dane['city']}")
    print(f"wspolrzedne:  {dane['lat']}, {dane['lon']}")
    print(f"czas pomiaru: {dane['timestamp']}")
    print(f"temperatura:  {dane['temp']} C")
    print(f"odczuwalna:   {dane['feels_like']} C")
    print(f"wilgotnosc:   {dane['humidity']} %")
    print(f"cisnienie:    {dane['pressure']} hPa")
    print(f"pogoda:       {dane['weather_description']}")
    print(f"wiatr:        {dane['wind_speed']} m/s")
    print(f"porywy:       {dane['wind_gust']} m/s")
    print(f"deszcz:       {dane['rain_1h']} mm/h")
    print(f"snieg:        {dane['snow_1h']} mm/h")
    print(f"zachmurzenie: {dane['clouds']} %")
    print(f"widocznosc:   {dane['visibility']} m")
    print("---")