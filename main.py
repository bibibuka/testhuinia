import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F
from openai import AsyncOpenAI


# ========== Настройки ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
try:
    with open("promt.txt", "r", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read().strip()
except FileNotFoundError:
    print("Файл promt.txt не найден. Используется дефолтный промт.")
    SYSTEM_PROMPT = "Ты — вежливый и лаконичный Telegram-бот."

# === ИНИЦИАЛИЗАЦИЯ ===
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
openai = AsyncOpenAI(api_key=OPENAI_API_KEY)

# === /start ===
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Привет! Напиши мне что-нибудь, и я отвечу с помощью GPT.")

# === ОБРАБОТКА СООБЩЕНИЙ ===
@dp.message(F.text)
async def handle_text(message: Message):
    try:
        user_input = message.text

        response = await openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content.strip()
        await message.answer(result)

    except Exception as e:
        print("[OpenAI ошибка]:", e)
        await message.answer("Произошла ошибка при обработке запроса.")

# === ЗАПУСК ===
if __name__ == "__main__":
    print("✅ Бот запущен и слушает сообщения...")
    asyncio.run(dp.start_polling(bot))
