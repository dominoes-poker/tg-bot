from aiogram import Router


class RootRouter(Router):
    def __init__(self, wellcome_router: Router, gamer_register_router: Router) -> None:
        super().__init__(use_builtin_filters=True, name="StartingHandler")
        self.setup(wellcome_router=wellcome_router, gamer_register_router=gamer_register_router)
        
    def setup(self, wellcome_router: Router, gamer_register_router: Router) -> None:
        self.include_router(wellcome_router)
        self.include_router(gamer_register_router)
