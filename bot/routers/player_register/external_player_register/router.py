from aiogram import F
from bot.bot import DPBot
from bot.routers.common.keyboards import BUTTON_ADD_GAMER
from bot.routers.router import DPRouter
from bot.services.player_service import PlayerDataService
from bot.states import RootState, ExternalPlayerRegisterState
from bot.routers.player_register.external_player_register.handler import ExternalPlayerRegisterHandler 


def setup_router(router: DPRouter, handler: ExternalPlayerRegisterHandler) -> None:
    ask_username_filters = [
        RootState.ON_HOLD,
        F.text.casefold() == BUTTON_ADD_GAMER.text.lower()
    ]
    router.setup_handler(handler.ask_username, *ask_username_filters)

    handle_username_filters = [ExternalPlayerRegisterState.WAIT_USERNAME]
    router.setup_handler(handler.handle_username, *handle_username_filters)


def create_external_player_register_router(bot: DPBot,
                                           player_data_service: PlayerDataService) -> DPRouter:
    router = DPRouter(name='<ExternalPlayerRegister> - Router')

    handler = ExternalPlayerRegisterHandler(bot, player_data_service)
    setup_router(router, handler)
    
    return router
