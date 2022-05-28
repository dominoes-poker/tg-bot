from aiogram import Router
from bot.handlers import Handler


class RootRouter(Router):
    def __init__(self, wellcom_handler: Handler) -> None:
        super().__init__(use_builtin_filters=True, name="StartingHandler")
        self.setup(wellcom_handler=wellcom_handler)
        
    def setup(self, wellcom_handler: Handler) -> None:
        self.message.register(wellcom_handler.handle, commands=['start'])

