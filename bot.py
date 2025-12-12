import telebot, os
from config import TELEGRAM_TOKEN
from db import init_db, file_exists, register_file
from youtube import download_youtube
from soundcloud_api import download_sc_track
from spotify_api import download_spotify_track

bot = telebot.TeleBot(TELEGRAM_TOKEN)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

init_db()   # створює SQLite‑таблицю, якщо ще немає

def send_file(chat_id, path):
    with open(path, "rb") as f:
        bot.send_document(chat_id, f)

@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message,
        "Надішліть посилання на YouTube, SoundCloud або Spotify – я завантажу відео 720p, MP3 320 kbps і AAC 256 kbps. "
        "Повторне завантаження того ж файлу буде пропущено."
    )

@bot.message_handler(func=lambda m: True)
def handle_link(message):
    url = message.text.strip()
    chat_id = message.chat.id

    try:
        if "youtube.com" in url or "youtu.be" in url:
            video, mp3, aac = download_youtube(url, DOWNLOAD_DIR)
            files = [video, mp3, aac]
        elif "soundcloud.com" in url:
            mp3 = download_sc_track(url, DOWNLOAD_DIR)
            files = [mp3]
        elif "spotify.com" in url:
            video, mp3, aac = download_spotify_track(url, DOWNLOAD_DIR)
            files = [video, mp3, aac]
        else:
            bot.reply_to(message, "❓ Не розпізнано підтримувану платформу.")
            return

        for f in files:
            if file_exists(f):
                bot.reply_to(message, f"📁 {os.path.basename(f)} вже є в базі – пропускаю.")
                continue
            send_file(chat_id, f)
            register_file(f, os.path.basename(f))

    except Exception as e:
        bot.reply_to(message, f"⚠️ Помилка: {e}")

if __name__ == "__main__":
    print("Bot started. Waiting for messages...")
    bot.infinity_polling()
