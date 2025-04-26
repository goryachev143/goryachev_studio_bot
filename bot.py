from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'ТВОЙ_ТОКЕН_ТУТ'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот Goryachev Studio!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
