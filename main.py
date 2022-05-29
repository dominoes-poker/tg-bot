import asyncio
import logging
import sys

from bot.factory import create_bot

async def main():
    API_TOKEN = ''
    bot = create_bot(API_TOKEN)
    await bot.polling()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())