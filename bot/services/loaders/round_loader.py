from typing import Dict, Any

from bot.services.loaders.loader import Loader
from bot.types import Round


class RoundLoader(Loader):
    
    def __call__(self, data: Dict[Any, Any]) -> Round:
        return Round(
            id=data['id']
        )