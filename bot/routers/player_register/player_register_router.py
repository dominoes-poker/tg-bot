from aiogram import F
from bot.bot import TGBot
from bot.routers.handlers.common.keyboards import BUTTON_NO
from bot.routers.player_register.handlers import PlayerRegisterHandler
from bot.routers.player_register.new_player_register_router import NewPlayerRegisterRouter, create_new_player_register_router
from bot.routers.player_register.tg_player_register_router import TGPlayerRegisterRouter, create_tg_player_register_router
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService
from bot.states import RootState


class PlayerRegisterRouter(TGRouter):
    def __init__(self, 
                root_player_register_handler: PlayerRegisterHandler,
                tg_player_register_router: TGPlayerRegisterRouter,
                new_player_register_router: NewPlayerRegisterRouter) -> None:
        super().__init__(use_builtin_filters=True, name='PlayerRegisterRouter')
        self.setup(root_player_register_handler, tg_player_register_router=tg_player_register_router, 
                   new_player_register_router=new_player_register_router)

    def setup(self, 
                root_player_register_handler: PlayerRegisterHandler,
                tg_player_register_router: TGPlayerRegisterRouter,
                new_player_register_router: NewPlayerRegisterRouter) -> None:
        self.include_router(tg_player_register_router)
        self.include_router(new_player_register_router)
        self.message.register(self.handler(root_player_register_handler.decline_registration), 
                              RootState.TG_PLAYER_REGISTRATION, F.text.casefold() == BUTTON_NO.text.lower())
        

def create_player_register_router(bot: TGBot,
                                  player_data_service: PlayerDataService) -> PlayerRegisterRouter:
    tg_player_register_router = create_tg_player_register_router(bot, player_data_service)
    new_player_register_router = create_new_player_register_router(bot, player_data_service)
    player_register_handler = PlayerRegisterHandler(bot, player_data_service)
    return PlayerRegisterRouter(player_register_handler, tg_player_register_router, new_player_register_router)
