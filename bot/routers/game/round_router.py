from aiogram import F
from bot.bot import TGBot
from bot.routers.game.handlers.round_handler import RoundHandler
from bot.routers.game.make_bets_router import create_make_bets_router
from bot.routers.game.set_birbes_router import create_set_bribes_router
from bot.routers.handlers.common.keyboards import BUTTON_ENTER_ROUND_RESULTS

from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.states import RoundState


class RoundRouter(TGRouter):
    def __init__(self, handler: RoundHandler) -> None:
        super().__init__(use_builtin_filters=True, name='RoundRouter')
        self.setup(handler=handler)

    def setup(self, handler: RoundHandler) -> None:
        self.setup_handler(handler.start_round, RoundState.START, F.text.regexp(r'Start the \w+ round'))
        self.setup_handler(handler.finish_round, RoundState.BRIBES, F.text == BUTTON_ENTER_ROUND_RESULTS.text)
        
def create_round_router(bot: TGBot,
                        game_data_service: GameDataService) -> RoundRouter:
    
    make_bet_router = create_make_bets_router(bot, game_data_service)
    set_bribes_router = create_set_bribes_router(bot, game_data_service)
    
    handler = RoundHandler(bot, make_bet_router.handler, set_bribes_router.handler, game_data_service)
    router = RoundRouter(handler)
    
    router.include_router(make_bet_router)
    router.include_router(set_bribes_router)
    return router
