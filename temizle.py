import pandas as pd

df = pd.read_csv("ulkeler.csv")
print(f"Ham veri: {len(df)} satır")

print("--- Ham veri boyutu ---")
print(df.shape)

print("--- Genel bilgi ---")
print(df.info())

print("--- Eksik veri olan satırlar ---")
print(df[df.isnull().any(axis=1)])

print("--- Sütun başına eksik sayısı ---")
print(df.isnull().sum())

print("--- TEMİZLİK ---")
df = df.dropna(subset=["ulke"])
df["nufus_milyon"] = df["nufus_milyon"].fillna(df["nufus_milyon"].mean())
df["yuzolcumu_bin_km2"] = df["yuzolcumu_bin_km2"].fillna(df["yuzolcumu_bin_km2"].mean())
df["gsyih_milyar_dolar"] = df["gsyih_milyar_dolar"].fillna(df["gsyih_milyar_dolar"].mean())
df["baskent"] = df["baskent"].fillna("Bilinmiyor")
df = df[df["nufus_milyon"] >= 0]

print("--- Temizlik sonrası eksik kontrolü ---")
print(df.isnull().sum())
print(f"Temiz veri: {len(df)} satır")

df.to_csv("temiz_ulkeler.csv", index=False, encoding="utf-8")
print("temiz_ulkeler.csv kaydedildi")