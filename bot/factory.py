from typing import List

from aiogram import Dispatcher

from bot.bot import TGBot

from bot.routers import TGRouter, create_wellcome_router, create_player_register_router
from bot.routers.game import create_root_game_router
from bot.services.game_service.factory import get_game_data_service
from bot.services.player_service import get_player_data_service


def create_bot(token: str) -> TGBot:
    return TGBot(token)

def create_dispatcher(bot: TGBot) -> Dispatcher:
    dispatcher = Dispatcher()
    routers = create_routers(bot)
    for router in routers:
        dispatcher.include_router(router)
    return dispatcher

def create_routers(bot: TGBot) -> List[TGRouter]:
    player_data_service = get_player_data_service()
    game_data_service = get_game_data_service()

    return [
        create_wellcome_router(bot, player_data_service),
        create_player_register_router(bot, player_data_service),
        create_root_game_router(bot, player_data_service, game_data_service)
    ]
