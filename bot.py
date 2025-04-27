import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Вставь сюда свой токен бота
TOKEN = '7755776750:AAHaFINi5nwT__E93inT9GfxkQycGUf-HS0'

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Стартовая команда
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я работаю 24/7!')

def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    # Команда /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
