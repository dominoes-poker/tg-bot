from aiogram import F

from bot.bot import TGBot
from bot.routers.router import TGRouter
from bot.services.game_service import GameDataService
from bot.states import RoundState
from bot.routers.game.round.statistics.handler import RoundStatisticsHandler
from bot.routers.common.keyboards import SHOW_STATISTICS_BUTTON

def setup_router(router: TGRouter, handler: RoundStatisticsHandler) -> None:
    statistics_filters = [
        RoundState.STATISTICS, 
        F.text.casefold() == SHOW_STATISTICS_BUTTON.text.lower()
    ]
    router.setup_handler(handler.show_statistics, *statistics_filters)

def create_statistics_router(bot: TGBot,
                            game_data_service: GameDataService) -> TGRouter:
    router = TGRouter(name='<ShowStatistics> - Router')

    handler = RoundStatisticsHandler(bot, game_data_service)
    setup_router(router, handler)

    return router
