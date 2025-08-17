# Futbol Tahminleri Uygulaması (KivyMD + FastAPI)

Bu proje, KivyMD ile geliştirilen mobil uygulama ve FastAPI tabanlı bir backend içerir. Günlük tahmin verileri CSV ile içe aktarılır, üyelik (abonelik) tabanlı erişim modeli mevcuttur. İlk sürümde IAP (in-app purchase) yer tutucu olarak planlanmıştır.

## Yapı

- `app/` — KivyMD mobil uygulama
  - `main.py` — uygulama girişi ve ekran yönetimi
  - `services/` — API istemcisi, i18n, auth yardımcıları
  - `i18n/` — `tr.json` (varsayılan), `en.json` (genişlemeye hazır)
- `server/` — FastAPI backend
  - `main.py` — FastAPI uygulaması ve CORS
  - `db.py` — veritabanı bağlantısı (SQLModel + SQLite)
  - `models.py` — veri modelleri (users, matches, predictions)
  - `schemas.py` — Pydantic şemaları
  - `auth.py` — JWT, parola hash, bağımlılıklar
  - `routers/` — `auth.py`, `matches.py`, `admin.py`
- `samples/` — örnek CSV

## Veri Şeması (CSV)

Zorunlu başlıklar:

```
match_id,match_date_utc,league,home_team,away_team,kickoff_utc,tip_type,tip_value,confidence_percent,odds_decimal,analysis_note,is_premium
```

Örnek satır:

```
12345,2025-01-31,Super Lig,Fenerbahce,Galatasaray,2025-01-31T17:00:00Z,over_under,Over 2.5,72,1.85,Derbi,True
```

- `is_premium`: True/False (üye olmayanlara gizlenecek içerik)

## Hızlı Başlangıç

### Backend (FastAPI)

Gereksinimler (öneri: Python 3.10+). Aşağıdaki paketleri kurun:
- fastapi, uvicorn[standard], sqlmodel, passlib[bcrypt], python-jose, python-multipart

Geliştirme sunucusu (kökten çalıştırma):
```
uvicorn betapp.server.main:app --reload
```

Ya da `betapp/` dizinine geçerek:
```
cd betapp
uvicorn server.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

### Mobil Uygulama (KivyMD)

Gereksinimler:
- kivy, kivymd, requests

Çalıştırma (kökten):
```
python betapp/app/main.py
```

`API_BASE_URL` varsayılan `http://127.0.0.1:8000`. Gerekirse ortam değişkeni ile değiştirin:
```
# Windows PowerShell
$env:API_BASE_URL="http://192.168.1.10:8000"; python betapp/app/main.py
# macOS/Linux
API_BASE_URL="http://192.168.1.10:8000" python betapp/app/main.py
```

## Üyelik Modeli

İlk sürüm: backend üzerinde `subscription_expires_at` alanı ile üyelik kontrolü. IAP entegrasyonu sonraki sürümde eklenecek (Google Play / App Store faturalarının sunucu doğrulaması ile).

## Lokalizasyon (i18n)

- Varsayılan dil Türkçe (`i18n/tr.json`).
- Anahtar-temelli çeviri altyapısı hazır; `en.json` ile genişletilebilir.

## Notlar

- Geliştirme veritabanı: SQLite. Üretimde PostgreSQL önerilir.
- CSV importu için `/admin/import` endpoint'i (admin rolü gerekir).
- CORS varsayılan olarak tüm kökenlere açık (geliştirme için). Üretimde kısıtlayın.
