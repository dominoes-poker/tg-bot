from aiogram import F
from bot.bot import DPBot
from bot.routers.common.keyboards import BUTTON_ENTER_ROUND_RESULTS
from bot.routers.game.round.bets import create_bets_router
from bot.routers.game.round.bribes import create_bribes_router
from bot.routers.game.round.handler import RoundHandler
from bot.routers.game.round.statistics import create_statistics_router
from bot.routers.router import DPRouter
from services.game_service import GameDataService
from bot.states import RoundState


def setup_router(router: DPRouter, handler: RoundHandler) -> None:
    router.setup_handler(
        handler.start_round,
        RoundState.START, F.text.regexp(r'Start the \d.* round')
    )
    router.setup_handler(
        handler.start_round,
        RoundState.ON_HOLD, F.text.regexp(r'Start the \d.* round')
    )
    router.setup_handler(
        handler.finish_round,
        RoundState.BRIBES, F.text == BUTTON_ENTER_ROUND_RESULTS.text
    )


def create_round_router(bot: DPBot,
                        game_data_service: GameDataService) -> DPRouter:

    bet_router, make_bet_handler = create_bets_router(bot, game_data_service)
    bribes_router, set_bribes_handler = create_bribes_router(bot, game_data_service)
    statistics_router = create_statistics_router(bot, game_data_service)

    router = DPRouter(name='<Round> - Router')
    handler = RoundHandler(bot, make_bet_handler, set_bribes_handler, game_data_service)

    setup_router(router, handler)
    router.include_router(bet_router)
    router.include_router(bribes_router)
    router.include_router(statistics_router)

    return router
