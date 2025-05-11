import os
import logging
from telegram import Update,
InlineKeyboardButton,
InlineKeyboardMarkup
from telegram.ext import
ApplicationBuilder, CommandHandler,
MessageHandler, filters,
CallbackContext, CallbackQueryHandler
import yt_dlp
from shazamio import Shazam
# تنظیمات اولیه
  TOKEN = os.getenv("BOT_TOKEN")
  logging.basicConfig(level=logging.INFO)
# دستور start
  async def start(update: Update, context:
  CallbackContext):
  await
  update.message.reply_text("سلام! لینک ویدیویی، صوتی یا نام خواننده/متن آهنگ رو بفرست.")
# مدیریت پیام‌ها
  async def handle_message(update: Update,
  context: CallbackContext):
  text = update.message.text
  if text.startswith("http"):
  await
  update.message.reply_text("در حال پردازش لینک...")
  await
  download_media(update, text) else: await search_song(update, text)
# دانلود رسانه
  async def download_media(update: Update, url: str): ydl_opts = { 'outtmpl': '%(title)s.%(ext)s', 'format': 'bestaudio/best', 'noplaylist': True, } with yt_dlp.YoutubeDL(ydl_opts) as ydl: try: info = ydl.extract_info(url, download=False) title = info.get('title', 'فایل') ext = info.get('ext', 'mp3') file_url = info['url'] await update.message.reply_text(f"دانلود آماده نیست، ولی این لینک پخش مستقیم فایل است: {file_url}") except Exception as e: await update.message.reply_text("خطا در پردازش لینک")
# جستجوی آهنگ
  async def search_song(update: Update, query: str): shazam = Shazam() try: results = await shazam.search(query) tracks = results['tracks']['hits'][:5] buttons = [ [InlineKeyboardButton(f"{track['track']['title']} - {track['track']['subtitle']}", callback_data=track['track']['key'])] for track in tracks ] reply_markup = InlineKeyboardMarkup(buttons) await update.message.reply_text("آهنگ‌های مرتبط:", reply_markup=reply_markup) except: await update.message.reply_text("نتیجه‌ای یافت نشد.")
# مدیریت دکمه‌ها
  async def button(update: Update, context: CallbackContext): query = update.callback_query await query.answer() key = query.data await query.edit_message_text(text=f"در حال پردازش آهنگ انتخاب‌شده با کلید: {key}")
# در مرحله‌ی بعدی می‌توان لینک مستقیم یا پیش‌نمایش آهنگ را ارائه داد #
# اجرای ربات
  if __name__ == '__main__': app = ApplicationBuilder().token(TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)) app.add_handler(CallbackQueryHandler(button)) app.run_polling()
