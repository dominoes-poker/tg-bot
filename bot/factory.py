from typing import List
from aiogram import Dispatcher, Router
from bot.routers.gamer_register_router import GamerRegisterRouter, create_gamer_register_router

from bot.routers.wellcome_router import WellcomeRouter, create_wellcome_router
from bot.services.factory import get_gamer_data_service
from bot.tgbot import TGBot
from bot.routers.router import RootRouter


def create_dispatcher(routers: List[Router]) -> Dispatcher:
    dispatcher = Dispatcher()

    for router in routers:
        dispatcher.include_router(router)
    
    return dispatcher

def create_bot(token: str) -> TGBot:
    gamer_data_service = get_gamer_data_service()
    wellcome_router: WellcomeRouter = create_wellcome_router(gamer_data_service)
    gamer_register_router: GamerRegisterRouter = create_gamer_register_router(gamer_data_service)
    router = RootRouter(wellcome_router, gamer_register_router)
    dispatcher = create_dispatcher([router,])
    return TGBot(token, dispatcher)
