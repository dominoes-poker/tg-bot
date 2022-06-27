from aiogram import F

from bot.bot import TGBot
from bot.routers.router import TGRouter
from bot.services.game_service import GameDataService
from bot.states import MakeBetsState
from bot.routers.game.round.bets.handler import BetsHandler

def setup_router(router: TGRouter, handler: BetsHandler) -> None:
    username_filters = [MakeBetsState.USERNAME]
    router.setup_handler(handler.handle_username, *username_filters)

    bet_filters = [MakeBetsState.BET, F.text.regexp(r'\d+')]
    router.setup_handler(handler.handle_bet, *bet_filters)

def create_bets_router(bot: TGBot,
                            game_data_service: GameDataService) -> TGRouter:
    router = TGRouter(name='<Bets> - Router')

    handler = BetsHandler(bot, game_data_service)
    setup_router(router, handler)

    return router, handler
