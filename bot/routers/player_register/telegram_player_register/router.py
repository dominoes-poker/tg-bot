from aiogram import F
from bot.bot import TGBot
from bot.routers.common.keyboards import BUTTON_NO, BUTTON_YES
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService
from bot.states import RootState, TelegramPlayerRegisterState
from bot.routers.player_register.telegram_player_register.handler import (
        TelegramPlayerRegisterHandler
    )


def setup_router(router: TGRouter, handler: TelegramPlayerRegisterHandler) -> None:
    start_registration_filters = [
        RootState.TG_PLAYER_REGISTRATION, 
        F.text.casefold() == BUTTON_YES.text.lower()
    ]
    router.setup_handler(handler.new_player, *start_registration_filters)

    decline_registration_filters = [
        RootState.TG_PLAYER_REGISTRATION, 
        F.text.casefold() == BUTTON_NO.text.lower()
    ]
    router.setup_handler(handler.decline_registration, *decline_registration_filters)

    agree_tg_username_filters = [
        TelegramPlayerRegisterState.WHAT_USERNAME_USE, 
        F.text.casefold() == BUTTON_YES.text.lower()
    ]
    router.setup_handler(handler.use_tg_username, *agree_tg_username_filters)

    disagree_tg_username_filters = [
        TelegramPlayerRegisterState.WHAT_USERNAME_USE, 
        F.text.casefold() == BUTTON_NO.text.lower()
    ]
    router.setup_handler(handler.ask_new_username, *disagree_tg_username_filters)

    new_username_filters = [
        TelegramPlayerRegisterState.WAIT_USERNAME,
    ]
    router.setup_handler(handler.use_new_username, *new_username_filters)


def create_telegram_player_register_router(bot: TGBot,
                                           player_data_service: PlayerDataService) -> TGRouter:
    handler = TelegramPlayerRegisterHandler(bot, player_data_service)

    router = TGRouter(name='<TGPlayerRegister> - Router')

    setup_router(router, handler)

    return router
