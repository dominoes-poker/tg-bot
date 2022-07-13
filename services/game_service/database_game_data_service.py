from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import selectinload

from bot.data_types import Game, Player, Round, Stake

from database.models import Game as DBGame, Round as DBRound, Stake as DBStake, Player as DBPlayer
from database.session import SessionManager

from services.database_mixin import DatabaseMixin
from services.game_service.game_data_service import GameDataService
from services.serializers import GameSerializer


class DataBaseGameDataService(GameDataService, DatabaseMixin):
    def __init__(self, session_manager: SessionManager, serializer: GameSerializer) -> None:
        GameDataService.__init__(self, serializer)
        DatabaseMixin.__init__(self, session_manager)

    async def create(self, players: List[Player]) -> Game:
        db_game = DBGame()
        async with self._session_manager.session() as session:
            db_players = []
            for player in players:
                query = select(DBPlayer).where(DBPlayer.id == player.id)
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
