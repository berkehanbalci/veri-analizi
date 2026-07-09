import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("temiz_ulkeler.csv")

en_kalabalik = df.sort_values("nufus_milyon", ascending = False).head(10)

plt.figure(figsize=(12, 6))
plt.bar(en_kalabalik["ulke"], en_kalabalik["nufus_milyon"], color="steelblue")
plt.title("En Kalabalık 10 Ülke")
plt.xlabel("Ülke")
plt.ylabel("Nüfus (milyon)")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.savefig("en_kalabalik_ulkeler.png")
plt.show()