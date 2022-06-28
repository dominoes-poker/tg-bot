from bot.bot import DPBot
from bot.routers.help.handler import HelpHandler
from bot.routers.router import DPRouter


def setup_router(router: DPRouter, handler: HelpHandler) -> None:
    router.setup_handler(handler.help_handler, commands=['help'])

def create_help_router(bot: DPBot) -> DPRouter:
    handler = HelpHandler(bot)

    router = DPRouter(name='<Help> - Router')
    setup_router(router, handler)

    return router
