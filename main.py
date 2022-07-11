import asyncio
import logging
import sys

from aiohttp.web import run_app
from aiohttp.web_app import Application

from config import create_config, ConfigType, Config
from bot import DPBot, BotFactory
from database.models.base import BaseModel
from database.session import SessionManager
from aiogram.dispatcher.webhook.aiohttp_server import setup_application


async def main():
    config = create_config(ConfigType.ENV)
    session_manager = SessionManager(config.data_service_url)
    await session_manager.create_all(BaseModel.metadata)
    bot: DPBot = BotFactory().create_bot(config, session_manager)
    await bot.start_polling()


async def on_startup(config: Config):
    session_manager = SessionManager(config.data_service_url)
    await session_manager.create_all(BaseModel.metadata)


def main_deploy():
    config = create_config(ConfigType.ENV)
    session_manager = SessionManager(config.data_service_url)

    bot = BotFactory().create_bot(config, session_manager)
    bot.dispatcher.startup.register(on_startup)

    app = Application()
    # SimpleRequestHandler(
    #     dispatcher=bot.dispatcher,
    #     bot=bot,
    # ).register(app, path='/webhook')
    setup_application(app, bot.dispatcher, bot=bot)

    run_app(app, host=config.host, port=config.port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    # main_deploy()
