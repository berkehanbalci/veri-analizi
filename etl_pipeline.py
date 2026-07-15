import requests
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime

load_dotenv()

def extract(sehirler):
    """API'lerden şehirlerin hava durumunu çeker"""
    print("[EXTRACT] Veri çekiliyor...")
    sonuclar = []

    for sehir_adi in sehirler:
        try:
            geo_url =  geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_yanit = requests.get(geo_url, params={"name": sehir_adi, "count": 1})
            geo_veri = geo_yanit.json()

            if "results" not in geo_veri or len(geo_veri["results"]) == 0:
                print(f"[EXTRACT] UYARI: '{sehir_adi}' bulunamadı, atlanıyor")
                continue


            konum = geo_veri["results"][0]     

            hava_url = "https://api.open-meteo.com/v1/forecast"
            hava_yanit = requests.get(hava_url, params={
                    "latitude": konum["latitude"],
                    "longitude": konum["longitude"],
                    "current": "temperature_2m,wind_speed_10m,relative_humidity_2m"
            })

            hava = hava_yanit.json()["current"]

            sonuclar.append({
                    "sehir": sehir_adi,
                    "sicaklik_c": hava["temperature_2m"],
                    "ruzgar": hava["wind_speed_10m"],
                    "nem": hava["relative_humidity_2m"]
            })
        except EXCEPTİON as hata:
            print(f"[EXTRACT] HATA: '{sehir_adi}' için veri alınamadı: {hata}")
            continue
    print(f"[EXTRACT] {len(sonuclar)} şehir başarıyla çekildi")
    return pd.DataFrame(sonuclar)

def transform(df):
    """Veriyi dönüştürür: Fahrenheit ekler, kategori belirler, zaman damgası ekler"""
    print("[TRANSFORM] Veri dönüştürülüyor...")

    df["sicaklik_f"] = (df["sicaklik_c"] * 9/5) + 32

    def kategori_belirle(sicaklik):
        if sicaklik < 15:
            return "Soğuk"
        elif sicaklik < 25:
            return "Ilık"
        else:
            return "Sıcak"

    df["kategori"] = df["sicaklik_c"].apply(kategori_belirle)
    df["cekilme_zamani"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print("[TRANSFORM] Tamamlandı")
    return df

def load(df):
    """Veriyi PostgreSQL'e yükler"""
    print("[LOAD] PostgreSQL'e yükleniyor...")

    engine = create_engine(
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

    df.to_sql("hava_durumu_log", engine, if_exists= "append", index = False)

    print(f"[LOAD] {len(df)} satir yüklendi")

def pipeline_calistir(sehirler):
    """Tam ETL akışını çalıştırır"""
    print("=" * 40)
    print("ETL PIPELINE BAŞLIYOR")
    print("=" * 40)

    df_ham = extract(sehirler)
    df_donusturulmus = transform(df_ham)
    load(df_donusturulmus)

    print("=" * 40)
    print("PIPELINE TAMAMLANDI")
    print("=" * 40)
    return df_donusturulmus

if __name__ == "__main__":
    sehirler = ["Ankara", "İstanbul", "İzmir", "Antalya", "Trabzon"]
    sonuc = pipeline_calistir(sehirler)
    print(sonuc)




