import asyncio
from typing import Iterable, List, Set
from bot.bot import TGBot

from bot.routers.handlers.common.keyboards import YES_NO_KEYBOARD, keyboard_from_data
from bot.routers.handlers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.player_service import GamerDataService
from bot.states import GameState
from bot.types import IncommingMessage, Game, Gamer


class RoundHandler(Handler):
    def __init__(self, bot: TGBot, 
                 player_data_service: GamerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._game_data_service = game_data_service

    async def ask_bet(self, message: IncommingMessage, context_service: ContextService) -> None:
        owner = await context_service.get_gamer()
        game = await self._game_data_service.create(owner)

        await context_service.set_current_game(game)
        await self.bot.send(
            chat_id = message.chat.id,
            text='Ok, let`s start a new game. Send me the names of players with comma separate',
        )
        await context_service.set_state(GameState.ADD_GAMERS)

    async def handle_gamer_names(self, message: IncommingMessage, context_service: ContextService) -> None:
        gamer_names = self._process_names(message.text.split(','))
        all_gamers = await self._player_data_service.get_users(names=gamer_names)

        game = await context_service.get_current_game()

        await self.bot.send(
            chat_id = message.chat.id,
            text='Ok, I will notify these persons about the game. Please, wait until they connect',
        )
        await context_service.set_state(GameState.WAIT_ANSWER)
        await self._invite_users(all_gamers, game, context_service)

    async def _invite_users(self, gamers: List[Gamer], game: Game, context_service: ContextService):
        invites = [self._invite_user(gamer, game, context_service) for gamer in gamers ]
        await context_service.set_awaing_responses_from(gamers)
        await asyncio.gather(*invites)
    
    async def _invite_user(self, gamer: Gamer, game: Game, context_service: ContextService):
        await self.bot.send(
            chat_id = gamer.identificator,
            text=f'{game.owner.username} invites you to a new game. Do you agree?',
            reply_markup=YES_NO_KEYBOARD
        )
        
        user_context = ContextService.for_user(context_service.context, gamer.identificator)
       
        gamer = await user_context.get_gamer()
        
        await user_context.set_state(GameState.WAIT_ANSWER)
        await user_context.set_current_game(game)

    async def handle_accept(self, message: IncommingMessage, context_service: ContextService):
        await self.bot.send(
            chat_id = message.chat.id,
            text=f'Ok, wait another users',
        )
        gamer = await context_service.get_gamer()
        if not gamer:
            gamer = await self._player_data_service.get_gamer(message.user_id)
            await context_service.set_gamer(gamer)
        current_game = await context_service.get_current_game()
        await self._set_agrement(gamer, current_game, context_service)

    async def _set_agrement(self, gamer: Gamer, game: Game, context_service: ContextService):
        owner_context_service = ContextService.for_user(context_service.context, game.owner.identificator)
        
        await owner_context_service.set_agrement(gamer)
        game = await self._game_data_service.add_gamers(gamer_ids=[gamer.id], game=game)
        owner_context_service.set_current_game(game)

        if not await owner_context_service.have_all_answers():
            return

        gamer_ids = await owner_context_service.get_agreed()
        await self._game_data_service.add_gamers(gamer_ids, game)

        await self.bot.send(
            chat_id = game.owner.identificator,
            text = 'Everyone has answered! You have to decide who is the first move maker',
            reply_markup=keyboard_from_data(list(gamer.username for gamer in game.gamers))
        )

    @staticmethod
    def _process_names(names: Iterable[str]) -> Set[str]:
        result = set()
        for name in names:
            name = name.strip()
            result.add(name)
        return result
