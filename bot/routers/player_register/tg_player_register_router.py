from aiogram import F
from bot.bot import TGBot
from bot.routers.handlers.common.keyboards import BUTTON_YES, BUTTON_NO
from bot.routers.player_register.handlers import TGPlayerRegisterHandler
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService
from bot.states import TGPlayerRegisterState, RootState


class TGPlayerRegisterRouter(TGRouter):
    def __init__(self, handler: TGPlayerRegisterHandler) -> None:
        super().__init__(use_builtin_filters=True, name='TGPlayerRegisterRouter')
        self.setup(handler=handler)

    def setup(self, handler: TGPlayerRegisterHandler) -> None:
        self.setup_handler(handler.new_player, RootState.TG_PLAYER_REGISTRATION, F.text.casefold() == BUTTON_YES.text.lower())
        self.setup_handler(handler.use_tg_username, TGPlayerRegisterState.WHAT_USERNAME_USE, F.text.casefold() == BUTTON_YES.text.lower())
        self.setup_handler(handler.ask_new_username, TGPlayerRegisterState.WHAT_USERNAME_USE, F.text.casefold() == BUTTON_NO.text.lower())
        self.setup_handler(handler.use_new_username, TGPlayerRegisterState.WAIT_USERNAME)


def create_tg_player_register_router(bot: TGBot,
                                     player_data_service: PlayerDataService) -> TGPlayerRegisterRouter:
    handler = TGPlayerRegisterHandler(bot, player_data_service)
    return TGPlayerRegisterRouter(handler)
