from typing import List
from aiogram import Dispatcher, Router
from bot.handlers import WellcomeEventHandler
from bot.services.factory import get_gamer_data_service
from bot.tgbot import TGBot
from routers.router import RootRouter


def create_dispatcher(routers: List[Router]) -> Dispatcher:
    dispatcher = Dispatcher()

    for router in routers:
        dispatcher.include_router(router)
    
    return dispatcher

def create_bot(token: str) -> TGBot:
    handler = WellcomeEventHandler(get_gamer_data_service())
    router = RootRouter(handler)
    dispatcher = create_dispatcher([router,])
    return TGBot(token, dispatcher)
