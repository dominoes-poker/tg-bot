
from typing import Dict, List

from bot.bot import TGBot
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.types import Game, IncommingMessage, Player, Round, Stake


class RoundStatisticsHandler(Handler):
    def __init__(self, bot: TGBot,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._game_data_service = game_data_service

    async def show_statistics(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        
        statistics = self._get_round_statistics(game.last_round, game.players)
        strings_statistics = "\n".join(f'`{player}` : {result}' for player, result in statistics.items())
        
        text = f"The Round Statistics:\n{strings_statistics}"
        await self.bot.send(
            chat_id=message.user_id,
            text=text
        )

    @staticmethod
    def _get_round_statistics(round: Round, players: List[Player]) -> Dict[str, int]:
        player_id_to_username = {player.id: player.username for player in players}
        results = {}
        for stake in round.stakes:
            username = player_id_to_username[stake.playerId]
            results[username] = RoundStatisticsHandler._get_result(stake)
        return results
    
    @staticmethod
    def _get_result(stake: Stake) -> int:
        if stake.bet > stake.bribe:
            return -10 * (stake.bribe - stake.bet)
        if stake.bet < stake.bribe:
            return stake.bribe
        return 10 * stake.bet
