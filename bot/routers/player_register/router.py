from bot.bot import DPBot
from bot.routers.player_register.telegram_player_register import (
        create_telegram_player_register_router
    )
from bot.routers.player_register.external_player_register import (
        create_external_player_register_router
    )
from bot.routers.router import DPRouter
from bot.services.player_service import PlayerDataService



def create_player_register_router(bot: DPBot,
                                  player_data_service: PlayerDataService) -> DPRouter:
    router = DPRouter(name='<RootPlayerRegister> - Router')

    tg_player_register_router = create_telegram_player_register_router(bot, player_data_service)
    router.include_router(tg_player_register_router)

    new_player_register_router = create_external_player_register_router(bot, player_data_service)
    router.include_router(new_player_register_router)

    return router
