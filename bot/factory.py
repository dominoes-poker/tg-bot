from typing import Tuple

from aiogram import Dispatcher

from config import Config

from bot.bot import DPBot
from bot.routers import (DPRouter, create_player_register_router,
                         create_root_game_router, create_wellcome_router,
                         create_help_router)
from bot.services.game_service.factory import get_game_data_service
from bot.services.player_service import get_player_data_service


class BotFactory:

    @classmethod
    def create_bot(cls, config: Config) -> DPBot:
        bot = DPBot(config.token)
        cls._attach_dispatcher(bot, config)
        return bot

    @classmethod
    def _attach_dispatcher(cls, bot: DPBot, config: Config) -> None:
        bot.dispatcher = Dispatcher()
        routers = cls._create_routers(bot, config)
        for router in routers:
            bot.dispatcher.include_router(router)

    @classmethod
    def _create_routers(cls, bot: DPBot, config: Config) -> Tuple[DPRouter]:

        player_data_service = get_player_data_service(config.data_service_url)
        game_data_service = get_game_data_service(config.data_service_url)

        return (
            create_wellcome_router(bot, player_data_service),
            create_player_register_router(bot, player_data_service),
            create_root_game_router(bot, player_data_service, game_data_service),
            create_help_router(bot)
        )
