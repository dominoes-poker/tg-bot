
from typing import List

from bot.bot import DPBot
from bot.routers.common.keyboards import (KEYBOARD_ENTER_ROUND_RESULTS,
                                          keyboard_from_data)
from bot.routers.handler import Handler
from bot.routers.utils import get_number_of_dices
from bot.services.context_service import ContextService
from services.game_service import GameDataService
from bot.states import MakeBetsState, RoundState
from bot.data_types import Game, IncomingMessage, Stake


class BetsHandler(Handler):
    def __init__(self, bot: DPBot,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def ask_who_make_bet(self, message: IncomingMessage,
                               context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        next_players = self._get_players_to_bet(game)

        await self._bot.send(
            chat_id=message.user_id,
            text='Who will make a bet?',
            reply_markup=keyboard_from_data(next_players)
        )
        return MakeBetsState.USERNAME

    async def handle_username(self, message: IncomingMessage,
                              context_service: ContextService) -> None:

        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        username = message.text
        player = next(filter(lambda player: player.username==username, game.players))
        await context_service.wait_bet_of(player)

        await self._bot.send(
            chat_id=message.user_id,
            text=f'Who many does `{username}` bet?',
            reply_markup=keyboard_from_data(self._get_variants_to_bet(game))
        )
        return MakeBetsState.BET

    async def handle_bet(self, message: IncomingMessage,
                         context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        username = await context_service.from_whom_expect_bet()
        player = next(filter(lambda p: p.username == username, game.players))

        stake = Stake(
            player_id=player.id,
            bet=int(message.text),
            round_id=game.last_round.id,
        )
        game = await self._game_data_service.set_bet(game_id, stake)
        if len(game.last_round.stakes) < len(game.players):
            return await self.ask_who_make_bet(message, context_service)

        await self._bot.send(
            chat_id=message.user_id,
            text='Everyone made a bet, now - play',
            reply_markup=KEYBOARD_ENTER_ROUND_RESULTS
        )
        return RoundState.BRIBES

    @staticmethod
    def _get_variants_to_bet(game: Game) -> List[int]:
        last_round = game.last_round
        number_of_dices = get_number_of_dices(game, last_round.number) if last_round else 1
        return list(range(number_of_dices + 1))

    @staticmethod
    def _get_players_to_bet(game: Game) -> List[str]:
        if not game.rounds or not game.last_round.stakes:
            return [player.username for player in game.players]
        players_made_bets = {stake.player_id for stake in game.last_round.stakes}
        return [
            player.username
            for player in game.players
            if player.id not in players_made_bets
        ]
