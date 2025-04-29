# YouTube Video İndirici ve Kesici Web Uygulaması

Bu Flask tabanlı web uygulaması, YouTube videolarını indirmenize ve belirlediğiniz zaman aralıklarına göre kesmenize olanak tanır. İşlemler arka planda yürütülür ve durum güncellemeleri web arayüzünde dinamik olarak gösterilir.

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.2+-black.svg)](https://flask.palletsprojects.com/)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-brightgreen.svg)](https://github.com/yt-dlp/yt-dlp)
[![ffmpeg](https://img.shields.io/badge/ffmpeg-required-yellow.svg)](https://ffmpeg.org/)

## Özellikler

*   **YouTube Video İndirme:** Sağlanan URL'den videoları indirir (`yt-dlp` kullanarak).
*   **Video Kesme:** İndirilen videoları belirtilen başlangıç ve bitiş zamanlarına göre keser (`ffmpeg` kullanarak).
*   **Web Arayüzü:** Basit ve kullanıcı dostu bir web arayüzü.
*   **Asenkron İşlemler:** İndirme ve kesme işlemleri arka planda çalışır, arayüz kilitlenmez.
*   **Dinamik Durum Takibi:** İşlemin durumu (sıraya alındı, indiriliyor, kesiliyor, tamamlandı, hata) arayüzde gerçek zamanlı olarak güncellenir.
*   **Hata Yönetimi:** Geçersiz girdiler ve işlem hataları için bilgilendirici mesajlar gösterilir.
*   **Kolay Dağıtım:** `Procfile` ve `requirements.txt` ile Railway gibi platformlara kolayca dağıtılabilir.

## Gereksinimler

*   **Python:** 3.13 veya üzeri (Önerilen sürüm `runtime.txt` içinde belirtilmiştir)
*   **pip:** Python paket yöneticisi
*   **ffmpeg:** Video kesme işlemi için gereklidir. Sisteminize kurmanız ve PATH ortam değişkenine eklemeniz gerekir.
    *   [ffmpeg İndirme ve Kurulum Kılavuzu](https://ffmpeg.org/download.html)
*   **Git:** Versiyon kontrol sistemi (isteğe bağlı, projeyi klonlamak için)

## Yerel Kurulum ve Çalıştırma

1.  **Projeyi Klonlayın (veya İndirin):**
    ```bash
    git clone https://github.com/yucel-gumus/flask_youtube_video_cut_dowload.git
    cd flask_youtube_video_cut_dowload
    ```

2.  **Sanal Ortam Oluşturun ve Aktifleştirin:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate  # Windows
    ```

3.  **Bağımlılıkları Kurun:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **ffmpeg'in Kurulu Olduğundan Emin Olun:**
    Terminalde `ffmpeg -version` komutunu çalıştırarak ffmpeg'in kurulu ve erişilebilir olup olmadığını kontrol edin.

5.  **Flask Uygulamasını Başlatın:**
    ```bash
    flask run
    ```

6.  Uygulamaya tarayıcınızdan erişin (varsayılan adres: `http://127.0.0.1:5000`).

## Kullanım

1.  Web arayüzündeki "YouTube URL" alanına indirmek istediğiniz videonun linkini yapıştırın.
2.  Videoyu kesmek istiyorsanız, "Başlangıç Zamanı" ve "Bitiş Zamanı" alanlarına istediğiniz zamanları girin. Formatlar:
    *   Sadece saniye (örn: `90`)
    *   Dakika:Saniye (örn: `01:30`)
    *   Saat:Dakika:Saniye (örn: `00:01:30`)
    *   Boş bırakırsanız, videonun başından başlar veya sonuna kadar gider.
3.  "İndir ve Kes" butonuna tıklayın.
4.  İşlem durumu arayüzde görünecektir.
5.  İşlem başarıyla tamamlandığında, kesilmiş (veya sadece indirilmiş) videoyu indirmek için bir bağlantı görünecektir.

## Railway ile Dağıtım (Deployment)

Bu proje, Railway üzerinde kolayca dağıtılmak üzere yapılandırılmıştır:

1.  Projenizi bir GitHub deposuna yükleyin.
2.  Railway hesabınıza giriş yapın ve yeni bir proje oluşturun.
3.  Proje kaynağı olarak GitHub deponuzu seçin.
4.  Railway, `Procfile` ve `requirements.txt` dosyalarını otomatik olarak algılayacaktır.
5.  **Önemli (`ffmpeg`):** Railway üzerinde `ffmpeg`'in kullanılabilir olması için proje kök dizinine `nixpacks.toml` dosyası eklenmiştir. Bu dosya, build sırasında `ffmpeg` paketinin kurulmasını sağlar.
6.  **Önemli (İndirme Sınırlamaları):** YouTube, sunucu IP adreslerinden gelen isteklere karşı bot koruması uygulayabilir. Bu nedenle, **deploy edilmiş uygulama bazı videoları indirirken "Sign in to confirm you're not a bot" gibi hatalar verebilir.** Bu tür videoları indirmek için kimlik doğrulaması (cookie'ler) gerekir. Cookie yönetimi deploy edilmiş bir web uygulaması için karmaşık ve riskli olduğundan, bu özellik şu an için eklenmemiştir. Bu tür videoları indirmek için uygulamayı yerel makinenizde çalıştırmanız gerekebilir.
7.  Dağıtımın tamamlanmasını bekleyin ve sağlanan URL üzerinden uygulamanıza erişin.

## Gelecekteki Olası Geliştirmeler

*   Daha gelişmiş ilerleme takibi (`yt-dlp` ve `ffmpeg` çıktılarından).
*   Video kalitesi seçme seçeneği.
*   İndirilen/kesilen dosyaları yönetmek için bir arayüz (listeleme, silme).
*   Daha sağlam bir arka plan görev sistemi (örn: Celery, RQ).
*   Yapılandırma dosyasından ayarları okuma (örn: indirme dizini).
*   Daha modern bir UI (örn: Bootstrap, Tailwind CSS).
