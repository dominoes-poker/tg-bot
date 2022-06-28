
from typing import List

from bot.bot import DPBot
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.statistics_service import RoundStatiticsService, StatisticsPresentService
from bot.types import IncommingMessage, Player, Round
from bot.states import RoundState
from bot.routers.common.keyboards import keyboard_start_new_round


class RoundStatisticsHandler(Handler):
    def __init__(self, bot: DPBot,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def show_statistics(self, message: IncommingMessage,
                              context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)

        statistics = self._get_round_statistics(game.last_round, game.players)

        text = f'The Round Statistics:\n\n{statistics}'
        await self.bot.send(
            chat_id=message.user_id,
            text=text,
            reply_markup=keyboard_start_new_round(game.last_round.number + 1)
        )
        return RoundState.START

    @staticmethod
    def _get_round_statistics(round_: Round, players: List[Player]) -> str:
        statistics = RoundStatiticsService(players).total(round_)
        return StatisticsPresentService.present(statistics)
