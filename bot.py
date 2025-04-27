import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Твой токен
TOKEN = "7755776750:AAHaFINi5nwT__E93inT9GfxkQycGUf-HS0"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём клавиатуру
main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📋 Записаться на услуги")],
    [KeyboardButton(text="💰 Узнать цены")],
    [KeyboardButton(text="☎️ Связаться с нами")]
], resize_keyboard=True)

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в Goryachev Studio!\n\n"
        "Выберите действие:",
        reply_markup=main_keyboard
    )

# Обработчик нажатий на кнопки
@dp.message()
async def handle_buttons(message: types.Message):
    if message.text == "📋 Записаться на услуги":
        await message.answer("Чтобы записаться на услуги, напишите нам в директ: @GoryachevStudioBot")
    elif message.text == "💰 Узнать цены":
        await message.answer("Прайс-лист доступен на нашем сайте или в директе. Напишите нам!")
    elif message.text == "☎️ Связаться с нами":
        await message.answer("Телефон: +7 (999) 999-99-99\nАдрес: г. Челябинск, ул. Примерная, 123")

# Основная функция запуска
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
