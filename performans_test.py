import sqlite3
import pandas as pd
import time 

df = pd.read_csv("satislar.csv")
print(f"Veri okundu: {len(df)} satır")

baglanti = sqlite3.connect("satislar.db")
df.to_sql("satislar", baglanti, if_exists="replace", index=False)
print("SQLite veritabanına yüklendi")

baglanti.close()

baglanti = sqlite3.connect("satislar.db")
imlec = baglanti.cursor()

print("--- INDEX'SİZ ARAMA ---")
baslangic = time.perf_counter()

for _ in range(1000):
    imlec.execute("""
    SELECT *
    FROM satislar
    WHERE musteri_id = 4321
    """)
    sonuclar = imlec.fetchall()

bitis = time.perf_counter()  
print(f"Bulunan kayıt: {len(sonuclar)}")
print(f"Toplam süre (1000 sorgu): {bitis - baslangic:.4f} saniye")
print(f"Ortalama süre (1 sorgu): {(bitis - baslangic) / 1000:.6f} saniye")
baglanti.close()


baglanti = sqlite3.connect("satislar.db")
imlec = baglanti.cursor()

imlec.execute("CREATE INDEX idx_musteri ON satislar(musteri_id)")
baglanti.commit()
print("Index oluşturuldu: idx_musteri(musteri_İd sütununa)")

baglanti.close()


baglanti = sqlite3.connect("satislar.db")
imlec = baglanti.cursor()

print("--- INDEX'Lİ ARAMA ---")
baslangic = time.perf_counter()

for _ in range(1000):
    imlec.execute("""
    SELECT *
    FROM satislar
    WHERE musteri_id = 4321
    """)
    sonuclar = imlec.fetchall()

bitis = time.perf_counter()
print(f"Bulunan kayıt: {len(sonuclar)}")
print(f"Toplam süre (1000 sorgu): {bitis - baslangic:.4f} saniye")
print(f"Ortalama süre (1 sorgu): {(bitis - baslangic) / 1000:.6f} saniye")

baglanti.close()


baglanti = sqlite3.connect("satislar.db")
imlec = baglanti.cursor()

print("--- Sorgu Planı (index'li) ---")
imlec.execute("""
EXPLAIN QUERY PLAN
SELECT * FROM satislar WHERE musteri_id = 4321
""")
for satir in imlec.fetchall():
    print(satir)

baglanti.close()