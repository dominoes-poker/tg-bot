from aiogram import F
from bot.bot import DPBot
from bot.routers.common.keyboards import BUTTON_SHOW_GAME_STATISTICS, BUTTON_SHOW_ROUND_STATISTICS
from bot.routers.game.round.statistics.handler import StatisticsHandler
from bot.routers.router import DPRouter
from bot.services.game_service import GameDataService
from bot.states import RoundState


def setup_router(router: DPRouter, handler: StatisticsHandler) -> None:
    round_statistics_filters = [
        RoundState.ON_HOLD,
        F.text.casefold() == BUTTON_SHOW_ROUND_STATISTICS.text.lower()
    ]
    router.setup_handler(handler.show_round_statistics, *round_statistics_filters)

    game_statistics_filters = [
        RoundState.ON_HOLD,
        F.text.casefold() == BUTTON_SHOW_GAME_STATISTICS.text.lower()
    ]
    router.setup_handler(handler.show_game_statistics, *game_statistics_filters)

def create_statistics_router(bot: DPBot,
                            game_data_service: GameDataService) -> DPRouter:
    router = DPRouter(name='<ShowStatistics> - Router')

    handler = StatisticsHandler(bot, game_data_service)
    setup_router(router, handler)

    return router
