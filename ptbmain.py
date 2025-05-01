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
        [KeyboardButton(
            text="🔓📢 Public Channels",
            request_chat=KeyboardButtonRequestChat(
                request_id=7,
                chat_is_channel=True,
                chat_has_username=True,
            )
        )],
        [KeyboardButton(
            text="🔐📢 Private Channels",
            request_chat=KeyboardButtonRequestChat(
                request_id=8,
                chat_is_channel=True,
                chat_has_username=False,
            )
        )],
        
        [KeyboardButton(
            text="🔓👥 Public Groups",
            request_chat=KeyboardButtonRequestChat(
                request_id=9,
                chat_is_channel=False,
                chat_has_username=True,
            )
        )],
        
        [KeyboardButton(
            text="🔐👥 Private Groups",
            request_chat=KeyboardButtonRequestChat(
                request_id=10,
                chat_is_channel=False,
                chat_has_username=False,
            )
        )],
        [KeyboardButton(
            text="🔓🗨️ Public Forums",
            request_chat=KeyboardButtonRequestChat(
                request_id=11,
                chat_is_channel=False,
                chat_has_username=True,
                chat_is_forum=True,
            )
        )],
        [KeyboardButton(
            text="🔐🗨️ Private Forums",
            request_chat=KeyboardButtonRequestChat(
                request_id=12,
                chat_is_channel=False,
                chat_has_username=False,
                chat_is_forum=True,
            )
        )],
        
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("A solution to find Public Private Channels, Groups, Forums with ownership and no ownership\n\n🤖 Use Buttons to interact with Bot\n\n🧑🏻‍💻 Creator @shuhaibnc", reply_markup=markup)

# Main
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()