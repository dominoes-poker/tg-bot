from aiogram import F

from bot.bot import TGBot
from bot.routers.router import TGRouter
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import SetBribesState
from bot.routers.game.round.bribes.handler import BribesHandler


def setup_router(router: TGRouter, handler: BribesHandler) -> None:
    bribes_filters = [
        SetBribesState.BRIBE,
        F.text.regexp(r'\d+')
    ]
    router.setup_handler(handler.handle_result, *bribes_filters)


def create_bribes_router(bot: TGBot,
                            game_data_service: GameDataService) -> TGRouter:
    router = TGRouter(name='<Bribes> - Router')

    handler = BribesHandler(bot, game_data_service)
    setup_router(router, handler)

    return router, handler
