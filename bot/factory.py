from typing import List

from bot.bot import TGBot

from bot.routers import TGRouter, create_wellcome_router, create_game_register_router
from bot.dispatcher import TGDispatcher
from bot.routers.game_router import create_root_game_router
from bot.services.game_service.factory import get_game_data_service
from bot.services.gamer_service import get_gamer_data_service



def create_bot(token: str) -> TGBot:
    return TGBot(token)

def create_dispatcher(token: str) -> TGDispatcher:
    bot = create_bot(token)
    dispatcher = TGDispatcher(bot)
    create_routers(dispatcher)

    return dispatcher


def create_routers(dispatcher: TGDispatcher) -> List[TGRouter]:
    gamer_data_service = get_gamer_data_service()
    game_data_service = get_game_data_service()
    return [
        create_wellcome_router(dispatcher, gamer_data_service),
        create_game_register_router(dispatcher, gamer_data_service),
        create_root_game_router(dispatcher, gamer_data_service, game_data_service)
    ]
