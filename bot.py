import os
import asyncio
import sqlite3
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")
bot = Bot(TOKEN)
dp = Dispatcher()

db = sqlite3.connect("farm.db")
db.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    clicks INTEGER DEFAULT 0,
    balance INTEGER DEFAULT 0
)""")
db.commit()

@dp.message(CommandStart())
async def start(message: Message):
    db.execute("INSERT OR IGNORE INTO users(id) VALUES(?)", (message.from_user.id,))
    db.commit()
    if WEBAPP_URL.startswith("https://"):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text="⭐ Играть в FARM ЗВЕЗД",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]])
        await message.answer("⭐ Добро пожаловать в FARM ЗВЕЗД!", reply_markup=keyboard)
    else:
        await message.answer("⭐ FARM ЗВЕЗД создан! Мини-приложение ещё настраивается.")

async def health(request):
    return web.Response(text="FARM ZVEZD bot is running")

async def main():
    app = web.Application()
    app.router.add_get("/", health)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", "8080")))
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
