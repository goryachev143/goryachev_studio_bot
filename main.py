import asyncio
from bot import create_app

async def main():
    bot, dp = create_app()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
