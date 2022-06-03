from bot.bot import TGBot
from bot.routers.handlers import WellcomeHandler
from bot.routers.router import TGRouter
from bot.services.gamer_service import GamerDataService


class WellcomeRouter(TGRouter):
    def __init__(self, handler: WellcomeHandler) -> None:
        super().__init__(use_builtin_filters=True, name='WellcomeRouter')
        self.setup(handler=handler)

    def setup(self, handler: WellcomeHandler) -> None:
        self.message.register(self.handler(handler.handle_enter), commands=['start'])

def create_wellcome_router(bot: TGBot, gamer_data_service: GamerDataService) -> WellcomeRouter:
    handler = WellcomeHandler(bot, gamer_data_service)
    return WellcomeRouter(handler)
