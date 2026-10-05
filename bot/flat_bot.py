import os, asyncio, logging
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from handlers import router


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
disp = Dispatcher()

async def main():
    disp.include_router(router)
    await disp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("exit")