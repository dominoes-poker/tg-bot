from bot.dispatcher import TGDispatcher
from bot.handlers import WellcomeHandler
from bot.routers.router import TGRouter
from bot.services.gamer_data_service import GamerDataService


class WellcomeRouter(TGRouter):
    def __init__(self, handler: WellcomeHandler) -> None:
        super().__init__(use_builtin_filters=True, name='WellcomeRouter')
        self.setup(handler=handler)

    def setup(self, handler: WellcomeHandler) -> None:
        self.message.register(self.handler(handler.enter_handle), commands=['start'])

def create_wellcome_router(dispatcher: TGDispatcher,
                           gamer_data_service: GamerDataService) -> WellcomeRouter:
    handler = WellcomeHandler(dispatcher.bot, gamer_data_service)
    router = WellcomeRouter(handler)
    router.parent_router = dispatcher
    return WellcomeRouter
