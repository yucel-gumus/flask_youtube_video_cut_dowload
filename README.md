# YouTube Video İndirici ve Kesici

Flask web uygulaması: YouTube URL'sinden **yt-dlp** ile indirme, isteğe bağlı **ffmpeg** ile zaman aralığına göre kesme; işler thread + in-memory job store ile arka planda yürür.

**GitHub:** [yucel-gumus/flask_youtube_video_cut_dowload](https://github.com/yucel-gumus/flask_youtube_video_cut_dowload)

[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/) [![Flask](https://img.shields.io/badge/Flask-2.2+-black.svg)](https://flask.palletsprojects.com/)

---

## Özellikler

- URL doğrulama (youtube.com / youtu.be)
- Zaman formatları: saniye, `MM:SS`, `HH:MM:SS`
- Job durumu: kuyruk, indirme, kesme, tamamlandı, hata — JSON polling
- İndirme linki tamamlanınca arayüzde
- `utils/youtube_utils.py`, `utils/ffmpeg_utils.py` modüler yapı
- Railway / benzeri PaaS için `Procfile` + `requirements.txt`

---

## Mimari

```
Browser (templates/)
    │ POST /process
    ▼
Flask app.py ──► threading.Thread
    │                ├── download_video (yt-dlp)
    │                └── cut_video (ffmpeg)
    ▼
jobs[job_id] dict ──► GET status / download
```

Üretimde ölçek için Redis/Celery önerilir (README'deki gelecek işler).

---

## Gereksinimler

- Python 3.13+ (`runtime.txt` ile uyumlu)
- **ffmpeg** PATH'te (`ffmpeg -version`)
- **yt-dlp** (`requirements.txt`)

---

## Kurulum

```bash
git clone https://github.com/yucel-gumus/flask_youtube_video_cut_dowload.git
cd flask_youtube_video_cut_dowload
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask run
```

`http://127.0.0.1:5000`

---

## Kullanım

1. YouTube linkini yapıştır
2. İsteğe bağlı başlangıç/bitiş zamanı
3. İşlem bitince dosyayı indir

---

## Güvenlik

- Herkese açık deploy'da abuse riski — rate limit ve auth ekleyin
- İndirilen dosyaları periyodik temizleyin

---

## Lisans

MIT.