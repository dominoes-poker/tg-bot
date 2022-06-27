from aiogram import F

from bot.bot import DPBot
from bot.routers.router import DPRouter
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import SetBribesState
from bot.routers.game.round.bribes.handler import BribesHandler


def setup_router(router: DPRouter, handler: BribesHandler) -> None:
    bribes_filters = [
        SetBribesState.BRIBE,
        F.text.regexp(r'\d+')
    ]
    router.setup_handler(handler.handle_bribe, *bribes_filters)


def create_bribes_router(bot: DPBot,
                            game_data_service: GameDataService) -> DPRouter:
    router = DPRouter(name='<Bribes> - Router')

    handler = BribesHandler(bot, game_data_service)
    setup_router(router, handler)

    return router, handler
