import subprocess, os

def normalize_audio(file_path: str):
    """EBU R128 нормалізація за допомогою ffmpeg‑loudnorm."""
    tmp = file_path + ".norm"
    subprocess.run([
        "ffmpeg", "-i", file_path,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        tmp, "-y"
    ], check=True)
    os.replace(tmp, file_path)

def convert_to_aac(src: str, dst: str, bitrate="256k"):
    subprocess.run([
        "ffmpeg", "-i", src,
        "-c:a", "aac", "-b:a", bitrate,
        dst, "-y"
    ], check=True)
