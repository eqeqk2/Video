from pytube import YouTube
import os, subprocess
from utils import normalize_audio, convert_to_aac

def download_youtube(url: str, out_dir: str, resolution="720p"):
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True,
                               file_extension='mp4',
                               res=resolution).first()
    if not stream:
        # береться найвища доступна якість
        stream = yt.streams.filter(progressive=True,
                                   file_extension='mp4').order_by('resolution').desc().first()
    video_path = stream.download(output_path=out_dir)

    base_name = os.path.splitext(os.path.basename(video_path))[0]
    mp3_path = os.path.join(out_dir, f"{base_name}.mp3")
    aac_path = os.path.join(out_dir, f"{base_name}.aac")

    # MP3 320 kbps
    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-b:a", "320k", "-vn", mp3_path,
        "-y"
    ], check=True)

    # AAC 256 kbps
    convert_to_aac(video_path, aac_path, bitrate="256k")

    normalize_audio(mp3_path)
    normalize_audio(aac_path)

    return video_path, mp3_path, aac_path
