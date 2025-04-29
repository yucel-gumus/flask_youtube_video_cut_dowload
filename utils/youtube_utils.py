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
    # yt-dlp expects path without extension for '%(ext)s' template
    output_template = output_path + '.%(ext)s'

    ydl_opts = {
        'outtmpl': output_template,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', # Prioritize mp4
        'merge_output_format': 'mp4',
        'noplaylist': True, # Ensure only single video is downloaded
        # 'quiet': True, # Uncomment to suppress yt-dlp console output
        # 'no_warnings': True, # Uncomment to suppress warnings
        'noprogress': True, # Disable progress bar in console
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4', # Ensure final output is mp4
        }],
    }

    final_path = None
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            # After download, figure out the exact path yt-dlp created
            final_path = ydl.prepare_filename(info_dict)
            # Sanity check if the file exists, handle potential templating issues
            if not final_path or not os.path.exists(final_path):
                 # Try to guess common extensions if exact path not found
                 if os.path.exists(output_path + ".mp4"):
                     final_path = output_path + ".mp4"
                 elif os.path.exists(output_path + ".mkv"):
                     final_path = output_path + ".mkv"
                     # Optionally convert mkv to mp4 here if needed, or adjust format options
                 elif os.path.exists(output_path + ".webm"):
                     final_path = output_path + ".webm"
                 else:
                     raise FileNotFoundError(f"İndirme tamamlandı ancak dosya bulunamadı: {output_path}.[mp4/mkv/webm]")

    except Exception as e:
        print(f"Video indirme sırasında hata ({url}): {e}") # Log the error
        # Re-raise the exception to be caught by the background task
        raise Exception(f"Video indirme hatası: {e}")

    # Check again if the file exists after potential post-processing
    if not final_path or not os.path.exists(final_path):
        raise FileNotFoundError(f"İndirme/işleme sonrası dosya bulunamadı: {final_path}")

    return final_path
