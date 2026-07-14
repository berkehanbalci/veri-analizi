import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


df = pd.read_csv("satislar.csv")
print(f"Okundu: {len(df)} satır")


df.to_sql("satislar", engine, if_exists="replace", index = False)
print("PostgreSQL'e yüklendi: 'satislar' tablosu")


kontrol = pd.read_sql("SELECT COUNT(*) FROM satislar", engine)
print(f"PostgreSQL'deki satır sayısı: {kontrol.iloc[0,0]}")


# ============ SORGULAR ============

print("--- Şehre göre toplam satış tutarı (ilk 5) ---")
sorgu1 = """
    SELECT sehir, SUM(adet * birim_fiyat) AS toplam_satis
    FROM satislar
    GROUP BY sehir
    ORDER BY toplam_satis DESC
    LIMIT 5
"""

sonuc1 = pd.read_sql(sorgu1, engine)
print(sonuc1)

print("--- En çok satılan 5 ürün (adet bazında) ---")
sorgu2 ="""
    SELECT urun, SUM(adet) AS toplam_adet
    FROM satislar
    GROUP BY urun
    ORDER BY toplam_adet DESC
    LIMIT 5
"""

sonuc2 = pd.read_sql(sorgu2, engine)
print(sonuc2)

print("--- 10000 TL üzeri tekil siparişler (adet) ---")
sorgu3 = """
    SELECT COUNT(*) AS siparis_sayisi
    FROM satislar
    WHERE (adet * birim_fiyat)  > 10000
"""

sonuc3 = pd.read_sql(sorgu3, engine)
print(sonuc3)