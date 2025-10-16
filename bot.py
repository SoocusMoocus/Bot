import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # твой Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = "users.json"

# --- Загрузка списка пользователей ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)

# --- Сохранение списка пользователей ---
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# --- Добавление пользователя ---
def add_user(user_id):
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)

# --- Команда /start ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("✅ Ви підписалися на оповіщення!")

# --- Команда /send (только для владельца) ---
@dp.message_handler(commands=["send"])
async def send_broadcast(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("🚫 У вас немає прав для цієї команди.")
        return

    text = message.text.replace("/send", "").strip()
    if not text:
        await message.answer("📝 Використання: `/send текст повідомлення`", parse_mode="Markdown")
        return

    users = load_users()
    count = 0

    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            count += 1
        except Exception:
            pass

    await message.answer(f"✅ Повідомлення надіслано {count} користувачам.")

# --- Запуск ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
