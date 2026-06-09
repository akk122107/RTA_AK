import requests

API_KEY = "8ea38794feb15127d37452b4dafe7226"

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "lat": 52.23,
    "lon": 21.01,
    "appid": API_KEY,
    "units": "metric",
    "lang": "pl"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("klucz dziala")
    print(f"miasto: {data['name']}")
    print(f"temperatura: {data['main']['temp']} C")
    print(f"pogoda: {data['weather'][0]['description']}")
    print(f"wiatr: {data['wind']['speed']} m/s")
else:
    print(f"blad {response.status_code}: {response.json()['message']}")