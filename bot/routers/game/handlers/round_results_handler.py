
from typing import List
from bot.bot import TGBot

from bot.routers.handlers.common.keyboards import keyboard_from_data
from bot.routers.handlers.handler import Handler
from bot.services.context_service import ContextService
from bot.services.game_service import GameDataService
from bot.services.player_service import PlayerDataService
from bot.types import Game, IncommingMessage, Round, Stake
from bot.states import RoundState
from aiogram.types import ReplyKeyboardRemove


class RoundResultsHandler(Handler):
    def __init__(self, bot: TGBot, 
                 player_data_service: PlayerDataService,
                 game_data_service: GameDataService) -> None:
        super().__init__(bot)
        self._player_data_service = player_data_service
        self._game_data_service = game_data_service
    

    async def ask_results(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        
        last_round = game.last_round
        


        await self._bot.send(
            chat_id=message.user_id,
            text=f'How many did {last_round}',
            reply_markup=keyboard_from_data(next_players)
        )
        await context_service.set_state(RoundState.WAIT_USERNAME_TO_BET)
    
    async def handle_username(self, message: IncommingMessage, context_service: ContextService) -> None:
        username = message.text
        await context_service.wait_bet_of(username)

        await self._bot.send(
            chat_id=message.user_id,
            text=f'Whow many does {username} bet?',
            reply_markup=keyboard_from_data(self._get_variants_to_bet())
        )
        await context_service.set_state(RoundState.WAIT_BET_OF_PLAYER)


    async def handle_bet(self, message: IncommingMessage, context_service: ContextService) -> None:
        game_id = await context_service.get_current_game_id()
        game = await self._game_data_service.get_game(game_id)
        
        username = await context_service.from_whom_expect_bet()
        player = next(filter(lambda p: p.username == username, game.players))

        stake = Stake(
            playerId=player.id,
            bet = int(message.text),
            roundId=1,
        )
        game = await self._game_data_service.player_makes_bet(game_id, stake)
        if len(game.last_round.stakes) < len(game.players):
            return await self.ask_who_make_bet(message, context_service)
        
        await self._bot.send(
            chat_id=message.user_id,
            text=f'Everyone made a bet, now - play'
        )


    def _get_variants_to_bet(self,) -> List[int]:
        return [0, 1]

    def _get_players_to_bet(self, game: Game) -> List[str]:
        if not game.rounds or not game.rounds[-1].stakes:
            return [player.username for player in game.players]
        players_made_bets = {stake.playerId for stake in game.rounds[-1].stakes}
        return [
            player.username 
            for player in game.players 
            if player.id not in players_made_bets
        ]