from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os, json

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = 123456789  # ← сюда вставь свой Telegram ID (узнать можно у @userinfobot)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# файл для хранения ID пользователей и чатов
DATA_FILE = "users.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"users": [], "chats": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    data = load_data()
    user_id = message.from_user.id
    chat_id = message.chat.id

    if user_id not in data["users"]:
        data["users"].append(user_id)
    if chat_id < 0 and chat_id not in data["chats"]:  # если это группа
        data["chats"].append(chat_id)

    save_data(data)
    await message.reply("✅ Ви підписалися на оповіщення!")

@dp.message_handler(content_types=["text", "photo", "video"])
async def broadcast(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return  # только владелец может рассылать

    data = load_data()
    targets = data["users"] + data["chats"]

    await message.reply(f"📣 Розсилаю повідомлення {len(targets)} одержувачам...")

    for target in targets:
        try:
            if message.text:
                await bot.send_message(target, message.text)
            elif message.photo:
                await bot.send_photo(target, message.photo[-1].file_id, caption=message.caption or "")
            elif message.video:
                await bot.send_video(target, message.video.file_id, caption=message.caption or "")
        except:
            pass

    await message.reply("✅ Розсилка завершена!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)