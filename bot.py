"""
ربات نیم بها کننده لینک تلگرام
"""
import os
import logging
import asyncio
from pathlib import Path
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode

from config import BOT_TOKEN, TEMP_DIR, MAX_FILE_SIZE
from uploaders import UploaderManager, LinkNimConverter

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)

# Uploaders manager
uploader_manager = UploaderManager()
link_converter = LinkNimConverter()


def human_readable_size(size):
    """تبدیل حجم به صورت خوانا"""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور شروع ربات"""
    welcome_message = """
<b>👋 سلام! به ربات نیم بها کننده لینک خوش آمدید</b>

<b>📌 نحوه استفاده:</b>

1️⃣ <b>فایل فوروارد کنید:</b>
   فایل را از یک چت دیگر به ربات فوروارد کنید

2️⃣ <b>لینک مستقیم بفرستید:</b>
   لینک دانلود مستقیم فایل را ارسال کنید

3️⃣ <b>دستورات:</b>
   /start - شروع مجدد
   /help - راهنما
   /list - لیست آپلودرها
   /set_uploader - تنظیم آپلودر پیش‌فرض

<b>💡 نکته:</b> فایل پس از آپلود به صورت خودکار حذف می‌شود.
"""
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.HTML)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """دستور راهنما"""
    help_text = """
<b>📖 راهنمای ربات</b>

<b>📌 روش‌های استفاده:</b>

<b>1. فوروارد فایل:</b>
   - فایل را از چت دیگر به ربات فوروارد کنید
   - ربات فایل را دانلود و آپلود می‌کند
   - لینک نیم بها برای شما ارسال می‌شود

<b>2. ارسال لینک مستقیم:</b>
   - لینک دانلود مستقیم فایل را ارسال کنید
   - ربات فایل را دانلود و آپلود می‌کند
   - لینک نیم بها برای شما ارسال می‌شود

<b>📌 دستورات:</b>
   /start - شروع مجدد
   /help - نمایش این راهنما
   /list - لیست آپلودرهای موجود
   /set_uploader - تنظیم آپلودر پیش‌فرض

<b>📌 حجم فایل:</b>
   حداکثر حجم فایل: 2 گیگابایت

<b>📌 آپلودرها:</b>
   - uplod.ir (پیش‌فرض)
   - uploadkon.ir
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)


async def list_uploaders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """لیست آپلودرهای موجود"""
    uploaders = uploader_manager.list_uploaders()
    
    message = "<b>📋 لیست آپلودرهای موجود:</b>

"
    for i, name in enumerate(uploaders, 1):
        message += f"{i}. {name}
"
    
    message += "
<b>💡 برای تنظیم آپلودر پیش‌فرض:</b>"
    message += "
/set_uploader نام_آپلودر"
    
    await update.message.reply_text(message, parse_mode=ParseMode.HTML)


async def set_uploader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تنظیم آپلودر پیش‌فرض"""
    if not context.args:
        await update.message.reply_text(
            "لطفاً نام آپلودر را وارد کنید.
"
            "مثال: /set_uploader uplod",
            parse_mode=ParseMode.HTML
        )
        return
    
    uploader_name = context.args[0].lower()
    uploaders = uploader_manager.list_uploaders()
    
    if uploader_name not in uploaders:
        message = f"<b>❌ آپلودر '{uploader_name}' یافت نشد</b>

"
        message += "<b>آپلودرهای موجود:</b>
"
        for name in uploaders:
            message += f"- {name}
"
        await update.message.reply_text(message, parse_mode=ParseMode.HTML)
        return
    
    context.user_data["preferred_uploader"] = uploader_name
    
    await update.message.reply_text(
        f"<b>✅ آپلودر پیش‌فرض تنظیم شد:</b> {uploader_name}",
        parse_mode=ParseMode.HTML
    )


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش فایل دریافتی"""
    document = update.message.document
    
    if not document:
        await update.message.reply_text("⚠️ فایلی دریافت نشد.")
        return
    
    file_size = document.file_size
    
    # Check file size
    if file_size > MAX_FILE_SIZE:
        size_str = human_readable_size(file_size)
        max_str = human_readable_size(MAX_FILE_SIZE)
        await update.message.reply_text(
            f"<b>❌ حجم فایل بیش از حد مجاز است</b>

"
            f"حجم فایل: {size_str}
"
            f"حداکثر مجاز: {max_str}",
            parse_mode=ParseMode.HTML
        )
        return
    
    file_name = document.file_name or "unknown_file"
    
    # Show processing message
    status_msg = await update.message.reply_text(
        f"<b>⏳ در حال پردازش فایل...</b>

"
        f"<b>📁 نام فایل:</b> {file_name}
"
        f"<b>📦 حجم فایل:</b> {human_readable_size(file_size)}",
        parse_mode=ParseMode.HTML
    )
    
    try:
        # Download file from Telegram
        file_path = os.path.join(TEMP_DIR, file_name)
        
        telegram_file = await context.bot.get_file(document.file_id)
        await telegram_file.download_to_drive(file_path)
        
        await status_msg.edit_text(
            f"<b>✅ فایل دانلود شد</b>

"
            f"<b>📁 نام فایل:</b> {file_name}
"
            f"<b>📦 حجم فایل:</b> {human_readable_size(file_size)}

"
            f"<b>🔄 در حال آپلود به آپلود سنتر...</b>",
            parse_mode=ParseMode.HTML
        )
        
        # Upload to Iranian uploader
        preferred = context.user_data.get("preferred_uploader")
        result = uploader_manager.upload_with_fallback(file_path, preferred)
        
        if result["success"]:
            message = f"""
<b>✅ فایل با موفقیت آپلود شد!</b>

<b>📁 نام فایل:</b> {file_name}
<b>📦 حجم فایل:</b> {human_readable_size(file_size)}
<b>🌐 آپلودر:</b> {result.get('uploader', 'نامشخص')}

<b>🔗 لینک دانلود نیم بها:</b>
{result['url']}
"""
            await status_msg.edit_text(message, parse_mode=ParseMode.HTML)
        else:
            await status_msg.edit_text(
                f"<b>❌ خطا در آپلود فایل</b>

"
                f"<b>خطا:</b> {result.get('error', 'نامشخص')}",
                parse_mode=ParseMode.HTML
            )
    
    except Exception as e:
        logger.error(f"خطا در پردازش فایل: {e}")
        await status_msg.edit_text(
            f"<b>❌ خطا در پردازش فایل</b>

"
            f"<b>خطا:</b> {str(e)}",
            parse_mode=ParseMode.HTML
        )
    
    finally:
        # Cleanup: Delete the file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"فایل حذف شد: {file_path}")
        except Exception as e:
            logger.error(f"خطا در حذف فایل: {e}")


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پردازش لینک مستقیم"""
    url = update.message.text.strip()
    
    if not url.startswith(("http://", "https://")):
        await update.message.reply_text(
            "<b>⚠️ لطفاً یک لینک مستقیم معتبر ارسال کنید</b>

"
            "مثال:
"
            "https://example.com/file.zip",
            parse_mode=ParseMode.HTML
        )
        return
    
    # Extract filename from URL
    from urllib.parse import urlparse, unquote
    parsed = urlparse(url)
    file_name = unquote(parsed.path.split("/")[-1]) or "downloaded_file"
    
    status_msg = await update.message.reply_text(
        f"<b>⏳ در حال دانلود فایل...</b>

"
        f"<b>🔗 لینک:</b> {url[:50]}...",
        parse_mode=ParseMode.HTML
    )
    
    file_path = os.path.join(TEMP_DIR, file_name)
    
    try:
        # Download file from URL
        import requests
        
        response = requests.get(url, stream=True, timeout=300, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        response.raise_for_status()
        
        # Get file size
        total_size = int(response.headers.get("content-length", 0))
        
        if total_size > MAX_FILE_SIZE:
            await status_msg.edit_text(
                f"<b>❌ حجم فایل بیش از حد مجاز است</b>

"
                f"حجم فایل: {human_readable_size(total_size)}
"
                f"حداکثر مجاز: {human_readable_size(MAX_FILE_SIZE)}",
                parse_mode=ParseMode.HTML
            )
            return
        
        # Download with progress
        downloaded = 0
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
        
        actual_size = os.path.getsize(file_path)
        
        await status_msg.edit_text(
            f"<b>✅ فایل دانلود شد</b>

"
            f"<b>📁 نام فایل:</b> {file_name}
"
            f"<b>📦 حجم فایل:</b> {human_readable_size(actual_size)}

"
            f"<b>🔄 در حال آپلود به آپلود سنتر...</b>",
            parse_mode=ParseMode.HTML
        )
        
        # Upload to Iranian uploader
        preferred = context.user_data.get("preferred_uploader")
        result = uploader_manager.upload_with_fallback(file_path, preferred)
        
        if result["success"]:
            message = f"""
<b>✅ فایل با موفقیت آپلود شد!</b>

<b>📁 نام فایل:</b> {file_name}
<b>📦 حجم فایل:</b> {human_readable_size(actual_size)}
<b>🌐 آپلودر:</b> {result.get('uploader', 'نامشخص')}

<b>🔗 لینک دانلود نیم بها:</b>
{result['url']}
"""
            await status_msg.edit_text(message, parse_mode=ParseMode.HTML)
        else:
            await status_msg.edit_text(
                f"<b>❌ خطا در آپلود فایل</b>

"
                f"<b>خطا:</b> {result.get('error', 'نامشخص')}",
                parse_mode=ParseMode.HTML
            )
    
    except requests.exceptions.RequestException as e:
        await status_msg.edit_text(
            f"<b>❌ خطا در دانلود فایل</b>

"
            f"<b>خطا:</b> {str(e)}",
            parse_mode=ParseMode.HTML
        )
    
    except Exception as e:
        logger.error(f"خطا در پردازش لینک: {e}")
        await status_msg.edit_text(
            f"<b>❌ خطا در پردازش لینک</b>

"
            f"<b>خطا:</b> {str(e)}",
            parse_mode=ParseMode.HTML
        )
    
    finally:
        # Cleanup: Delete the file
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"فایل حذف شد: {file_path}")
        except Exception as e:
            logger.error(f"خطا در حذف فایل: {e}")


async def post_init(application: Application):
    """تنظیمات پس از راه‌اندازی ربات"""
    # Set bot commands
    commands = [
        BotCommand("start", "شروع مجدد ربات"),
        BotCommand("help", "راهنمای ربات"),
        BotCommand("list", "لیست آپلودرها"),
        BotCommand("set_uploader", "تنظیم آپلودر پیش‌فرض"),
    ]
    await application.bot.set_my_commands(commands)
    
    logger.info("ربات با موفقیت راه‌اندازی شد!")


def main():
    """تابع اصلی"""
    # Create application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("list", list_uploaders))
    application.add_handler(CommandHandler("set_uploader", set_uploader))
    
    # Document handler (for forwarded files)
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    # URL handler (for direct links)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_url
    ))
    
    # Run bot
    logger.info("ربات در حال اجرا...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
