import asyncio
import logging
import sys

from config import create_config, ConfigType
from bot import TGBot, BotFactory

async def main():
    config = create_config(ConfigType.ENV)
    bot: TGBot = BotFactory().create_bot(config)
    await bot.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
