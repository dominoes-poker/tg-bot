from pathlib import Path

from bot.bot import DPBot
from bot.messages.factory import create_message_service
from bot.routers.wellocme.handler import WellcomeHandler
from bot.routers.router import DPRouter
from config import Config
from services.player_service import PlayerDataService


def setup_router(router: DPRouter, handler: WellcomeHandler) -> None:
    router.setup_handler(handler.handle_enter, commands=['start'])


def create_wellcome_router(config: Config, bot: DPBot, player_data_service: PlayerDataService ) -> DPRouter:
    message_service = create_message_service('wellcome', config.message_path)

    handler = WellcomeHandler(bot, message_service, player_data_service)

    router = DPRouter(name='<Wellcome> - Router')
    setup_router(router, handler)

    return router
