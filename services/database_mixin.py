from typing import Any, Dict, List, Optional

from database.session import SessionManager

from sqlalchemy.sql.selectable import Select


class DatabaseMixin:
    def __init__(self, session_manager: SessionManager) -> None:
        self._session_manager = session_manager

    async def all(self, query) -> List[Optional[Any]]:
        async with self._session_manager.session() as session:
            result = await session.execute(query)
            scalars = result.scalars().all()
            if not scalars:
                return []
            return [self._serializer.deserialize(scalar) for scalar in scalars]

    async def _first_raw(self, query) -> Optional[Any]:
        async with self._session_manager.session() as session:
            result = await session.execute(query)
            return result.scalars().first()

    async def first(self, query: Select) -> Optional[Any]:
        result = await self._first_raw(query)
        return self._serializer.deserialize(result)
