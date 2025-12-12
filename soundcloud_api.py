import soundcloud
import subprocess, os
from utils import normalize_audio

from config import SOUNDCLOUD_CLIENT_ID

client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)

def download_sc_track(track_url: str, out_dir: str):
    track = client.get('/resolve', url=track_url)
    stream_url = track.stream_url + f"?client_id={client.client_id}"
    filename = f"{track.title}.mp3"
    mp3_path = os.path.join(out_dir, filename)

    subprocess.run([
        "ffmpeg", "-i", stream_url,
        "-b:a", "320k", mp3_path,
        "-y"
    ], check=True)

    normalize_audio(mp3_path)
    return mp3_path
