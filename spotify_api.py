import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtube import download_youtube
import yt_dlp
import os

from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET))

def download_spotify_track(track_uri: str, out_dir: str):
    track = sp.track(track_uri)
    query = f"{track['name']} {track['artists'][0]['name']} audio"

    ydl_opts = {"quiet": True, "skip_download": True, "default_search": "ytsearch1"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        yt_url = info["entries"][0]["webpage_url"]

    return download_youtube(yt_url, out_dir, resolution="720p")
