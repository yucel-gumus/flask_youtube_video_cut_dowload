import os
import subprocess
from yt_dlp import YoutubeDL

def is_ffmpeg_installed():
    """ffmpeg'in kurulu olup olmadığını kontrol eder."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def convert_to_hhmmss(time_str):
    """
    Verilen zaman bilgisini HH:MM:SS formatına dönüştürür.
    Eğer kullanıcı '780' gibi bir değer verirse bunu HH:MM:SS formatına çevirir.
    Boş string gelirse None döndürür.
    """
    time_str = time_str.strip()
    if not time_str:
        return None
    if ':' in time_str:
        return time_str
    else:
        seconds = int(time_str)
        return f"{seconds // 3600:02}:{(seconds % 3600) // 60:02}:{seconds % 60:02}"

def download_video(url, output_path):
    """
    YouTube videosunu en iyi kalitede indirir.
    Zaten indirilmişse tekrar indirmez.
    Return: İndirilen dosyanın yolu.
    Raises: Exception: İndirme sırasında bir hata oluşursa.
    """
    output_template = output_path + '.%(ext)s'

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'noprogress': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }

    final_path = None
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            final_path = ydl.prepare_filename(info_dict)
            if not final_path or not os.path.exists(final_path):
                 if os.path.exists(output_path + ".mp4"):
                     final_path = output_path + ".mp4"
                 elif os.path.exists(output_path + ".mkv"):
                     final_path = output_path + ".mkv"
                 elif os.path.exists(output_path + ".webm"):
                     final_path = output_path + ".webm"
                 else:
                     raise FileNotFoundError(f"İndirme tamamlandı ancak dosya bulunamadı: {output_path}.[mp4/mkv/webm]")

    except Exception as e:
        print(f"Video indirme sırasında hata ({url}): {e}")
        raise Exception(f"Video indirme hatası: {e}")

    if not final_path or not os.path.exists(final_path):
        raise FileNotFoundError(f"İndirme/işleme sonrası dosya bulunamadı: {final_path}")

    return final_path
