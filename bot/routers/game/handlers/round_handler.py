
from typing import List
from bot.bot import TGBot
from bot.routers.game.handlers.make_bets_handler import MakeBetsHandler

from bot.routers.handlers.handler import Handler
from bot.routers.utils import get_number_of_dices
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.types import Game, IncommingMessage, Round


class RoundHandler(Handler):
    def __init__(self, bot: TGBot, 
                 player_data_service: PlayerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._game_data_service = game_data_service

    def _get_next_round_number(self, game: Game) -> int:
        if game.rounds:
            next(
                sorted(
                    game.rounds, 
                    key=lambda round: round.number
                    )
                ) + 1
        return 0

    async def start_round(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        
        next_round = self._get_next_round_number(game)
        new_round = Round(
            gameId=game_id,
            numberOfDice=get_number_of_dices(game, next_round),
        )
        await self._game_data_service.start_new_round(new_round)
        return await MakeBetsHandler(self._bot, self._player_data_service, self._game_data_service).ask_who_make_bet(message, context_service)
