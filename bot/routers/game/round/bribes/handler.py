
from typing import List, Optional

from aiogram.dispatcher.fsm.state import State
from bot.bot import DPBot
from bot.routers.common.keyboards import (KEYBOARD_GAME_OVER,
                                          keyboard_after_round,
                                          keyboard_from_data)
from bot.routers.handler import Handler
from bot.routers.utils import get_number_of_dices
from bot.services.context_service import ContextService
from services.game_service import GameDataService
from bot.states import RootState, RoundState, SetBribesState
from bot.data_types import Game, IncomingMessage, Player, Stake


class BribesHandler(Handler):
    def __init__(self, bot: DPBot, game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def ask_player_bribes(self, message: IncomingMessage,
                                context_service: ContextService) -> State:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        player = self._get_player_to_ask_results(game)

        if not player:
            return await self._finish(message.user_id, game)

        remaining_bribes = self._get_bribes_variants(game)
        if not remaining_bribes:
            return await self._early_finish(game, message.user_id)

        await context_service.wait_bribe_of(player)
        await self._bot.send(
            chat_id=message.user_id,
            text=f'How many bribes did `{player.username}` take in the round?',
            reply_markup=keyboard_from_data(remaining_bribes)
        )
        return SetBribesState.BRIBE

    async def handle_bribe(self, message: IncomingMessage,
                           context_service: ContextService) -> State:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        username = await context_service.from_whom_expect_bribe()
        player = next(filter(lambda p: p.username == username, game.players))

        await self._set_bribe(player.id, int(message.text), game)

        return await self.ask_player_bribes(message, context_service)

    async def _early_finish(self, game: Game, user_id: int) -> State:
        stakes = game.last_round.stakes
        players = {player.id: player.username for player in game.players}

        losers = {
            stake.player_id: players[stake.player_id]
            for stake in stakes if stake.bribe is None
        }

        for loser in losers:
            await self._set_bribe(loser, 0, game)

        losers = '`, `'.join(losers.values())

        await self._bot.send(
                chat_id=user_id,
                text=f'Looks like `{losers}` did not get anything in this round.'
        )
        return await self._finish(user_id, game)

    async def _finish(self, user_id: int, game: Game) -> State:
        next_round_number = game.last_round.number + 1
        if next_round_number < 17:
            await self._bot.send(
                    chat_id=user_id,
                    text='The round has finished',
                    reply_markup=keyboard_after_round(next_round_number)
            )
            return RoundState.ON_HOLD
        await self._bot.send(
                    chat_id=user_id,
                    text='The game is over',
                    reply_markup=KEYBOARD_GAME_OVER
            )
        return RootState.ON_HOLD

    async def _set_bribe(self, player_id: int, bribe: int, game: Game) -> Game:
        stake = Stake(
            player_id=player_id,
            bribe=bribe,
            round_id=game.last_round.id,
        )
        return await self._game_data_service.set_bribe(game.id, stake)

    @staticmethod
    def _get_bribes_variants(game: Game) -> Optional[List[int]]:
        stakes = sorted(game.last_round.stakes, key=lambda stake: stake.id)
        taken = sum(stake.bribe for stake in stakes if stake.bribe is not None)

        remaining_bribes = get_number_of_dices(game, game.last_round.number) - taken

        if remaining_bribes == 0:
            return None

        return list(range(remaining_bribes + 1))

    @staticmethod
    def _get_player_to_ask_results(game: Game) -> Optional[Player]:
        stakes = sorted(game.last_round.stakes, key=lambda stake: stake.id)
        players_ask_results = {stake.player_id for stake in stakes if stake.bribe is None}

        for player in game.players:
            if player.id in players_ask_results:
                return player
        return None
        