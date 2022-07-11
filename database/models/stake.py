from typing import Optional
from sqlalchemy import Column, ForeignKey, Integer

from database.models.base import BaseModel
from database.models.player import Player


class Stake(BaseModel):
    __tablename__ = 'stakes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey(Player.id))
    round_id = Column(Integer, ForeignKey('rounds.id'))
    
    bet = Column(Integer, nullable=True)
    bribe = Column(Integer, nullable=True)

    def __init__(self, round_id: int, player_id: int, bet: int, bribe: Optional[int] = None) -> None:
        self.round_id = round_id
        self.player_id = player_id
        self.bet = bet
        self.bribe = bribe
