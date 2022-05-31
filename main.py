import asyncio
import logging
import os
import sys
from bot.factory import create_dispatcher

async def main():
    API_TOKEN = os.getenv('TOKEN')
    dispatcher = create_dispatcher(API_TOKEN)
    await dispatcher.polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())