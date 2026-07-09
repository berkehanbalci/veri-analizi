import pandas as pd

df = pd.read_csv("ulkeler.csv")

print("--- İlk 5 satır ---")
print(df.head())

print("--- Boyut (satır, sütun) ---")
print(df.shape)

print("--- Genel Bilgi ---")
print(df.info())

print("--- Eksik veri olan satırlar ---")
print(df[df.isnull().any(axis=1)])

print("--- Sütun başına eksik sayısı ---")
print(df.isnull().sum())

print("--- TEMİZLİK ---")
df_temiz = df.dropna(subset=["ulke"])
print(f"Ülke adı eksik satırlar silindi. Kalan: {len(df_temiz)} satır")

df_temiz["nufus_milyon"] = df_temiz["nufus_milyon"].fillna(df_temiz["nufus_milyon"].mean())
df_temiz["yuzolcumu_bin_km2"] = df_temiz["yuzolcumu_bin_km2"].fillna(df_temiz["yuzolcumu_bin_km2"].mean())
df_temiz["gsyih_milyar_dolar"] = df_temiz["gsyih_milyar_dolar"].fillna(df_temiz["gsyih_milyar_dolar"].mean())
print("2. Eksik sayısal değerler ortalama ile dolduruldu.")

df_temiz["baskent"] = df_temiz["baskent"].fillna("Bilinmiyor")
print("3. Eksik başkent 'Bilinmiyor' ile dolduruldu.")

df_temiz = df_temiz[df_temiz["nufus_milyon"] >= 0]
print(f"Hatalı (negatif nüfus) satırlar silindi. Kalan: {len(df_temiz)} satır")

print("--- Temizlik sonrası eksik kontrolü ---")
print(df_temiz.isnull().sum())


print("--- ANALİZ ---")

print("--- En kalabalık 5 ülke ---")
print(df_temiz.sort_values("nufus_milyon", ascending = False).head(5)[["ulke", "nufus_milyon"]])

print("--- Kıtaya göre ülke sayısı---")
print(df_temiz["kita"].value_counts())

print("--- Kıtaya göre toplam nüfus(milyon) ---")
print(df_temiz.groupby("kita")["nufus_milyon"].sum().sort_values(ascending = False))