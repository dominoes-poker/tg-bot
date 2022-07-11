from database.models.base import BaseModel
from database.models.stake import Stake
from sqlalchemy import Column, ForeignKey, Integer, orm


class Round(BaseModel):
    __tablename__ = 'rounds'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    
    number = Column(Integer, nullable=False)
    number_of_dominoes = Column(Integer, nullable=False)

    stakes = orm.relationship(
        Stake, uselist=True, lazy='subquery'
    )

    def __init__(self, game_id: int, number: int, number_of_dominoes: int) -> None:
        self.game_id = game_id
        self.number = number
        self.number_of_dominoes = number_of_dominoes
