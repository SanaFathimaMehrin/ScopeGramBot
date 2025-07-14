import os
import logging
from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup, Update,
    ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters, CallbackQueryHandler
)
from aiohttp import web
import asyncio
from route import routes  # Import routes
from telegram.constants import ParseMode

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_STATE = {}

# Navigation helpers
async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in USER_STATE and USER_STATE[chat_id]:
        last_handler = USER_STATE[chat_id].pop()
        await last_handler(update, context)
    else:
        await start(update, context)

def save_state(update: Update, handler):
    chat_id = update.effective_chat.id
    if chat_id not in USER_STATE:
        USER_STATE[chat_id] = []
    USER_STATE[chat_id].append(handler)

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main_keyboard = [
    [KeyboardButton(
        "👥 MY GROUPS",
        request_chat=KeyboardButtonRequestChat(
            request_id=13,
            chat_is_channel=False,
            chat_is_created=True
        )
    )],
    [KeyboardButton("🌐 OTHER")],
]
    markup = ReplyKeyboardMarkup(keyboard=main_keyboard, resize_keyboard=True)
    await update.message.reply_text("""1. Select My Groups using the buttons. 

2. Click on the desired chat — the bot will send its name.

3. Click on the name to open the chat.

If the chat doesn't open, it means the Telegram server is unable to display it, and returning to it won't be possible. 

Choose a section:""", reply_markup=markup)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🧑🏻‍💻 About", callback_data='btn_clicked')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "<b>HELP</b>:\n\nA solution to find Public Private Channels, Groups, Forums with ownership",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'btn_clicked':
        await query.edit_message_text(text="👨🏻‍💻 Creator : @ShuhaibNC")

# My Groups (Ownership-based groups only)
async def show_my_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, start)
    keyboard = [
        [KeyboardButton(
            "👥 Select My Group",
            request_chat=KeyboardButtonRequestChat(
                request_id=13,
                chat_is_channel=False,      # Not a channel
                chat_has_username=None,     # Both public and private
                chat_is_created=True        # User is the creator
            )
        )],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select your owned group:", reply_markup=markup)

# Full menu under "Other"
async def show_own(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, start)
    keyboard = [
        [KeyboardButton("📢 Channels (Own)"), KeyboardButton("👥 Groups (Own)")],
        [KeyboardButton("🗨️ Forums (Own)"), KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose category for ✔️ Own:", reply_markup=markup)

async def show_non_own(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, start)
    keyboard = [
        [KeyboardButton("📢 Channels (Non-Own)"), KeyboardButton("👥 Groups (Non-Own)")],
        [KeyboardButton("🗨️ Forums (Non-Own)"), KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose category for ❌ Non-Own:", reply_markup=markup)

async def show_own_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, show_own)
    keyboard = [
        [KeyboardButton("🔓📢 Public Channels", request_chat=KeyboardButtonRequestChat(request_id=1, chat_is_channel=True, chat_has_username=True, chat_is_created=True))],
        [KeyboardButton("🔐📢 Private Channels", request_chat=KeyboardButtonRequestChat(request_id=2, chat_is_channel=True, chat_has_username=False, chat_is_created=True))],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select channel type (Own):", reply_markup=markup)

async def show_non_own_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, show_non_own)
    keyboard = [
        [KeyboardButton("🔓📢 Public Channels", request_chat=KeyboardButtonRequestChat(request_id=3, chat_is_channel=True, chat_has_username=True))],
        [KeyboardButton("🔐📢 Private Channels", request_chat=KeyboardButtonRequestChat(request_id=4, chat_is_channel=True, chat_has_username=False))],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select channel type (Non-Own):", reply_markup=markup)

async def show_own_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, show_own)
    keyboard = [
        [KeyboardButton("🔓👥 Public Groups", request_chat=KeyboardButtonRequestChat(request_id=5, chat_is_channel=False, chat_has_username=True, chat_is_created=True))],
        [KeyboardButton("🔐👥 Private Groups", request_chat=KeyboardButtonRequestChat(request_id=6, chat_is_channel=False, chat_has_username=False, chat_is_created=True))],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select group type (Own):", reply_markup=markup)

async def show_non_own_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, show_non_own)
    keyboard = [
        [KeyboardButton("🔓👥 Public Groups", request_chat=KeyboardButtonRequestChat(request_id=7, chat_is_channel=False, chat_has_username=True))],
        [KeyboardButton("🔐👥 Private Groups", request_chat=KeyboardButtonRequestChat(request_id=8, chat_is_channel=False, chat_has_username=False))],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select group type (Non-Own):", reply_markup=markup)

async def show_own_forums(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, show_own)
    keyboard = [
        [KeyboardButton("🔓🗨️ Public Forums", request_chat=KeyboardButtonRequestChat(request_id=9, chat_is_channel=False, chat_has_username=True, chat_is_forum=True, chat_is_created=True))],
        [KeyboardButton("🔐🗨️ Private Forums", request_chat=KeyboardButtonRequestChat(request_id=10, chat_is_channel=False, chat_has_username=False, chat_is_forum=True, chat_is_created=True))],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select forum type (Own):", reply_markup=markup)

async def show_non_own_forums(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_state(update, show_non_own)
    keyboard = [
        [KeyboardButton("🔓🗨️ Public Forums", request_chat=KeyboardButtonRequestChat(request_id=11, chat_is_channel=False, chat_has_username=True, chat_is_forum=True))],
        [KeyboardButton("🔐🗨️ Private Forums", request_chat=KeyboardButtonRequestChat(request_id=12, chat_is_channel=False, chat_has_username=False, chat_is_forum=True))],
        [KeyboardButton("↩️ Back")]
    ]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
    await update.message.reply_text("Select forum type (Non-Own):", reply_markup=markup)

# Web server for route integration
async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

# Entry point
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Text("🌐 Other"), show_own))

    app.add_handler(MessageHandler(filters.Text("📢 Channels (Own)"), show_own_channels))
    app.add_handler(MessageHandler(filters.Text("📢 Channels (Non-Own)"), show_non_own_channels))

    app.add_handler(MessageHandler(filters.Text("👥 Groups (Own)"), show_own_groups))
    app.add_handler(MessageHandler(filters.Text("👥 Groups (Non-Own)"), show_non_own_groups))

    app.add_handler(MessageHandler(filters.Text("🗨️ Forums (Own)"), show_own_forums))
    app.add_handler(MessageHandler(filters.Text("🗨️ Forums (Non-Own)"), show_non_own_forums))

    app.add_handler(MessageHandler(filters.Text("↩️ Back"), go_back))

    loop = asyncio.get_event_loop()
    web_app = loop.run_until_complete(web_server())
    web_runner = web.AppRunner(web_app)
    loop.run_until_complete(web_runner.setup())
    loop.create_task(web.TCPSite(web_runner, "0.0.0.0", 8080).start())

    app.run_polling()

if __name__ == "__main__":
    main()