
from typing import List
from bot.bot import TGBot

from bot.routers.handler import Handler
from bot.routers.utils import get_number_of_dices
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.types import Game, IncommingMessage, Round
from bot.routers.game.round.bets import BetsHandler
from bot.routers.game.round.bribes import BribesHandler

class RoundHandler(Handler):
    def __init__(self, bot: TGBot,
                 make_bets_handler: BetsHandler,
                 set_bribes_handler: BribesHandler,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service
        self._make_bets_handler = make_bets_handler
        self._set_bribes_handler = set_bribes_handler

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
        return await self._make_bets_handler.ask_who_make_bet(message, context_service)

    async def finish_round(self, message: IncommingMessage, context_service: ContextService) -> None:
        return await self._set_bribes_handler.ask_results(message, context_service)
