import pandas as pd

df = pd.read_csv("temiz_ulkeler.csv")

print("--- En kalabalık 5 ülke ---")
print(df.sort_values("nufus_milyon", ascending = False).head(5)[["ulke", "nufus_milyon"]])

print("--- Kıtaya göre ülke sayısı---")
print(df["kita"].value_counts())

print("--- Kıtaya göre toplam nüfus(milyon) ---")
print(df.groupby("kita")["nufus_milyon"].sum().sort_values(ascending = False))