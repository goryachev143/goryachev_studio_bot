import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

TOKEN = "7755776750:AAHaFINi5nwT__E93inT9GfxkQycGUf-HS0"
ADMIN_CHAT_ID = "7681110461"  # Твой чат ID

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

# Машина состояний для анкеты
class Form(StatesGroup):
    service = State()
    subservice = State()
    tint_shade = State()
    name = State()
    phone = State()
    car = State()
    datetime = State()

# Клавиатура с основными услугами
main_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тонировка автомобилей")],
    [KeyboardButton(text="Бронирование плёнкой")],
    [KeyboardButton(text="Полировка кузова")],
    [KeyboardButton(text="Химчистка салона")],
], resize_keyboard=True)

# Клавиатура с вариантами тонировки
tinting_options = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Тонировка автомобиля в круг")],
    [KeyboardButton(text="Тонировка передней полусферы")],
    [KeyboardButton(text="Тонировка задней полусферы")],
    [KeyboardButton(text="Тонировка передних двух боковых стёкол")],
    [KeyboardButton(text="Тонировка задних двух боковых стёкол")],
    [KeyboardButton(text="Тонировка лобового стекла")],
    [KeyboardButton(text="Тонировка заднего стекла")],
    [KeyboardButton(text="Тонировка одного стекла")],
    [KeyboardButton(text="Тонировка одной форточки")],
    [KeyboardButton(text="Тонировка полосы 14см по ГОСТу")],
    [KeyboardButton(text="Растонировка")],
], resize_keyboard=True)

# Клавиатура для выбора светопропускания
tint_shades = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="5"), KeyboardButton(text="15"), KeyboardButton(text="20")],
    [KeyboardButton(text="35"), KeyboardButton(text="50"), KeyboardButton(text="70")],
    [KeyboardButton(text="80 (оттормалка)")],
], resize_keyboard=True)

# Клавиатура для растонировки
remove_tint_options = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Растонировка задней полусферы")],
    [KeyboardButton(text="Растонировка передней полусферы")],
    [KeyboardButton(text="Растонировка лобового стекла")],
    [KeyboardButton(text="Растонировка заднего стекла")],
    [KeyboardButton(text="Растонировка двух стёкол")],
    [KeyboardButton(text="Растонировка одного стекла")],
    [KeyboardButton(text="Растонировка одной форточки")],
    [KeyboardButton(text="Снятие полосы")],
], resize_keyboard=True)

# Стартовая команда
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await message.answer(
        "👋 Добро пожаловать в <b>Goryachev Studio</b>!\n\n"
        "Мы профессионально занимаемся:\n\n"
        "🚗 <b>Тонировкой автомобилей</b>\n"
        "🛡 <b>Бронированием плёнкой</b>\n"
        "✨ <b>Полировкой кузова</b>\n"
        "🧼 <b>Химчисткой салона</b>\n\n"
        "Выберите интересующую услугу в меню ниже!",
        reply_markup=main_menu
    )
    await state.set_state(Form.service)

# Выбор услуги
@dp.message(Form.service)
async def choose_service(message: types.Message, state: FSMContext):
    await state.update_data(service=message.text)

    if message.text == "Тонировка автомобилей":
        await message.answer("Выберите вариант тонировки:", reply_markup=tinting_options)
        await state.set_state(Form.subservice)
    else:
        await ask_contacts(message, state)

# Выбор подуслуги
@dp.message(Form.subservice)
async def choose_subservice(message: types.Message, state: FSMContext):
    await state.update_data(subservice=message.text)

    if message.text == "Растонировка":
        await message.answer("Выберите вариант растонировки:", reply_markup=remove_tint_options)
    elif "Растонировка" in message.text:
        await message.answer(
            "⚡ Внимание!\n\n"
            "Goryachev Studio не несет ответственности за демонтаж плёнки с заднего стекла. "
            "Существует риск повреждения нитей обогрева во время снятия плёнки (примерно 50 на 50). "
            "Пожалуйста, учитывайте это перед началом работы."
        )
        await ask_contacts(message, state)
    else:
        await message.answer("Выберите светопропускание плёнки:", reply_markup=tint_shades)
        await state.set_state(Form.tint_shade)

# Выбор светопропускания
@dp.message(Form.tint_shade)
async def choose_shade(message: types.Message, state: FSMContext):
    await state.update_data(tint_shade=message.text)
    await ask_contacts(message, state)

# Сбор контактов
async def ask_contacts(message: types.Message, state: FSMContext):
    await message.answer(
        "Почти готово!\n\n"
        "Пожалуйста, отправьте свои контактные данные, чтобы с вами связался менеджер из Goryachev Studio."
    )
    await message.answer("Введите ваше имя:")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def ask_phone(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(Form.phone)

@dp.message(Form.phone)
async def ask_car(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("Введите марку и модель автомобиля:")
    await state.set_state(Form.car)

@dp.message(Form.car)
async def ask_datetime(message: types.Message, state: FSMContext):
    await state.update_data(car=message.text)
    await message.answer("Укажите желаемую дату и время записи:")
    await state.set_state(Form.datetime)

@dp.message(Form.datetime)
async def send_application(message: types.Message, state: FSMContext):
    await state.update_data(datetime=message.text)
    data = await state.get_data()

    # Отправляем данные в админский чат
    text = (
        f"<b>Новая заявка!</b>\n\n"
        f"<b>Услуга:</b> {data.get('service')}\n"
        f"<b>Подуслуга:</b> {data.get('subservice', 'Не указана')}\n"
        f"<b>Светопропускание:</b> {data.get('tint_shade', 'Не указано')}\n\n"
        f"<b>Имя клиента:</b> {data.get('name')}\n"
        f"<b>Телефон:</b> {data.get('phone')}\n"
        f"<b>Авто:</b> {data.get('car')}\n"
        f"<b>Дата и время записи:</b> {data.get('datetime')}"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)

    # Сообщение клиенту
    await message.answer(
        "✅ Ваши данные успешно получены!\n\n"
        "В течение 5–10 минут с вами свяжется менеджер."
    )
    await message.answer("Отличного настроения и хорошего дня! Спасибо, что выбрали Goryachev Studio!")

    # Адрес
    await message.answer(
        "📍 Мы находимся по адресу:\n"
        "<b>г. Челябинск, Копейское шоссе 40Б/1</b>"
    )

    # Завершаем анкету
    await state.clear()

if __name__ == "__main__":
    import asyncio
    async def main():
        await dp.start_polling(bot)
    asyncio.run(main())
