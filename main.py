from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import logging

logging.basicConfig(level=logging.INFO)

app = Client(
    "my_bot",
    api_id=3616787,
    api_hash="e49f6597a66149243a7baf5df57c0337",
    bot_token="7629727539:AAE4UqcP0lTXXf3WaKFDEvxON13zbnhyGlA"
)

@app.on_message(filters.command("start"))
def start(client, message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("My Channels")],
            [KeyboardButton("My Groups")]
        ],
        resize_keyboard=True
    )
    message.reply("Hell9\n\nChoose an option:", reply_markup=keyboard)

@app.on_message(filters.text)
def handle_options(client, message: Message):
    if message.text == "My Channels":
        message.reply("You selected: My Channels")
    elif message.text == "My Groups":
        message.reply("You selected: My Groups")
    else:
        message.reply("Use the menu to choose.")

app.run()