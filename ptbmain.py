from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your bot token
BOT_TOKEN = "7629727539:AAE4UqcP0lTXXf3WaKFDEvxON13zbnhyGlA"

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton(
            text="📢 Channels",
            request_chat=KeyboardButtonRequestChat(
                request_id=1,
                chat_is_channel=True,
                
            )
        )],
        [KeyboardButton(
            text="👥 Groups",
            request_chat=KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False
            )
        )],
        
        [KeyboardButton(
            text="🗨️ Forums",
            request_chat=KeyboardButtonRequestChat(
                request_id=3,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )],
        
        [KeyboardButton(
            text="📢 My Channels",
            request_chat=KeyboardButtonRequestChat(
                request_id=4,
                chat_is_channel=True,
                chat_is_created=True
            )
        )],
        
        [KeyboardButton(
            text="👥 My Groups",
            request_chat=KeyboardButtonRequestChat(
                request_id=5,
                chat_is_channel=False,
                chat_is_created=True
            )
        )],
        
        [KeyboardButton(
            text="🗨️ My Forums",
            request_chat=KeyboardButtonRequestChat(
                request_id=6,
                chat_is_channel=False,
                chat_is_forum=True,
                chat_is_created=True
            )
        )],
        
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("🤖 Use Buttons to interact with Bot", reply_markup=markup)

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()