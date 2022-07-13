from aiogram import F

from bot.bot import DPBot
from bot.routers.common.keyboards import BUTTON_FINISH_GAME
from bot.routers.game.finish.handler import FinishGameHandler
from bot.routers.router import DPRouter
from services.game_service import GameDataService


def setup_router(router: DPRouter, handler: FinishGameHandler) -> None:
    finish_filters = [F.text == BUTTON_FINISH_GAME.text]
    router.setup_handler(handler.finish, *finish_filters)


def create_finish_game_router(bot: DPBot, game_data_service: GameDataService) -> DPRouter:
    router = DPRouter(name='<FinishGame> - Router')

    handler = FinishGameHandler(bot, game_data_service)
    setup_router(router, handler)

    return router
