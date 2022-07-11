import asyncio
import logging
import sys

from aiohttp.web import run_app
from aiohttp.web_app import Application

from config import create_config, ConfigType
from bot import DPBot, BotFactory
from database.models.base import BaseModel
from database.session import SessionManager
from aiogram.dispatcher.webhook.aiohttp_server import SimpleRequestHandler, setup_application


async def main():
    config = create_config(ConfigType.ENV)
    session_manager = SessionManager(config.data_service_url)
    await session_manager.async_create_all(BaseModel.metadata)
    bot: DPBot = BotFactory().create_bot(config, session_manager)
    await bot.start_polling()


def main_deploy():
    config = create_config(ConfigType.ENV)
    session_manager = SessionManager(config.data_service_url)
    session_manager.create_all(BaseModel.metadata)
    bot = BotFactory().create_bot(config, session_manager)
    app = Application()
    app['bot'] = bot
    SimpleRequestHandler(
        dispatcher=bot.dispatcher,
        bot=bot,
    ).register(app, path='/webhook')
    setup_application(app, bot.dispatcher, bot=bot)

    run_app(app, host='127.0.0.1', port=8081)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    main_deploy()
