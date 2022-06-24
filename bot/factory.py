from aiogram import Dispatcher
from typing import List

from aiogram import Dispatcher
from bot.bot import TGBot

from bot.routers import TGRouter, create_wellcome_router, create_player_register_router
from bot.routers.game import create_root_game_router
from bot.services.game_service.factory import get_game_data_service
from bot.services.player_service import get_player_data_service

from config import Config

class BotFactory:
    
    @classmethod
    def create_bot(self, config: Config) -> TGBot:
        bot = TGBot(config.token)
        self._attach_dispatcher(bot, config)
        return bot

    @classmethod
    def _attach_dispatcher(cls, bot: TGBot, config: Config) -> None:
        bot.dispatcher = Dispatcher()
        routers = cls._create_routers(bot, config)
        for router in routers:
            bot.dispatcher.include_router(router)

    @classmethod
    def _create_routers(cls, bot: TGBot, config: Config) -> List[TGRouter]:
        player_data_service = get_player_data_service(config.data_service_url)
        game_data_service = get_game_data_service(config.data_service_url)

        return [
            create_wellcome_router(bot, player_data_service),
            create_player_register_router(bot, player_data_service),
            create_root_game_router(bot, player_data_service, game_data_service)
        ]
