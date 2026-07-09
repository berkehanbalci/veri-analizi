# Veri Analizi — Ülkeler

Pandas ile bir ülke veri seti üzerinde veri okuma, temizleme ve analiz çalışması. Gerçek dünya verisinin nasıl keşfedildiğini, kirli/eksik değerlerin nasıl temizlendiğini ve gruplama (groupby) ile nasıl özet çıkarıldığını gösterir.

## Kullanılan Teknolojiler

- Python
- Pandas (veri işleme ve analiz)

## Proje Yapısı

```
veri-analizi/
├── ulkeler.csv       # Ülke veri seti (nüfus, yüzölçümü, GSYİH, kıta, başkent)
├── ulke_analiz.py    # Ana analiz: okuma, temizlik, gruplama
├── ilk_pandas.py     # Pandas temelleri (DataFrame, filtreleme, sıralama)
└── README.md
```

## Kurulum

```
pip install pandas
```

## Çalıştırma

```
python ulke_analiz.py
```

## Ne Yapıyor?

### 1. Veri Okuma ve Keşif
- CSV dosyasını okur (`read_csv`)
- Verinin boyutunu, sütunlarını ve tiplerini inceler (`head`, `shape`, `info`)

### 2. Veri Temizliği
Gerçek veri kirlidir. Bu projede iki tür kirlilik ele alınır:
- **Eksik veri** (boş hücreler): `isnull` ile tespit edilir
- **Hatalı veri** (dolu ama mantıksız, örneğin negatif nüfus): mantık kontrolüyle tespit edilir

Temizlik doğru sırayla yapılır:
1. Ülke adı (kimlik) eksik olan satırlar silinir — kurtarılamaz
2. Eksik sayısal değerler ortalama ile doldurulur (`fillna`) — böylece satır korunur
3. Eksik metin değerleri "Bilinmiyor" ile doldurulur
4. Hatalı (negatif nüfus) satırlar silinir

> Not: Sıra önemlidir. Önce doldurma, sonra silme yapılır; çünkü eksik (NaN) değerler
> sayısal karşılaştırmalarda beklenmedik şekilde elenebilir.

### 3. Analiz
- En kalabalık ülkeler (`sort_values`)
- Kıtaya göre ülke sayısı (`value_counts`)
- Kıtaya göre toplam nüfus (`groupby` + `sum`)

## Öğrenilen Kavramlar

- DataFrame, Series
- Sütun seçme ve satır filtreleme
- Eksik ve hatalı veri tespiti/temizliği
- `fillna` ile eksik değer doldurma (imputation)
- `groupby` ile gruplama ve özetleme
- Method chaining (zincirleme işlemler)