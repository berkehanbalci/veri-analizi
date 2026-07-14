# Veri Analizi — Ülkeler ve Performans

Pandas ile veri okuma, temizleme, analiz ve görselleştirme çalışması; ayrıca SQLite üzerinde büyük veriyle index kullanımının sorgu performansına etkisinin ölçülmesi.

## Kullanılan Teknolojiler

- Python
- Pandas (veri işleme ve analiz)
- Matplotlib (görselleştirme)
- SQLite (veritabanı, index performans testi)
- PostgreSQL (sunucu tabanlı veritabanı)
- SQLAlchemy (Pandas ↔ PostgreSQL köprüsü)
- python-dotenv (bağlantı bilgilerinin güvenli yönetimi)

## Proje Yapısı

```
veri-analizi/
├── ulkeler.csv               # Ham ülke veri seti (nüfus, yüzölçümü, GSYİH, kıta, başkent)
├── temiz_ulkeler.csv         # Temizlenmiş veri (temizle.py'nin çıktısı)
├── temizle.py                # Keşif + temizlik + doğrulama, temiz_ulkeler.csv üretir
├── ulke_analiz.py            # Temiz veri üzerinde analiz (sıralama, gruplama)
├── gorsellestir.py           # Temiz veri üzerinde grafik oluşturma
├── ilk_pandas.py             # Pandas temelleri (DataFrame, filtreleme, sıralama)
├── en_kalabalik_ulkeler.png  # Üretilen grafik
├── satislar.csv              # 50.000 satırlık büyük veri seti (performans testi için)
├── performans_test.py        # Index'siz/index'li sorgu süresi karşılaştırması
├── postgres_test.py          # PostgreSQL'e veri taşıma ve SQL sorguları
├── .env                      # Veritabanı bağlantı bilgileri (depoya dahil değildir)
└── README.md
```

Her dosyanın tek bir sorumluluğu vardır: `temizle.py` sadece temizler, `ulke_analiz.py` sadece analiz eder, `gorsellestir.py` sadece görselleştirir. Temizlik mantığı tek bir yerde tanımlıdır; diğer dosyalar doğrudan temizlenmiş veriyi (`temiz_ulkeler.csv`) okur.

`satislar.db` (SQLite veritabanı dosyası) `.gitignore` içindedir — `performans_test.py` çalıştırıldığında `satislar.csv`'den otomatik olarak yeniden oluşturulur, bu yüzden depoya dahil edilmez.

PostgreSQL bağlantı bilgileri (host, port, veritabanı adı, kullanıcı, şifre) `.env` dosyasında tutulur ve `python-dotenv` ile okunur; kod içinde hiçbir yerde şifre açık yazılmaz.

## Kurulum

```
pip install pandas matplotlib sqlalchemy psycopg2-binary python-dotenv
```

(`sqlite3` Python ile birlikte gelir, ayrıca kurulum gerekmez.)

PostgreSQL kuruluysa, proje klasöründe bir `.env` dosyası oluşturup bağlantı bilgilerini tanımlayın:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=veri_analizi_db
DB_USER=postgres
DB_PASSWORD=kendi-sifreniz
```

## Çalıştırma

Sırasıyla çalıştırın (temizlik önce yapılmalı, diğerleri temiz veriyi kullanır):

```
python temizle.py
python ulke_analiz.py
python gorsellestir.py
python performans_test.py
python postgres_test.py
```

## Ne Yapıyor?

### 1. Keşif ve Temizlik (`temizle.py`)
Önce ham veri incelenir (`shape`, `info`, `isnull`) — hangi sütunlarda ne kadar eksik olduğu görülür. Gerçek veride iki tür kirlilik ele alınır:
- **Eksik veri** (boş hücreler): `isnull` ile tespit edilir
- **Hatalı veri** (dolu ama mantıksız, örneğin negatif nüfus): mantık kontrolüyle tespit edilir

Temizlik doğru sırayla yapılır:
1. Ülke adı (kimlik) eksik olan satırlar silinir — kurtarılamaz
2. Eksik sayısal değerler ortalama ile doldurulur (`fillna`) — böylece satır korunur
3. Eksik metin değerleri "Bilinmiyor" ile doldurulur
4. Hatalı (negatif nüfus) satırlar silinir

> Not: Sıra önemlidir. Önce doldurma, sonra silme yapılır; çünkü eksik (NaN) değerler
> sayısal karşılaştırmalarda beklenmedik şekilde elenebilir.

Temizlik sonrası tekrar `isnull().sum()` ile doğrulanır, sonuç `temiz_ulkeler.csv` olarak kaydedilir.

### 2. Analiz (`ulke_analiz.py`)
Temiz veri üzerinde çalışır:
- En kalabalık ülkeler (`sort_values`)
- Kıtaya göre ülke sayısı (`value_counts`)
- Kıtaya göre toplam nüfus (`groupby` + `sum`)

### 3. Görselleştirme (`gorsellestir.py`)
Temiz veri üzerinde çubuk grafik oluşturur:

![En kalabalık 10 ülke](en_kalabalik_ulkeler.png)

Hindistan ve Çin, diğer ülkelerden belirgin şekilde ayrışıyor — dünya nüfusunun büyük kısmı bu iki ülkede yoğunlaşmış durumda.

### 4. Büyük Veri ve Performans (`performans_test.py`)
50.000 satırlık bir satış veri seti (`satislar.csv`) SQLite'a yüklenir (`to_sql`) ve aynı sorgu iki durumda karşılaştırılır:

1. **Index'siz arama** — veritabanı tabloyu baştan sona tarar (`SCAN`)
2. **Index'li arama** — `CREATE INDEX` ile oluşturulan index üzerinden doğrudan bulunur (`SEARCH`)

Gürültüyü azaltmak için her sorgu 1.000 kez tekrarlanır ve ortalama süre alınır (`time.perf_counter`). Ölçülen sonuç:

| Durum       | Ortalama sorgu süresi |
|-------------|------------------------|
| Index'siz   | ~0.0050 saniye         |
| Index'li    | ~0.00008 saniye        |

**~62 kat hızlanma.** `EXPLAIN QUERY PLAN` ile bu fark doğrulanır: index'siz durumda `SCAN satislar`, index'li durumda `SEARCH satislar USING INDEX idx_musteri` görülür.

> Not: 50.000 satırda fark zaten belirgin; gerçek dünyada milyonlarca satırlı tablolarda index eksikliği dakikalar süren sorgulara yol açabilir.

### 5. PostgreSQL Entegrasyonu (`postgres_test.py`)
SQLite'tan sunucu tabanlı bir veritabanına geçiş: `satislar.csv`, SQLAlchemy üzerinden PostgreSQL'e yüklenir (`to_sql`) ve satır sayısı geri okunarak doğrulanır.

Ardından tanıdık SQL kalıpları (`GROUP BY`, `SUM`, `WHERE`, `ORDER BY ... LIMIT`) PostgreSQL üzerinde çalıştırılır:
- Şehre göre toplam satış tutarı
- En çok satılan ürünler (adet bazında)
- Belirli bir tutarın üzerindeki siparişlerin sayısı

Bağlantı bilgileri kodun içine yazılmaz; `.env` dosyasından `python-dotenv` ile okunur — tıpkı bir API projesindeki gizli anahtar yönetimi gibi.

> Not: SQLite tek bir dosya olarak çalışırken, PostgreSQL bağımsız bir sunucu
> süreci olarak çalışır (host, port, kullanıcı, şifre gerektirir). Bu fark,
> küçük/tekil projeler ile çok kullanıcılı/production sistemler arasındaki
> temel ayrımlardan biridir.

## Öğrenilen Kavramlar

- DataFrame, Series
- Sütun seçme ve satır filtreleme
- Eksik ve hatalı veri tespiti/temizliği
- `fillna` ile eksik değer doldurma (imputation)
- `groupby` ile gruplama ve özetleme
- Method chaining (zincirleme işlemler)
- Matplotlib ile temel görselleştirme (çubuk grafik)
- Tek sorumluluk ilkesi: temizlik, analiz ve görselleştirmeyi ayrı dosyalara bölme
- Pandas → SQLite köprüsü (`to_sql`)
- Performans ölçümü (`time.perf_counter`, tekrarlı ölçüm ile gürültü azaltma)
- Index kavramı ve sorgu hızına etkisi
- `EXPLAIN QUERY PLAN` ile sorgu planını okuma (`SCAN` vs `SEARCH`)
- SQLite ile PostgreSQL arasındaki temel farklar (dosya tabanlı vs sunucu tabanlı)
- SQLAlchemy ile Pandas ↔ PostgreSQL köprüsü
- Bağlantı bilgilerinin `.env` ile güvenli yönetimi