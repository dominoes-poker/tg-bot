from aiogram import F

from bot.bot import DPBot
from bot.routers.common.keyboards import BUTTON_NEW_GAME
from bot.routers.game.create_game.handler import CreateGameHandler
from bot.routers.router import DPRouter
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import GameState, RootState


def setup_router(router: DPRouter, handler: CreateGameHandler) -> None:
    wait_player_usernames = [RootState.ON_HOLD, F.text == BUTTON_NEW_GAME.text]
    router.setup_handler(handler.ask_player_usernames, *wait_player_usernames)

    player_usernames = [GameState.WAIT_PLAYER_USERNAMES]
    router.setup_handler(handler.handle_player_usernames, *player_usernames)

def create_start_game_router(bot: DPBot,
                            player_data_service: PlayerDataService,
                            game_data_service: GameDataService) -> DPRouter:
    router = DPRouter(name='<CreateGame> - Router')

    handler = CreateGameHandler(bot, player_data_service, game_data_service)
    setup_router(router, handler)

    return router
