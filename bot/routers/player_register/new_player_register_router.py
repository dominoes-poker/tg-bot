from aiogram import F
from bot.bot import TGBot
from bot.routers.handlers.common.keyboards import BUTTON_ADD_GAMER
from bot.routers.player_register.handlers import NewPlayerRegisterHandler
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService
from bot.states import NewPlayerRegisterState, RootState


class NewPlayerRegisterRouter(TGRouter):
    def __init__(self, handler: NewPlayerRegisterHandler) -> None:
        super().__init__(use_builtin_filters=True, name='NewPlayerRegisterRouter')
        self.setup(handler=handler)

    def setup(self, handler: NewPlayerRegisterHandler) -> None:
        self.setup_handler(handler.ask_username, RootState.ON_HOLD, F.text.casefold() == BUTTON_ADD_GAMER.text.lower())
        self.setup_handler(handler.handle_username, NewPlayerRegisterState.WAIT_USERNAME)


def create_new_player_register_router(bot: TGBot,
                                     player_data_service: PlayerDataService) -> NewPlayerRegisterRouter:
    handler = NewPlayerRegisterHandler(bot, player_data_service)
    return NewPlayerRegisterRouter(handler)
