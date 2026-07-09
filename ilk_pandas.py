import pandas as pd

veri = {
    "ad": ["Ali", "Ayşe", "Mehmet", "Fatma"],
    "yas": [25, 30, 35, 28],
    "sehir": ["İstanbul", "Ankara", "İzmir", "Bursa"]
}

df = pd.DataFrame(veri)

print(df)

print("--- Sadece yaşlar ---")
print(df["yas"])

print("--- 30 yaşından büyükler ---")
print(df[df["yas"] > 30])

print("--- Yaşa göre sıralı ---")
print(df.sort_values("yas"))

print("--- Yaş istatistikleri ---")
print(df["yas"].describe())