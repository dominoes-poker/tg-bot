from aiogram import F

from bot.bot import TGBot
from bot.routers.router import TGRouter
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import MakeBetsState
from bot.routers.game.round.bets.handler import BetsHandler

def setup_router(router: TGRouter, handler: BetsHandler) -> None:
    # ask_player_username_filters = [
    #     RoundState.START, 
    #     F.text.regexp(r'Start the \w+ round')
    # ]
    # router.setup_handler(handler.ask_who_make_bet, *ask_player_username_filters)

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
