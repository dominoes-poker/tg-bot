from typing import List

from aiogram import Dispatcher

from bot.bot import TGBot

from bot.routers import TGRouter, create_wellcome_router, create_gamer_register_router
from bot.routers.game_router import create_root_game_router
from bot.services.game_service.factory import get_game_data_service
from bot.services.gamer_service import get_gamer_data_service


def create_bot(token: str) -> TGBot:
    return TGBot(token)

def create_dispatcher(bot: TGBot) -> Dispatcher:
    dispatcher = Dispatcher()
    routers = create_routers(bot)
    for router in routers:
        dispatcher.include_router(router)
    return dispatcher

def create_routers(bot: TGBot) -> List[TGRouter]:
    gamer_data_service = get_gamer_data_service()
    game_data_service = get_game_data_service()

    return [
        create_wellcome_router(bot, gamer_data_service),
        create_gamer_register_router(bot, gamer_data_service),
        create_root_game_router(bot, gamer_data_service, game_data_service)
    ]
