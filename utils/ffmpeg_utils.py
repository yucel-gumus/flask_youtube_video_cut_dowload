import subprocess

def cut_video(input_path, start_time, end_time):
    """
    ffmpeg ile videoyu keser.
    start_time veya end_time boşsa kesme yapmadan input'u geri döndürür.
    """
    if not start_time or not end_time:
        return input_path

    output_path = input_path.replace('.mp4', '_cut.mp4')
    command = [
        'ffmpeg',
        '-i', input_path,
        '-ss', start_time,
        '-to', end_time,
        '-c', 'copy',
        output_path,
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Kesilmiş video oluşturuldu: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print("Video kesme sırasında hata oluştu:", e)
        return None
