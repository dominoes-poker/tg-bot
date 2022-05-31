from aiogram import F
from bot.dispatcher import TGDispatcher
from bot.handlers import Handler, GamerRegisterHandler
from bot.routers.router import TGRouter
from bot.services.gamer_data_service import GamerDataService
from bot.states import GamerRegisterState, RootState


class GamerRegisterRouter(TGRouter):
    def __init__(self, handler: GamerRegisterHandler) -> None:
        super().__init__(use_builtin_filters=True, name='GamerRegisterRouter')
        self.setup(handler=handler)

    def setup(self, handler: GamerRegisterHandler) -> None:
        self.message.register(self.handler(handler.ask_name),
                              RootState.GAMER_REGISTER, F.text.casefold() == 'yes')
        self.message.register(self.handler(handler.handle_name), GamerRegisterState.NAME)


def create_game_register_router(dispatcher: TGDispatcher,
                                gamer_data_service: GamerDataService) -> GamerRegisterRouter:
    handler = GamerRegisterHandler(dispatcher.bot, gamer_data_service)
    router = GamerRegisterRouter(handler)
    router.parent_router = dispatcher
    return router
