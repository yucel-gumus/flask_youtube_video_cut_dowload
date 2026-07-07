# 🎬 YouTube Video İndirici ve Kesici (Flask yt-dlp & FFmpeg Processor)

YouTube Video İndirici ve Kesici; kullanıcıların YouTube video adreslerini girerek videoları doğrudan sunucuya indirmesini ve ardından belirledikleri zaman aralıklarına göre (kırpma/kesme) sadece istedikleri kısımları cihazlarına kaydetmesini sağlayan **Python & Flask** tabanlı bir web uygulamasıdır.

Uygulama, uzun indirme işlemlerinin web isteklerini bloke etmesini engellemek için **arka plan iş parçacıkları (threading)** mimarisiyle çalışır.

---

## 🌟 Öne Çıkan Özellikler

* 🚀 **Asenkron Arka Plan İşleme (Threading):** İndirme ve kesme işlemleri sunucu tarafında `threading.Thread` ile arka planda çalıştırılır. Kullanıcı arayüzü işlem devam ederken donmaz.
* 🔄 **JSON Polling Durum Takibi:** İstemci, bir işlem başlattıktan sonra `/status/<job_id>` API endpoint'ini periyodik olarak sorgular (polling) ve arayüzdeki durum göstergesini (`pending`, `downloading`, `cutting`, `completed`, `failed`) gerçek zamanlı günceller.
* 📦 **yt-dlp ile Güçlü İndirme Motoru:** En güncel ve popüler video indirme kütüphanesi olan `yt-dlp` kullanılarak YouTube video ve ses akışları en yüksek kalitede çekilir.
* ✂️ **FFmpeg ile Hassas Kesme:**
  * Kullanıcılar saniye, `MM:SS` veya `HH:MM:SS` formatında esnek başlangıç/bitiş zamanları tanımlayabilir.
  * Sistem, arka planda **FFmpeg** CLI komutlarını tetikleyerek videoyu belirlenen zaman aralığına göre tam karesinde keser ve muxing (ses ve görüntüyü birleştirme) yapar.
* 📁 **Kuyruk ve Bellek Yönetimi:** İş durumları sunucu RAM'inde (in-memory job store) güvenli bir şekilde saklanır.

---

## 🏗️ Sistem Akışı ve Mimarisi

```
[ Kullanıcı URL + Süre Girer ] ──► [ POST /process ]
                                          │
                                          ▼
[ JSON Yanıtı: {job_id} ] ◄── [ Başlat: threading.Thread ]
      │
      ├──► (Arka Planda) ──► 1. yt-dlp İndirme ──► 2. FFmpeg Kesme (Trim)
      │
[ GET /status/<job_id> ] ──► (Polling durumunu okur ve UI'da gösterir)
      │
      ▼
[ İşlem Tamamlandı ] ──► [ Kullanıcı İndirme Linkini Alır ]
```

---

## 🛠️ Teknoloji Stack

* **Backend Framework:** Python 3.13, Flask.
* **İndirme Aracı:** `yt-dlp`.
* **Medya İşleme:** FFmpeg CLI.
* **Arayüz Tasarımı:** HTML5, CSS3, JavaScript (polling client).

---

## 📂 Proje Klasör Yapısı

```
flask_youtube_video_cut_dowload/
├── templates/
│   └── index.html            # İndirme formu ve polling durum paneli
├── utils/
│   ├── ffmpeg_utils.py       # FFmpeg trim/cut komut sarmalayıcısı
│   └── youtube_utils.py      # yt-dlp indirme yöneticisi
├── app.py                    # Flask sunucu rotaları ve thread kuyruk yönetimi
├── requirements.txt          # Gerekli kütüphaneler listesi
└── README.md
```

---

## 🚀 Kurulum ve Yerel Çalıştırma

### Ön Gereksinimler
Sisteminizde **FFmpeg** yüklü ve PATH çevresel değişkenine tanımlı olmalıdır:
* **macOS:** `brew install ffmpeg`
* **Ubuntu/Debian:** `sudo apt update && sudo apt install ffmpeg`

### 1. Bağımlılıkları Yükleyin
```bash
git clone https://github.com/yucel-gumus/flask_youtube_video_cut_dowload.git
cd flask_youtube_video_cut_dowload
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Uygulamayı Başlatın
```bash
flask run
```
Uygulama `http://127.0.0.1:5000` adresinde yerel sunucuda çalışmaya başlayacaktır.

---

## 🔗 Bağlantılar
* **GitHub Repository:** [https://github.com/yucel-gumus/flask_youtube_video_cut_dowload](https://github.com/yucel-gumus/flask_youtube_video_cut_dowload)
* **Geliştirici LinkedIn:** [https://linkedin.com/in/yucel-gumus](https://linkedin.com/in/yucel-gumus)