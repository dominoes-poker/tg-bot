from bot.data_types import Game


def get_number_of_dices(game: Game, round_number: int) -> int:

    number_of_players = len(game.players)
    max_number_of_dices = 28 // number_of_players

    if max_number_of_dices > round_number:
        return round_number

    repeat_rounds = 17 - (2 * max_number_of_dices + 1)
    if max_number_of_dices + repeat_rounds < round_number + 1:
        return max_number_of_dices


def get_ending_for_ordered_number(number: int) -> str:
    if number > 9:
        return get_ending_for_ordered_number(number % 10)
    endings = {1: 'st', 2: 'nd', 3: 'rd'}
    return endings.get(number, 'th')
