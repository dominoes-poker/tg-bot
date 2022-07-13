from typing import Optional

from bot.data_types import Stake, Player, Round, Game
from database.models import Game as DBGame, Round as DBRound, Stake as DBStake, Player as DBPlayer, BaseModel
from typing import TypeVar


TypeFrom = TypeVar('TypeFrom')


class Serializer:
    @staticmethod
    def serialize(data: TypeFrom) -> BaseModel:
        raise NotImplementedError

    @staticmethod
    def deserialize(data: BaseModel) -> TypeFrom:
        raise NotImplementedError


class PlayerSerializer(Serializer):
    def serialize(self, player: Player) -> DBPlayer:
        return DBPlayer(
            username=player.username,
            identificator=player.identificator
        )

    def deserialize(self, player: DBPlayer) -> Optional[Player]:
        if not player:
            return None
        return Player(
            id=player.id,
            username=player.username,
            identificator=player.identificator
        )


class StakeSerializer(Serializer):

    def serialize(self, stake: Stake) -> DBStake:
        return DBStake(
            round_id=stake.round_id,
            player_id=stake.player_id,
            bet=stake.bet,
            bribe=stake.bribe
        )

    def deserialize(self, stake: DBStake) -> Stake:
        return Stake(
            id=stake.id,
            round_id=stake.round_id,
            player_id=stake.player_id,
            bet=stake.bet,
            bribe=stake.bribe
        )


class RoundSerializer(Serializer):
    def __init__(self, stake_serializer: StakeSerializer) -> None:
        super().__init__()
        self._stake_serializer = stake_serializer

    def serialize(self, round_: Round) -> DBRound:
        return DBRound(
            game_id=round_.game_id,
            number=round_.number,
            number_of_dominoes=round_.number_of_dominoes,
        )

    def deserialize(self, round_: DBRound) -> Round:
        return Round(
            id=round_.id,
            game_id=round_.game_id,
            number=round_.number,
            number_of_dominoes=round_.number_of_dominoes,
            stakes=[self._stake_serializer.deserialize(stake) for stake in round_.stakes] if round_.stakes else []
        )


class GameSerializer(Serializer):
    def __init__(self, player_serializer: PlayerSerializer, round_serializer: RoundSerializer) -> None:
        super().__init__()
        self._player_serializer = player_serializer
        self._round_serializer = round_serializer

    @property
    def player_serializer(self) -> PlayerSerializer:
        return self._player_serializer

    @property
    def round_serializer(self) -> RoundSerializer:
        return self._round_serializer

    def serialize(self, game: Game) -> DBGame:
        result = DBGame(
            players=[self._player_serializer.serialize(player) for player in game.players] if game.players else [],
            rounds=[self._round_serializer.serialize(round) for round in game.rounds] if game.rounds else []
        )
        if game.id is not None:
            result.id = game.id
        return result

    def deserialize(self, game: DBGame) -> Game:
        result = Game(
            players=[self._player_serializer.deserialize(player) for player in game.players],
            rounds=[self._round_serializer.deserialize(round_) for round_ in game.rounds],
            is_over=game.is_over
        )
        if game.id is not None:
            result.id = game.id
        return result
