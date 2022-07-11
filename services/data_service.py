from common import SingletonMetaClass
from services.serializer import Serializer


class DataService(metaclass=SingletonMetaClass):
    def __init__(self, serializer: Serializer) -> None:
        self._serializer = serializer
