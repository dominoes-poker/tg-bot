from typing import Any, List, Type, Union

from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from bot.data_types import Game, Player, Round, Stake

from database.models import Game as DBGame
from database.models import Round as DBRound
from database.models import Stake as DBStake
from database.models import Player as DBPlayer
from database.session import SessionManager

from services.database_mixin import DatabaseMixin
from services.game_service.game_data_service import GameDataService
from services.player_service.database_player_data_service import PlayerSerializer
from services.serializer import Serializer


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


class DataBaseGameDataService(GameDataService, DatabaseMixin):
    def __init__(self, session_manager: SessionManager, serializer: GameSerializer) -> None:
        GameDataService.__init__(self, serializer)
        DatabaseMixin.__init__(self, session_manager)

    async def create(self, players: List[Player]) -> Game:
        db_game = DBGame()
        async with self._session_manager.session() as session:
            db_players = []
            for player in players:
                query = select(DBPlayer).where(DBPlayer.id==player.id)
                db_players.append(await self._first_raw(query))
            db_game.players = db_players
            async with session.begin():
                session.add_all([
                    db_game
                ])
                await session.commit()
        query = select(DBGame).where(DBGame.id == db_game.id).options(
            selectinload(DBGame.rounds)
        )
        return await self.first(query)

    async def get_game(self, game_id: int) -> Game:
        query = select(DBGame).where(DBGame.id == game_id).options(
            selectinload(DBGame.rounds)
        )
        return await self.first(query)

    async def start_new_round(self, round_: Round) -> Game:
        db_round: DBRound = self._serializer.round_serializer.serialize(round_)
        async with self._session_manager.session() as session:
            async with session.begin():
                session.add_all([
                    db_round
                ])
                await session.commit()
        return await self.get_game(db_round.game_id)
    
    async def set_bet(self, game_id: int, stake: Stake) -> Game:
        db_stake: DBStake = self._serializer.round_serializer._stake_serializer.serialize(stake)
        async with self._session_manager.session() as session:
            async with session.begin():
                session.add_all([db_stake])
        return await self.get_game(game_id)

    async def set_bribe(self, game_id: int, stake: Stake) -> Game:
        query = select(DBStake).where(
            and_(
                DBStake.round_id == stake.round_id,
                DBStake.player_id == stake.player_id, 
                )
            )
        db_stake: DBStake = await self._first_raw(query)
        if not db_stake:
            raise ValueError()

        db_stake.bribe = stake.bribe

        async with self._session_manager.session() as session:
            async with session.begin():
                session.add_all([
                    db_stake
                ])
            session.commit()
        return await self.get_game(game_id)

    async def finish(self, game_id: int) -> Game:
        query = select(DBGame).where(DBGame.game_id == game_id)
        return await self.first(query)
