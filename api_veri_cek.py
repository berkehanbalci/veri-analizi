import requests
import pandas as pd

def koordinat_bul(sehir_adi):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    yanit = requests.get(url, params={"name": sehir_adi, "count": 1})
    veri = yanit.json()

    sonuc = veri["results"][0]
    return sonuc ["latitude"], sonuc["longitude"]


def hava_durumu_getir(enlem, boylam):
    url = "https://api.open-meteo.com/v1/forecast"
    parametreler = {
        "latitude": enlem,
        "longitude": boylam,
        "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
    }
    yanit = requests.get(url, params=parametreler)
    return yanit.json()["current"]    

sehirler = ["Ankara", "İstanbul", "İzmir", "Antalya", "Trabzon"]
sonuclar = []

for sehir_adi in sehirler:
    enlem, boylam = koordinat_bul(sehir_adi)
    hava = hava_durumu_getir(enlem, boylam)

    sonuclar.append({
        "sehir": sehir_adi,
        "sicaklik": hava["temperature_2m"],
        "ruzgar": hava["wind_speed_10m"],
        "nem": hava["relative_humidity_2m"]
    })
    print(f"{sehir_adi}: {hava['temperature_2m']}°C (koordinat: {enlem}, {boylam})")

df = pd.DataFrame(sonuclar)
print("--- Tüm şehirler ---")
print(df)


df.to_csv("hava_durumu.csv", index=False, encoding="utf-8")
print("hava_durumu.csv kaydedildi")