from flask import Flask, render_template, request
from utils.youtube_utils import convert_to_hhmmss, download_video, is_ffmpeg_installed
from utils.ffmpeg_utils import cut_video
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    status_message = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        start_time_raw = request.form.get("start_time", "")
        end_time_raw = request.form.get("end_time", "")

        start_time = convert_to_hhmmss(start_time_raw)
        end_time = convert_to_hhmmss(end_time_raw)

        if not is_ffmpeg_installed():
            status_message = "ffmpeg yüklü değil. Lütfen ffmpeg kurun."
            return render_template("index.html", status_message=status_message)

        if url:
            output_path = "downloaded_video"
            status_message = "Video indiriliyor..."
            # Video indirme
            video_path = download_video(url, output_path)
            if not video_path:
                status_message = "Video indirmede hata oluştu."
            else:
                status_message = "Video kesiliyor..."
                cut_path = cut_video(video_path, start_time, end_time)
                if cut_path:
                    # İşlem tamam
                    final_name = os.path.basename(cut_path)
                    status_message = f"İşlem tamamlandı! Çıktı dosyası: {final_name}"
                else:
                    status_message = "Kesme işleminde hata oluştu."

    return render_template("index.html", status_message=status_message)

if __name__ == "__main__":
    # Flask uygulamasını çalıştırma
    app.run(debug=True)
