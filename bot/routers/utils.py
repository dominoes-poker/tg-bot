from bot.types import Game


def get_number_of_dices(game: Game, round_number: int):
        number_of_players = len(game.players)
        max_number_of_dices = 28 // number_of_players
        if max_number_of_dices > round_number + 1:
            return round_number + 1
        repeat_rounds = 17 - (2*max_number_of_dices + 1)
        if max_number_of_dices + repeat_rounds < round_number + 1:
            return max_number_of_dices