import asyncio
import os
from aiohttp import web
from bot import create_app

async def handle(request):
    return web.Response(text="I'm alive")

async def start_web_app():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 3000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    bot, dp = create_app()
    await start_web_app()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
