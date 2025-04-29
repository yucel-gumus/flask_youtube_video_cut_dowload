import re
from flask import Flask, render_template, request, jsonify, redirect, url_for
from utils.youtube_utils import download_video, is_ffmpeg_installed
from utils.ffmpeg_utils import cut_video
import os
import time
import threading
import uuid
import traceback

app = Flask(__name__)

# --- Global Job Store ---
# In a real-world scenario, consider using a more robust solution like Redis or a database
# for job tracking, especially if scaling or persistence is needed.
jobs = {}

# --- Helper Functions (Validation, Time Conversion - keep as is) ---
# Simpler regex: removed the optional ending part (&.*)?
YOUTUBE_URL_REGEX = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([\w-]+)$"

def validate_time_format(time_str):
    """Validates HH:MM:SS, MM:SS or seconds format and converts seconds to HH:MM:SS"""
    time_str = time_str.strip()
    if not time_str:
        return "", None

    if re.fullmatch(r"\d+", time_str):
        try:
            seconds = int(time_str)
            if seconds < 0:
                return None, "Zaman negatif olamaz."
            return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}", None
        except ValueError:
            return None, "Geçersiz saniye formatı."

    elif re.fullmatch(r"\d{1,2}:\d{1,2}", time_str):
        try:
            parts = list(map(int, time_str.split(':')))
            if len(parts) == 2:
                m, s = parts
                if not (0 <= m < 60 and 0 <= s < 60):
                    return None, "Geçersiz MM:SS formatı (dakika/saniye 0-59 arası olmalı)."
                return f"00:{m:02}:{s:02}", None
            else:
                 return None, "Geçersiz MM:SS formatı."
        except ValueError:
            return None, "Geçersiz MM:SS formatı (sayısal olmayan karakterler?)."

    elif re.fullmatch(r"\d{1,2}:\d{1,2}:\d{1,2}", time_str):
        try:
            parts = list(map(int, time_str.split(':')))
            if len(parts) == 3:
                h, m, s = parts
                if not (0 <= m < 60 and 0 <= s < 60):
                     return None, "Geçersiz HH:MM:SS formatı (dakika/saniye 0-59 arası olmalı)."
                return f"{h:02}:{m:02}:{s:02}", None
            else:
                return None, "Geçersiz HH:MM:SS formatı."
        except ValueError:
             return None, "Geçersiz HH:MM:SS formatı (sayısal olmayan karakterler?)."

    return None, "Geçersiz zaman formatı. Sadece saniye (örn: 90), MM:SS (örn: 01:30) veya HH:MM:SS (örn: 00:01:30) kullanın."

def time_str_to_seconds(time_str):
    """Converts HH:MM:SS string to total seconds."""
    if not time_str: return 0
    try:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except ValueError:
        return 0

# --- Background Task Function ---
def process_video_task(job_id, url, start_time, end_time, output_dir, base_filename):
    """The actual video processing logic to run in a thread."""
    video_path = None
    cut_path = None
    output_path_base = os.path.join(output_dir, base_filename)

    try:
        jobs[job_id] = {'status': 'downloading', 'message': 'Video indiriliyor...'}
        print(f"Job {job_id}: Downloading {url}")

        video_path = download_video(url, output_path_base)

        jobs[job_id]['message'] = 'Video indirme tamamlandı.'
        jobs[job_id]['original_video'] = os.path.basename(video_path)

        if start_time or end_time:
            jobs[job_id] = {'status': 'cutting', 'message': f"'{os.path.basename(video_path)}' kesiliyor ({start_time or 'başlangıç'} - {end_time or 'son'})..."}
            print(f"Job {job_id}: Cutting {video_path} from {start_time} to {end_time}")

            cut_path = cut_video(video_path, start_time, end_time)

            if not cut_path or not os.path.exists(cut_path):
                raise Exception("Video kesme işlemi başarısız. Zaman aralığını veya indirilen videoyu kontrol edin.")

            final_name = os.path.basename(cut_path)
            jobs[job_id] = {
                'status': 'completed',
                'message': f"İşlem tamamlandı! Kesilen dosya: {final_name}",
                'download_path': cut_path,
                'filename': final_name
            }
            print(f"Job {job_id}: Cutting completed: {final_name}")

        else:
            jobs[job_id] = {
                'status': 'completed',
                'message': f"İndirme tamamlandı! Dosya: {os.path.basename(video_path)}",
                'download_path': video_path,
                'filename': os.path.basename(video_path)
            }
            print(f"Job {job_id}: Download completed (no cutting): {os.path.basename(video_path)}")

    except Exception as e:
        print(f"Job {job_id}: Hata oluştu - {e}")
        traceback.print_exc()
        jobs[job_id] = {'status': 'error', 'message': f"Hata: {e}"}
        if cut_path and os.path.exists(cut_path):
            try: os.remove(cut_path)
            except OSError: pass
        if video_path and os.path.exists(video_path) and cut_path != video_path :
             try: os.remove(video_path)
             except OSError: pass

# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        start_time_raw = request.form.get("start_time", "")
        end_time_raw = request.form.get("end_time", "")
        error_message = None

        if not url:
            error_message = "Lütfen bir YouTube URL'si girin."
        else:
            if not re.fullmatch(YOUTUBE_URL_REGEX, url):
                 error_message = "Geçersiz YouTube URL formatı."

        start_time, start_err = validate_time_format(start_time_raw)
        if start_err:
            error_message = f"Başlangıç zamanı hatası: {start_err}"

        end_time, end_err = validate_time_format(end_time_raw)
        if end_err and not error_message:
           error_message = f"Bitiş zamanı hatası: {end_err}"

        if start_time and end_time and time_str_to_seconds(start_time) >= time_str_to_seconds(end_time):
             if not error_message:
                 error_message = "Başlangıç zamanı, bitiş zamanından önce olmalıdır."

        if not error_message and (start_time or end_time) and not is_ffmpeg_installed():
             error_message = "ffmpeg kurulu değil veya PATH içinde bulunamadı. Kesme işlemi için gereklidir."

        if error_message:
            return render_template("index.html", error_message=error_message)
        else:
            job_id = str(uuid.uuid4())
            output_dir = "downloads"
            if not os.path.exists(output_dir):
                 os.makedirs(output_dir)
            base_filename = f"video_{job_id}"

            thread = threading.Thread(target=process_video_task, args=(job_id, url, start_time, end_time, output_dir, base_filename))
            thread.start()

            jobs[job_id] = {'status': 'queued', 'message': 'İşlem sıraya alındı...'}
            print(f"Job {job_id}: Queued for URL {url}")

            return redirect(url_for('index', job_id=job_id))

    job_id = request.args.get('job_id')
    initial_status = None
    error_message = None

    if job_id and job_id in jobs:
        initial_status = jobs[job_id]
    elif job_id:
        error_message = "Geçersiz veya süresi dolmuş iş kimliği."

    return render_template("index.html", job_id=job_id, initial_status=initial_status, error_message=error_message)

@app.route("/status/<job_id>")
def job_status(job_id):
    """API endpoint to get the status of a job."""
    job = jobs.get(job_id)
    if job:
        return jsonify(job)
    else:
        return jsonify({'status': 'error', 'message': 'İş bulunamadı.'}), 404

@app.route("/download/<job_id>")
def download_file(job_id):
    job = jobs.get(job_id)
    if job and job['status'] == 'completed' and 'download_path' in job and os.path.exists(job['download_path']):
        from flask import send_file
        try:
            return send_file(job['download_path'], as_attachment=True, download_name=job.get('filename', os.path.basename(job['download_path'])))
        except Exception as e:
            print(f"Download error for job {job_id}: {e}")
            return jsonify({'status': 'error', 'message': 'Dosya gönderilirken hata oluştu.'}), 500
    elif job and job['status'] == 'error':
         return jsonify({'status': 'error', 'message': 'İşlem hatayla sonuçlandı, dosya indirilemez.'}), 400
    elif job:
        return jsonify({'status': 'processing', 'message': 'İşlem henüz tamamlanmadı.'}), 400
    else:
        return jsonify({'status': 'error', 'message': 'İş bulunamadı.'}), 404

if __name__ == "__main__":
    app.run(debug=True)
