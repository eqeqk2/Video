import os
from dotenv import load_dotenv

load_dotenv()          # читає .env у корені проєкту

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
