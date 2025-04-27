import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Твой токен
TOKEN = "7755776750:AAHaFINi5nwT__E93inT9GfxkQycGUf-HS0"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создаём клавиатуру с услугами
services_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🚗 Тонировка"), KeyboardButton(text="🛡 Бронирование плёнкой")],
    [KeyboardButton(text="✨ Полировка кузова"), KeyboardButton(text="🧼 Химчистка салона")],
    [KeyboardButton(text="📋 Записаться"), KeyboardButton(text="☎️ Связаться с нами")]
], resize_keyboard=True)

# Обработчик команды /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать в *Goryachev Studio*!\n\n"
        "Мы профессионально занимаемся:\n"
        "🚗 Тонировкой\n"
        "🛡 Бронированием плёнкой\n"
        "✨ Полировкой кузова\n"
        "🧼 Химчисткой салона\n\n"
        "Выберите интересующую услугу из меню ниже!",
        reply_markup=services_keyboard,
        parse_mode="Markdown"
    )

# Обработчик нажатий на кнопки
@dp.message()
async def handle_buttons(message: types.Message):
    if message.text == "🚗 Тонировка":
        await message.answer("🚗 Тонировка автомобилей качественными плёнками. Пожизненная гарантия!")
    elif message.text == "🛡 Бронирование плёнкой":
        await message.answer("🛡 Защита кузова от сколов и царапин премиальными плёнками.")
    elif message.text == "✨ Полировка кузова":
        await message.answer("✨ Восстановление блеска кузова, удаление мелких царапин и дефектов лака.")
    elif message.text == "🧼 Химчистка салона":
        await message.answer("🧼 Глубокая чистка салона автомобиля профессиональной автохимией.")
    elif message.text == "📋 Записаться":
        await message.answer("Для записи напишите сюда: @GoryachevStudioBot\nИли позвоните: +7 (999) 999-99-99")
    elif message.text == "☎️ Связаться с нами":
        await message.answer("☎️ Наш телефон: +7 (999) 999-99-99\nАдрес: г. Челябинск, ул. Примерная, 123")

# Основная функция запуска
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
