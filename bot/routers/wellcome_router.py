from aiogram import Router
from bot.handlers import Handler, WellcomeHandler
from bot.services.gamer_data_service import GamerDataService


class WellcomeRouter(Router):
    def __init__(self, handler: Handler) -> None:
        super().__init__(use_builtin_filters=True, name='WellcomeRouter')
        self.setup(handler=handler)
        
    def setup(self, handler: Handler) -> None:
        self.message.register(handler.handle, commands=['start'])

def create_wellcome_router(gamer_data_service: GamerDataService) -> WellcomeRouter:
    handler = WellcomeHandler(gamer_data_service)
    return WellcomeRouter(handler)