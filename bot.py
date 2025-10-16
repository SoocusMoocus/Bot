import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # твой Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = "subscribers.json"


def load_subscribers():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_subscribers(subs):
    with open(DATA_FILE, "w") as f:
        json.dump(subs, f)


def add_subscriber(chat_id):
    subs = load_subscribers()
    if chat_id not in subs:
        subs.append(chat_id)
        save_subscribers(subs)


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    add_subscriber(message.chat.id)
    await message.answer("✅ Ви підписалися на оповіщення!")


@dp.message_handler(commands=["send"])
async def send_broadcast(message: types.Message):
    # проверяем права
    if message.from_user.id != OWNER_ID:
        await message.reply("🚫 У вас немає прав для цієї команди.")
        return

    subs = load_subscribers()
    if not subs:
        await message.reply("⚠️ Немає підписників для розсилки.")
        return

    # текст после /send
    text = message.get_args()
    if not text:
        await message.reply("📝 Використання: `/send повідомлення`", parse_mode="Markdown")
        return

    sent = 0
    failed = 0

    for cid in subs:
        try:
            await bot.send_message(cid, text)
            sent += 1
        except Exception:
            failed += 1

    await message.reply(f"✅ Успішно: {sent}, ❌ Не вдалося: {failed}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
