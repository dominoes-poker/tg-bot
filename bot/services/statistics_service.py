from typing import Iterable, Tuple, List, Union
from bot.types import Game
from bot.types.data_types import Player, Round


class Statistics:
    def __init__(self, players: Iterable[Player]) -> None:
        self._players ={player.id: player for player in players}
        self._statistics = {player.id: 0 for player in players}

    def update_from_round(self, round_: Round) -> 'Statistics':
        for stake in round_.stakes:
            self._statistics[stake.playerId] = self._infer(stake.bet, stake.bribe)
        return self

    @staticmethod
    def _infer(bet: int, bribe: int) -> int:
        if bet == bribe:
            return 10 * bet
        return -10 * (bet - bribe) if bet > bribe else bribe

    def sorted(self, names: bool = True) -> List[Tuple[Union[str, int], int]]:
        sorted_players = sorted(
            self._statistics.keys(),
            key=lambda player_id: self._statistics[player_id]
        )
        result = []
        for player_id in sorted_players:
            player = self._players[player_id] if names else player_id
            result.append(tuple((player.username, self._statistics[player_id])))
        return result


class RoundStatiticsService:
    def __init__(self, players: Iterable[Player]) -> None:
        self._statistics = Statistics(players)

    def total(self, round_: Round) -> Statistics:
        return self._statistics.update_from_round(round_)

class GameStatiticsService:
    def __init__(self, players: Iterable[Player]) -> None:
        self._statistics = Statistics(players)

    def total(self, game: Game) -> Statistics:
        for round_ in game.rounds:
            self._statistics.update_from_round(round_)
        return self._statistics

class StatisticsPresentService:
    @staticmethod
    def present(statistics: Statistics) -> str:
        result_string = ''
        for player, result in statistics.sorted():
            result_string += f'`{player}`:\t{result}\n'
        return result_string
