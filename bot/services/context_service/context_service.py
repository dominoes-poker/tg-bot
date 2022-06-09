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

    async def get_player(self) -> Optional[Player]:
        data = await self._context.get_data()
        if 'player' in data:
            return data['player']
        return None

    async def set_player(self, player: Player) -> None:
        await self._context.update_data(player=player)

    async def get_current_game(self) -> Optional[Game]:
        data = await self._context.get_data()
        if 'current_game' in data:
            return data['current_game']
        return None

    async def set_current_game_id(self, game: Game) -> None:
        await self._context.update_data(current_game=game.id)

    async def set_awaing_responses_from(self, players: List[Player]):
        await self._context.update_data({
            'answers':  {player.id: None for player in players}
        })


    @classmethod
    def for_user(cls, context: FSMContext, user_id: int) -> 'ContextService':
        from aiogram.dispatcher.fsm.storage.base import StorageKey
        user_key = StorageKey(context.bot.id, int(user_id), int(user_id))
        context = FSMContext(context.bot, context.storage, user_key)
        return ContextService(context)

    
