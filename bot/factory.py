from typing import Tuple

from aiogram import Dispatcher

from config import Config

from bot.bot import DPBot
from bot.routers import (DPRouter, create_player_register_router,
                         create_root_game_router, create_wellcome_router,
                         create_help_router)
from database.session import SessionManager
from services.game_service.factory import get_game_data_service
from services.player_service import get_player_data_service


class BotFactory:

    @classmethod
    def create_bot(cls, config: Config, session_manager: SessionManager) -> DPBot:
        bot = DPBot(config.token)
        cls._attach_dispatcher(bot, config, session_manager)
        return bot

    @classmethod
    def _attach_dispatcher(cls, bot: DPBot, config: Config, session_manager: SessionManager) -> None:
        bot.dispatcher = Dispatcher()
        routers = cls._create_routers(bot, session_manager)
        for router in routers:
            bot.dispatcher.include_router(router)

    @classmethod
    def _create_routers(cls, bot: DPBot, session_manager: SessionManager) -> Tuple[DPRouter, ...]:

        player_data_service = get_player_data_service(session_manager)
        game_data_service = get_game_data_service(session_manager)

        return (
            create_wellcome_router(bot, player_data_service),
            create_player_register_router(bot, player_data_service),
            create_root_game_router(bot, player_data_service, game_data_service),
            create_help_router(bot)
        )
