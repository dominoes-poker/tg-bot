import asyncio
from typing import Iterable, List, Set
from bot.context import TGContext

from bot.dispatcher import TGDispatcher
from bot.routers.handlers.common.keyboards import YES_NO_KEYBOARD, keyboard_from_data
from bot.routers.handlers.handler import Handler
from bot.services.game_service import GameDataService
from bot.services.gamer_service import GamerDataService
from bot.states import GameState
from bot.types import IncommingMessage
from bot.types.gamer import Game, Gamer


class CreateGameHandler(Handler):
    def __init__(self, dispatcher: TGDispatcher, 
                 gamer_data_service: GamerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(dispatcher)
        self._gamer_data_service = gamer_data_service
        self._game_data_service = game_data_service

    async def ask_gamer_usernames(self, message: IncommingMessage, context: TGContext) -> None:
        owner = await context.get_gamer()
        game = await self._game_data_service.create(owner)

        await context.set_current_game(game)
        await self.bot.send(
            chat_id = message.chat.id,
            text='Ok, let`s start a new game. Send me the names of players with comma separate',
        )
        await context.set_state(GameState.ADD_GAMERS)

    async def handle_gamer_names(self, message: IncommingMessage, context: TGContext) -> None:
        gamer_names = self._process_names(message.text.split(','))
        all_gamers = await self._gamer_data_service.get_users(names=gamer_names)

        game = await context.get_current_game()

        await self.bot.send(
            chat_id = message.chat.id,
            text='Ok, I will notify these persons about the game. Please, wait until they connect',
        )
        await context.set_state(GameState.WAIT_ANSWER)
        await self._invite_users(all_gamers, game, context)

    async def _invite_users(self, gamers: List[Gamer], game: Game, context: TGContext):
        invites = [self._invite_user(gamer, game, context) for gamer in gamers ]
        answers = {gamer.id: None for gamer in gamers}
        await context.update_data(ANSWERS=answers)
        await asyncio.gather(*invites)
    
    async def _invite_user(self, gamer: Gamer, game: Game, context: TGContext):
        await self.bot.send(
            chat_id = gamer.identificator,
            text=f'{game.owner.name} invites you to a new game. Do you agree?',
            reply_markup=YES_NO_KEYBOARD
        )
        
        user_context = TGContext.for_user(context, gamer.identificator)
       
        gamer = await user_context.get_gamer()
        
        await user_context.set_state(GameState.WAIT_ANSWER)
        await user_context.set_current_game(game)

    async def handle_accept(self, message: IncommingMessage, context: TGContext):
        await self.bot.send(
            chat_id = message.chat.id,
            text=f'Ok, wait another users',
        )
        gamer = await context.get_gamer()
        if not gamer:
            gamer = await self._gamer_data_service.get_gamer(message.user_id)
            await context.set_gamer(gamer)
        current_game = await context.get_current_game()
        await self._set_agrement(gamer, current_game.owner, context)

    async def _set_agrement(self, gamer: Gamer, owner: Gamer, context: TGContext):
        owner_context = TGContext.for_user(context, owner.identificator)
        game_owner_data = await owner_context.get_data()

        answers = game_owner_data['ANSWERS']
        answers[gamer.id] = True

        game = await owner_context.get_current_game()
        game.gamers.append(gamer)

        if None in answers.values():
            return

        game_owner_data.pop('ANSWERS')

        await self.bot.send(
            chat_id = game.owner.identificator,
            text = 'Everyone has answered! You have to decide who is the first move maker',
            reply_markup=keyboard_from_data(list(gamer.name for gamer in game.gamers))
        )

    @staticmethod
    def _process_names(names: Iterable[str]) -> Set[str]:
        result = set()
        for name in names:
            name = name.strip()
            result.add(name)
        return result
