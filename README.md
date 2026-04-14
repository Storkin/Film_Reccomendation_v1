#  CineTrack — Film Öneri ve Takip Uygulaması

IMDb Top 1000 listesini temel alan, nesne yönelimli Python backend ve modern web arayüzüne sahip tam yığın film yönetim uygulaması.

## Özellikler

- Tür, minimum puan, yıl ve anahtar kelimeye göre film filtreleme
- Film detay görünümü (yönetmen, oyuncular, özet, süre)
- İzlenenler listesi — oturumlar arası JSON ile kalıcı depolama
- Kişisel puan (0–10) ve yorum ekleme
- Sinema temalı karanlık web arayüzü

## Teknolojiler

| Katman | Teknoloji |
|---|---|
| Backend | Python 3, Flask |
| Veri İşleme | Pandas |
| Veri Depolama | JSON |
| Frontend | HTML5, CSS3, Vanilla JavaScript |

## Kurulum

```bash
pip install flask pandas
python app.py
```

Tarayıcıda `http://127.0.0.1:5000` adresini aç.

## Mimari

`Film` temel sınıfından Action, Comedy, Thriller, Horror, Sci-Fi dahil **14 tür alt sınıfı** türetilmiştir. Her alt sınıf `make_comment()` metodunu override ederek IMDb puanına dayalı özgün yorum üretir. `FilmManager` sınıfı filtreleme operasyonlarını yönetir; Flask REST API bu katmanı web'e açar.

```
proje.py        → OOP model katmanı (Film, User, FilmManager)
app.py          → Flask REST API
templates/      → HTML arayüzü
static/         → CSS ve JavaScript
films.json      → IMDb Top 1000 film verisi
user_data.json  → Kullanıcı izleme listesi ve yorumlar
```
