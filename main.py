import asyncio
import logging
import sys

from config import create_config, ConfigType
from bot import DPBot, BotFactory
from database.models.base import BaseModel
from database.session import SessionManager

async def main():
    config = create_config(ConfigType.ENV)
    session_manager = SessionManager(config.data_service_url)
    await session_manager.create_all(BaseModel.metadata)
    bot: DPBot = BotFactory().create_bot(config, session_manager)
    await bot.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
