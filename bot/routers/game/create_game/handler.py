from typing import Iterable, Set

from bot.bot import TGBot
from bot.routers.common.keyboards import keyboard_round
from bot.routers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.states import GameState, RoundState
from bot.types import IncommingMessage


class CreateGameHandler(Handler):
    def __init__(self, bot: TGBot,
                 player_data_service: PlayerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._game_data_service = game_data_service

    async def ask_player_usernames(self, message: IncommingMessage, _: ContextService) -> None:
        await self.bot.send(
            chat_id=message.user_id,
            text='Ok, lets start a new game. ' \
                 'Who will play with you? ' \
                 'Send me usernames of every player',
        )
        return GameState.WAIT_PLAYER_USERNAMES

    async def handle_player_usernames(self, message: IncommingMessage, context_service: ContextService) -> None:
        player_usernames = self._process_names(message.text.split(','))
        player = await self._player_data_service.get_player_by_identificator(message.user_id)
        player_usernames.add(player.username)
        
        if len(player_usernames) < 2:
            return await self.bot.send(
                chat_id=message.user_id,
                text=f'At least two players must be participants at game. Please, try again.'
            )
        players = await self._player_data_service.get_players_by_username(player_usernames)
        if len(players) != len(player_usernames):
            found_usernams = {player.username for player in players}
            strange_usernames = filter(lambda username: username not in found_usernams, player_usernames)
            return await self.bot.send(
                chat_id=message.user_id,
                text=f'I could not find users: `{"`, `".join(strange_usernames)}`. Please, check and send correct'
            )
        game = await self._game_data_service.create(players=players)
        await context_service.set_current_game_id(game)
        await self.bot.send(
            chat_id=message.user_id,
            text='Great! We are ready to start the first round',
            reply_markup=keyboard_round(1)
        )
        return RoundState.START
        
    @staticmethod
    def _process_names(names: Iterable[str]) -> Set[str]:
        return set(name.strip() for name in names)