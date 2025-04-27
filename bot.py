from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = 'твой токен бота'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот студии Goryachev Studio! Чем могу помочь?")

if __name__ == '__main__':
    executor.start_polling(dp)
