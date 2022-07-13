from typing import List

from sqlalchemy.orm import declarative_base, Session


class BaseModel(declarative_base()):
    __abstract__ = True

    async def write_record(self, session: Session):
        session.add(self)
        session.commit()

    @staticmethod
    async def write_records(records: List['BaseModel'], session: Session):
        session.add_all(records)
        session.commit()

    async def delete_record(self, session: Session):
        session.delete(self)
        session.commit()

    @staticmethod
    async def delete_records(records: List['BaseModel'], session: Session):
        for i in records:
            session.delete(i)
        session.commit()
