import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token (از @BotFather بگیرید)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Iranian Uploader API Keys (اختیاری)
UUPLOAD_TOKEN = os.getenv("UUPLOAD_TOKEN", "")
UPLOAD_IR_TOKEN = os.getenv("UPLOAD_IR_TOKEN", "")

# حداکثر حجم فایل (پیش‌فرض 2 گیگابایت)
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 2 * 1024 * 1024 * 1024))

# پوشه موقت برای دانلود فایلها
TEMP_DIR = os.getenv("TEMP_DIR", "/tmp/nim-behah-bot")
