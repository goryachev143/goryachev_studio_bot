import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN'  # Замени на свой токен

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

admin_id = YOUR_TELEGRAM_ID  # Замени на свой Telegram ID

# --- Состояния ---
class Form(StatesGroup):
    ChoosingService = State()
    ChoosingCarClass = State()
    EnteringCarModel = State()
    ChoosingDetail = State()
    ChoosingTintPercentage = State()
    ChoosingFilmType = State()
    ConfirmingAdditionalService = State()
    EnteringName = State()
    EnteringPhone = State()
    FinalConfirmation = State()

# --- Кнопки ---
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("Тонировка", "Бронирование")
main_menu.add("Полировка", "Химчистка")

back_button = KeyboardButton("Назад")

# --- Обработчики ---
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Приветствуем в Goryachev Studio! Чем можем быть полезны?", reply_markup=main_menu)
    await Form.ChoosingService.set()

@dp.message_handler(lambda message: message.text == "Назад", state="*")
async def go_back(message: types.Message, state: FSMContext):
    await message.answer("Вы вернулись в главное меню. Выберите услугу:", reply_markup=main_menu)
    await Form.ChoosingService.set()

@dp.message_handler(state=Form.ChoosingService)
async def choose_service(message: types.Message, state: FSMContext):
    service = message.text
    await state.update_data(service=service)
    if service == "Тонировка" or service == "Бронирование":
        car_class_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        car_class_markup.add("Легковой седан", "Кроссовер", "Внедорожник", "Минивэн", "Купе", "Хэтчбек", "Универсал")
        car_class_markup.add(back_button)
        await message.answer("Выберите класс автомобиля:", reply_markup=car_class_markup)
        await Form.ChoosingCarClass.set()
    else:
        await message.answer("Напишите, что хотите сделать (например: Полировка кузова)", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(back_button))
        await Form.EnteringCarModel.set()

@dp.message_handler(state=Form.ChoosingCarClass)
async def choose_class(message: types.Message, state: FSMContext):
    await state.update_data(car_class=message.text)
    await message.answer("Введите марку и модель автомобиля (например: BMW 5 серия):", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(back_button))
    await Form.EnteringCarModel.set()

@dp.message_handler(state=Form.EnteringCarModel)
async def enter_model(message: types.Message, state: FSMContext):
    await state.update_data(car_model=message.text)
    data = await state.get_data()
    if data["service"] == "Тонировка":
        tint_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        tint_markup.add("5%", "15%", "35%", "50%", "70%")
        tint_markup.add(back_button)
        await message.answer("Выберите процент тонировки:", reply_markup=tint_markup)
        await Form.ChoosingTintPercentage.set()
    elif data["service"] == "Бронирование":
        detail_markup = ReplyKeyboardMarkup(resize_keyboard=True)
        detail_markup.add("Капот", "Передняя оптика", "Зеркала", "Бампер", "Крыша", "Вся машина")
        detail_markup.add("Ниши ручек", "Зона погрузки багажника")
        detail_markup.add(back_button)
        await message.answer("Что будем бронировать?", reply_markup=detail_markup)
        await Form.ChoosingDetail.set()
    else:
        await ask_to_continue(message, state)

@dp.message_handler(state=Form.ChoosingTintPercentage)
async def choose_tint(message: types.Message, state: FSMContext):
    await state.update_data(tint=message.text)
    await ask_to_continue(message, state)

@dp.message_handler(state=Form.ChoosingDetail)
async def choose_detail(message: types.Message, state: FSMContext):
    await state.update_data(detail=message.text)
    film_type_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    film_type_markup.add("Гидрогелевая", "Полиуретановая")
    film_type_markup.add(back_button)
    await message.answer("Выберите тип пленки:", reply_markup=film_type_markup)
    await Form.ChoosingFilmType.set()

@dp.message_handler(state=Form.ChoosingFilmType)
async def choose_film(message: types.Message, state: FSMContext):
    await state.update_data(film=message.text)
    await ask_to_continue(message, state)

async def ask_to_continue(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Нет")
    markup.add(back_button)
    await message.answer("Хотите ли вы выбрать ещё какую-то услугу?", reply_markup=markup)
    await Form.ConfirmingAdditionalService.set()

@dp.message_handler(state=Form.ConfirmingAdditionalService)
async def confirm_more(message: types.Message, state: FSMContext):
    if message.text == "Да":
        await message.answer("Выберите услугу:", reply_markup=main_menu)
        await Form.ChoosingService.set()
    else:
        await message.answer("Как вас зовут?", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(back_button))
        await Form.EnteringName.set()

@dp.message_handler(state=Form.EnteringName)
async def enter_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Укажите номер телефона:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(back_button))
    await Form.EnteringPhone.set()

@dp.message_handler(state=Form.EnteringPhone)
async def enter_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()

    client_info = f"""ЗАЯВКА

Услуга: {data.get('service')}
Класс авто: {data.get('car_class')}
Модель: {data.get('car_model')}
Детали: {data.get('detail', '—')}
Пленка: {data.get('film', '—')}
Тонировка: {data.get('tint', '—')}

Имя: {data.get('name')}
Телефон: {data.get('phone')}
"""

    # Отправка админу
    await bot.send_message(admin_id, client_info)

    await message.answer("Спасибо! Мы получили вашу заявку и скоро свяжемся с вами.")
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
