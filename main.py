import asyncio
import logging
import os
import sys
from bot.factory import create_bot, create_dispatcher

async def main():
    API_TOKEN = os.getenv('TOKEN')
    bot = create_bot(API_TOKEN)
    dispatcher = create_dispatcher(bot)
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())