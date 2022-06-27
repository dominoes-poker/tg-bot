
from bot.bot import DPBot
from bot.routers.game.round.bets import BetsHandler
from bot.routers.game.round.bribes import BribesHandler
from bot.routers.handler import Handler
from bot.routers.utils import get_number_of_dices
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.types import Game, IncommingMessage, Round


class RoundHandler(Handler):
    def __init__(self, bot: DPBot,
                 bets_handler: BetsHandler,
                 bribes_handler: BribesHandler,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service
        self._bets_handler = bets_handler
        self._bribes_handler = bribes_handler

    def _get_next_round_number(self, game: Game) -> int:
        if game.rounds:
            return list(
                sorted(
                    game.rounds, 
                    key=lambda round: round.number
                    )
                )[0].number + 1
        return 1

    async def start_round(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        
        next_round = self._get_next_round_number(game)
        new_round = Round(
            gameId=game_id,
            numberOfDice=get_number_of_dices(game, next_round),
        )
        await self._game_data_service.start_new_round(new_round)
        return await self._bets_handler.ask_who_make_bet(message, context_service)

    async def finish_round(self, message: IncommingMessage, context_service: ContextService) -> None:
        return await self._bribes_handler.ask_player_bribes(message, context_service)
