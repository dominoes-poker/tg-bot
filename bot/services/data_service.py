from common import SingletonMetaClass
from bot.services.loaders.loader import Loader


class DataService(metaclass=SingletonMetaClass):
    def __init__(self, loader: Loader) -> None:
        self._loader = loader
