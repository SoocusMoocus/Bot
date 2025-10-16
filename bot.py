import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))  # твой Telegram ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

DATA_FILE = "subscribers.json"


# --- Хранилище подписчиков ---
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


# --- Добавление при /start или любом сообщении в чате ---
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    add_subscriber(message.chat.id)
    await message.answer("✅ Ви підписалися на оповіщення!")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def on_text(message: types.Message):
    # Если бот в чате, добавляем его (на случай, если он уже там)
    if message.chat.type in ["group", "supergroup"]:
        add_subscriber(message.chat.id)


# --- Если бота только что добавили ---
@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
async def on_new_member(message: types.Message):
    for member in message.new_chat_members:
        if member.id == (await bot.me).id:
            add_subscriber(message.chat.id)
            await message.reply("✅ Бот активований у цьому чаті!")


# --- /send для владельца ---
@dp.message_handler(commands=["send"], content_types=types.ContentTypes.ANY)
async def send_broadcast(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🚫 У вас немає прав для цієї команди.")

    subs = load_subscribers()
    if not subs:
        return await message.reply("⚠️ Немає підписників для розсилки.")

    sent = 0
    failed = 0

    # Медиа-рассылка
    if message.photo:
        file_id = message.photo[-1].file_id
        caption = message.caption or ""
        for cid in subs:
            try:
                await bot.send_photo(cid, file_id, caption=caption)
                sent += 1
            except Exception:
                failed += 1

    elif message.video:
        file_id = message.video.file_id
        caption = message.caption or ""
        for cid in subs:
            try:
                await bot.send_video(cid, file_id, caption=caption)
                sent += 1
            except Exception:
                failed += 1

    elif message.document:
        file_id = message.document.file_id
        caption = message.caption or ""
        for cid in subs:
            try:
                await bot.send_document(cid, file_id, caption=caption)
                sent += 1
            except Exception:
                failed += 1

    else:
        text = message.text.replace("/send", "").strip()
        if not text:
            return await message.reply("📝 Використання: `/send повідомлення`", parse_mode="Markdown")
        for cid in subs:
            try:
                await bot.send_message(cid, text)
                sent += 1
            except Exception:
                failed += 1

    await message.reply(f"✅ Успішно: {sent}, ❌ Помилка: {failed}")


# --- Запуск ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
