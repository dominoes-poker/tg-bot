from typing import Optional

from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.storage.base import StorageKey

from bot.types.gamer import Game, Gamer

class TGContext(FSMContext):
    
    async def get_gamer(self) -> Optional[Gamer]:
        data = await self.get_data()
        if 'gamer' in data:
            return data['gamer']
        return None

    async def set_gamer(self, gamer: Gamer) -> None:
        await self.update_data(gamer=gamer)

    async def get_current_game(self) -> Optional[Game]:
        data = await self.get_data()
        if 'current_game' in data:
            return data['current_game']
        return None

    async def set_current_game(self, game: Game) -> None:
        await self.update_data(current_game=game)

    @classmethod
    def from_state(cls, state: FSMContext) -> 'TGContext':
        return cls(state.bot, state.storage, state.key)

    @classmethod
    def for_user(cls, context: 'TGContext', user_id: int) -> 'TGContext':
        user_key = StorageKey(context.bot.id, int(user_id), int(user_id))
        return TGContext(context.bot, context.storage, user_key)