from aiogram import Router, F
from bot.handlers import Handler
from bot.handlers.gamer_register_handler import GamerRegisterHandler
from bot.services.gamer_data_service import GamerDataService
from bot.states import GamerRegisterState, RootState


class GamerRegisterRouter(Router):
    def __init__(self, handler: Handler) -> None:
        super().__init__(use_builtin_filters=True, name='GamerRegisterRouter')
        self.setup(handler=handler)
        
    def setup(self, handler: Handler) -> None:
        self.message.register(handler.ask_name, RootState.GAMER_REGISTER, F.text.casefold() == 'yes')
        self.message.register(handler.handle_name, GamerRegisterState.NAME)
        self.message.register(handler.handle_username, GamerRegisterState.USERNAME)

def create_gamer_register_router(gamer_data_service: GamerDataService) -> GamerRegisterRouter:
    handler = GamerRegisterHandler(gamer_data_service)
    return GamerRegisterRouter(handler)