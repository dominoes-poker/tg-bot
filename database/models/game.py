from database.models.base import BaseModel
from sqlalchemy import Column, Integer,Boolean, ForeignKey, orm

class GamePlayer(BaseModel):
    __tablename__ = 'games_players'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    player_id = Column(Integer, ForeignKey('players.id'))


class Game(BaseModel):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True, autoincrement=True)
    is_over = Column(Boolean, default=False, nullable=False)

    players = orm.relationship(
        'Player', lazy='subquery', secondary='games_players', uselist=True
    )

    rounds = orm.relationship(
        'Round', lazy='subquery', uselist=True
    )

