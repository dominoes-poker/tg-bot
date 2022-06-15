from aiogram import F
from bot.bot import TGBot
from bot.routers.game.handlers.set_bribes_handler import SetBribesHandler

from bot.routers.router import TGRouter
from bot.services.game_service.game_data_service import GameDataService
from bot.states import RoundState


class SetBribesRouter(TGRouter):
    def __init__(self, handler: SetBribesHandler) -> None:
        super().__init__(use_builtin_filters=True, name='RoundRouter')
        self._handler = handler
        self.setup(handler=handler)
        
    @property
    def handler(self) -> SetBribesHandler:
        return self._handler

    def setup(self, handler: SetBribesHandler) -> None:
        self.setup_handler(handler.handle_result, RoundState.WAIT_RESULT_OF_PLAYER, F.text.regexp(r'\d+'))


def create_set_bribes_router(bot: TGBot,
                             game_data_service: GameDataService) -> SetBribesRouter:
    handler = SetBribesHandler(bot, game_data_service)
    return SetBribesRouter(handler)
