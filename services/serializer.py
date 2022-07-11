from typing import TypeVar


TypeFrom = TypeVar('TypeFrom')
TypeTo = TypeVar('TypeTo')


class Serializer:
    @staticmethod
    def serialize(data: TypeFrom) -> TypeTo:
        raise NotImplementedError

    @staticmethod
    def deserialize(data: TypeTo) -> TypeFrom:
        raise NotImplementedError
