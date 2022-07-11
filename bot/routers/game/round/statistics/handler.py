
from typing import List

from bot.bot import DPBot
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from services.game_service import GameDataService
from bot.services.statistics_service import (GameStatiticsService,
                                             RoundStatiticsService,
                                             StatisticsPresentService)
from bot.data_types import Game, IncomingMessage, Player, Round


class StatisticsHandler(Handler):
    def __init__(self, bot: DPBot,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def show_round_statistics(self, message: IncomingMessage,
                                    context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        statistics = self._get_round_statistics(game.last_round, game.players)

        text = f'The Round Statistics:\n\n{statistics}'
        await self.bot.send(
            chat_id=message.user_id,
            text=text
        )

    async def show_game_statistics(self, message: IncomingMessage,
                                   context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        statistics = self._get_game_statistics(game)

        text = f'The Game Statistics:\n\n{statistics}'
        await self.bot.send(
            chat_id=message.user_id,
            text=text,
        )

    @staticmethod
    def _get_round_statistics(round_: Round, players: List[Player]) -> str:
        statistics = RoundStatiticsService(players).total(round_)
        return StatisticsPresentService.present(statistics)

    @staticmethod
    def _get_game_statistics(game: Game) -> str:
        statistics = GameStatiticsService(game.players).total(game)
        return StatisticsPresentService.present(statistics)
