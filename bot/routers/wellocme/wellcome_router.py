from bot.bot import TGBot
from bot.routers.handlers import WellcomeHandler
from bot.routers.router import TGRouter
from bot.services.player_service import PlayerDataService


class WellcomeRouter(TGRouter):
    def __init__(self, handler: WellcomeHandler) -> None:
        super().__init__(use_builtin_filters=True, name='WellcomeRouter')
        self.setup(handler=handler)

    def setup(self, handler: WellcomeHandler) -> None:
        self.message.register(self.handler(handler.handle_enter), commands=['start'])

def create_wellcome_router(bot: TGBot, player_data_service: PlayerDataService) -> WellcomeRouter:
    handler = WellcomeHandler(bot, player_data_service)
    return WellcomeRouter(handler)
