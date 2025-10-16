import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Команда /photo ---
@dp.message_handler(commands=["photo"])
async def send_photo(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("📝 Використання: /photo <название файла без расширения>")
        return

    filename = f"photos/{args}.jpg"  # можно менять расширение или добавить проверку
    if not os.path.exists(filename):
        await message.reply("❌ Фото не найдено")
        return

    await message.reply_photo(open(filename, "rb"))
@dp.message_handler(commands=["start"])    
await message.reply("hyi")
# --- Команда /video ---
@dp.message_handler(commands=["video"])
async def send_video(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("📝 Використання: /video <название файла без расширения>")
        return

    filename = f"videos/{args}.mp4"
    if not os.path.exists(filename):
        await message.reply("❌ Видео не найдено")
        return

    await message.reply_video(open(filename, "rb"))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
