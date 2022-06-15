from aiogram import F
from bot.bot import TGBot
from bot.routers.game.handlers.make_bets_handler import MakeBetsHandler
from bot.routers.handlers.common.keyboards import BUTTON_NEW_GAME

from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import GameState, RoundState


class MakeBetsRouter(TGRouter):
    def __init__(self, handler: MakeBetsHandler) -> None:
        super().__init__(use_builtin_filters=True, name='MakeBetsRouter')
        self.setup(handler=handler)
        self._handler = handler
    
    @property
    def handler(self) -> MakeBetsHandler:
        return self._handler

    def setup(self, handler: MakeBetsHandler) -> None:
        self.setup_handler(handler.ask_who_make_bet, GameState.START_ROUND, F.text.regexp(r'Start the \w+ round'))
        self.setup_handler(handler.handle_username, RoundState.WAIT_USERNAME_TO_BET)
        self.setup_handler(handler.handle_bet, RoundState.WAIT_BET_OF_PLAYER, F.text.regexp(r'\d+'))


def create_make_bets_router(bot: TGBot,
                            game_data_service: GameDataService) -> MakeBetsRouter:
    handler = MakeBetsHandler(bot, game_data_service)
    return MakeBetsRouter(handler)
