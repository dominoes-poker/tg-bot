
from typing import List, Optional
from bot.bot import TGBot

from bot.routers.handlers.common.keyboards import SHOW_STATISTICS_KEYBOARD, keyboard_from_data
from bot.routers.handlers.handler import Handler
from bot.routers.utils import get_number_of_dices
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.types import Game, IncommingMessage, Player
from bot.states import SetBribesState


class SetBribesHandler(Handler):
    def __init__(self, bot: TGBot,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def ask_results(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        player = self._get_player_to_ask_results(game)
        
        if not player:
            return await self._finish(message, context_service)

        await context_service.wait_bribe_of(player)
        await self._bot.send(
            chat_id=message.user_id,
            text=f'How many did `{player.username}` get in the round?',
            reply_markup=keyboard_from_data(self._get_results_variants(game))
        )
        await context_service.set_state(SetBribesState.BRIBE)

    async def handle_result(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        
        username = await context_service.from_whom_expect_bribe()
        player = next(filter(lambda p: p.username == username, game.players))

        stake = dict(
            playerId=player.id,
            bribe = int(message.text),
            roundId=game.last_round.number,
        )
        game = await self._game_data_service.set_bribe(game_id, stake)
        
        return await self.ask_results(message, context_service)

    async def _finish(self, message: IncommingMessage, context_service: ContextService) -> None:
        return await self._bot.send(
                chat_id=message.user_id,
                text=f'The round has finished',
                reply_markup=SHOW_STATISTICS_KEYBOARD
        )

    def _get_results_variants(self, game: Game) -> List[int]:
        stakes = sorted(game.last_round.stakes, key=lambda stake: stake.id)
        variants = list(range(get_number_of_dices(game, game.last_round.number)))
        for stake in stakes:
            if stake.bribe is not None:
                variants.remove(stake.bribe)
        return variants
        

    def _get_player_to_ask_results(self, game: Game) -> Optional[Player]:
        if not game.rounds or not game.last_round.stakes:
            return [player.username for player in game.players]
        stakes = sorted(game.last_round.stakes, key=lambda stake: stake.id, reverse=True)
        players_ask_results = {stake.playerId for stake in stakes if stake.bribe is None}
        
        for player in game.players:
            if player.id in players_ask_results:
                return player
        return None
        
        