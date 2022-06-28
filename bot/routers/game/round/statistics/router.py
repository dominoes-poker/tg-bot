from aiogram import F
from bot.bot import DPBot
from bot.routers.common.keyboards import BUTTON_SHOW_ROUND_STATISTICS
from bot.routers.game.round.statistics.handler import RoundStatisticsHandler
from bot.routers.router import DPRouter
from bot.services.game_service import GameDataService
from bot.states import RoundState


def setup_router(router: DPRouter, handler: RoundStatisticsHandler) -> None:
    statistics_filters = [
        RoundState.STATISTICS,
        F.text.casefold() == BUTTON_SHOW_ROUND_STATISTICS.text.lower()
    ]
    router.setup_handler(handler.show_statistics, *statistics_filters)

def create_statistics_router(bot: DPBot,
                            game_data_service: GameDataService) -> DPRouter:
    router = DPRouter(name='<ShowStatistics> - Router')

    handler = RoundStatisticsHandler(bot, game_data_service)
    setup_router(router, handler)

    return router
