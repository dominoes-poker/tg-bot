from bot.bot import TGBot
from bot.routers.player_register.telegram_player_register import (
        create_telegram_player_register_router
    )
from bot.routers.player_register.external_player_register import (
        create_external_player_register_router
    )
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService



def create_player_register_router(bot: TGBot,
                                  player_data_service: PlayerDataService) -> TGRouter:
    router = TGRouter(name='<RootPlayerRegister> - Router')

    tg_player_register_router = create_telegram_player_register_router(bot, player_data_service)
    router.include_router(tg_player_register_router)

    new_player_register_router = create_external_player_register_router(bot, player_data_service)
    router.include_router(new_player_register_router)

    return router
