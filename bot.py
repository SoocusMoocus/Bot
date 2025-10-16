import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
VIDEO_LIST = {
    "bobozhirvore1": "бобожир воре 1 серия",
    "bobozhirvorehd": "бобожир воре HD",
}
PHOTO_LIST = {
    "kopai": "КОПАЙ",
}
@dp.message_handler(commands=["list"])
async def list_cmd(message: types.Message):
    text = "🎬 Доступные видео:\n"
    for key, desc in VIDEO_LIST.items():
        text += f"{key} - {desc}\n"
    
    text += "\n🖼 Доступные фото:\n"
    for key, desc in PHOTO_LIST.items():
        text += f"{key} - {desc}\n"

    await message.reply(text)
    
@dp.message_handler(commands=["photo"])
async def send_photo(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("📝 Используй: /photo <название файла без расширения>")
        return

    filename = f"photos/{args}.jpg"  # можно менять расширение или добавить проверку
    if not os.path.exists(filename):
        await message.reply("❌ Фото не найдено")
        return

    await message.reply_photo(open(filename, "rb"))
@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет ты в архиве дани 2010 /list - лист всех видео та фото /video - найти видео /photo - найти фото")
# --- Команда /video ---
@dp.message_handler(commands=["video"])
async def send_video(message: types.Message):
    args = message.get_args()
    if not args:
        await message.reply("📝 Используй: /video <название файла без расширения>")
        return

    filename = f"videos/{args}.mp4"
    if not os.path.exists(filename):
        await message.reply("❌ Видео не найдено")
        return

    await message.reply_video(open(filename, "rb"))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
