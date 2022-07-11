from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from common.singleton_metaclass import SingletonMetaClass


class SessionManager(metaclass=SingletonMetaClass):
    def __init__(self, db_url: str) -> None:
        self._db_url = db_url
        self._engine = self._create_engine(self._db_url)

    async def create_all(self, meta: MetaData):
        async with self._engine.begin() as connection:
            await connection.run_sync(meta.drop_all)
            await connection.run_sync(meta.create_all)
    
    @staticmethod
    def _create_engine(db_url):
        return create_async_engine(
            f'postgresql+asyncpg://{db_url}',
            echo=True,
        )

    @property
    def session(self) -> sessionmaker:
        return sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )
