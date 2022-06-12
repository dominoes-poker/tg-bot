from typing import List, Optional
from aiogram.dispatcher.fsm.state import State
from aiogram.dispatcher.fsm.context import FSMContext

from bot.types import Game, Player


class ContextService:
    def __init__(self, context: FSMContext) -> None:
        self._context = context

    @property
    def context(self) -> FSMContext:
        return self._context

    async def set_state(self, state: State) -> None:
        return await self._context.set_state(state)

    async def set_current_game_id(self, game: Game) -> None:
        await self._context.update_data(current_game_id=game.id)
    
    async def get_current_game_id(self) -> Optional[int]:
        data = await self._context.get_data()
        return data.get('current_game_id')

    
