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
    Return: İndirilen dosyanın yolu veya None.
    """
    mp4_path = output_path + '.mp4'
    if os.path.exists(mp4_path):
        print(f"Dosya zaten mevcut: {mp4_path}")
        return mp4_path

    ydl_opts = {
        'outtmpl': output_path + '.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print("Video indirme sırasında hata:", e)
        return None

    return mp4_path if os.path.exists(mp4_path) else None
