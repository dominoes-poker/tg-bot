
from bot.bot import TGBot

from bot.routers.handlers.common.keyboards import keyboard_from_data
from bot.routers.handlers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.types import IncommingMessage, Round


class RoundHandler(Handler):
    def __init__(self, bot: TGBot, 
                 player_data_service: PlayerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._game_data_service = game_data_service

    async def start_round(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        new_round = Round(
            gameId=game_id,
            numberOfDice=1,
        )
        game = await self._game_data_service.start_new_round(new_round)
        await self._bot.send(
            chat_id=message.user_id,
            text=f'Who will make a bet?',
            reply_markup=keyboard_from_data([player.username for player in game['players']])
        )
