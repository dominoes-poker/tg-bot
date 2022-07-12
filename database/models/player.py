from typing import Union, Optional

from database.models.base import BaseModel
from sqlalchemy import Column, Index, Integer, String, UniqueConstraint, orm


class Player(BaseModel):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    identificator = Column(String, nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint('username', name='_username'),
        Index(
            'uix_identificator', 
            'identificator',
            unique=True, 
            postgresql_where=identificator.isnot(None)
        ),
    )

    def __init__(self, username: str, identificator: Optional[str]) -> None:
        self.username = username
        self.identificator = identificator
    
