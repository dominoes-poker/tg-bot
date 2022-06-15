from aiogram import F

from bot.bot import TGBot
from bot.routers.game.handlers.make_bets_handler import MakeBetsHandler
from bot.routers.router import TGRouter
from bot.services.game_service import GameDataService
from bot.states import MakeBetsState, RoundState


class MakeBetsRouter(TGRouter):
    def __init__(self, handler: MakeBetsHandler) -> None:
        super().__init__(use_builtin_filters=True, name='MakeBetsRouter')
        self.setup(handler=handler)
        self._handler = handler
    
    @property
    def handler(self) -> MakeBetsHandler:
        return self._handler

    def setup(self, handler: MakeBetsHandler) -> None:
        self.setup_handler(handler.ask_who_make_bet, RoundState.START, F.text.regexp(r'Start the \w+ round'))
        self.setup_handler(handler.handle_username, MakeBetsState.USERNAME)
        self.setup_handler(handler.handle_bet, MakeBetsState.BET, F.text.regexp(r'\d+'))


def create_make_bets_router(bot: TGBot,
                            game_data_service: GameDataService) -> MakeBetsRouter:
    handler = MakeBetsHandler(bot, game_data_service)
    return MakeBetsRouter(handler)
