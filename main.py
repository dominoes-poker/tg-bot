import asyncio
import logging
import sys

from config import create_config, ConfigType, Config
from bot import DPBot, BotFactory
from database.models.base import BaseModel
from database.session import SessionManager


async def initialize_models(config: Config):
    session_manager = SessionManager(config.data_service_url)
    await session_manager.create_all(BaseModel.metadata)


async def main():
    config = create_config(ConfigType.ENV)
    session_manager = SessionManager(config.data_service_url)
    await session_manager.create_all(BaseModel.metadata)
    bot: DPBot = BotFactory().create_bot(config, session_manager)
    bot.dispatcher.startup.register(initialize_models)
    await bot.start_polling(config=config)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    # main_deploy()
