from bot.data_types import Game


def get_number_of_dices(game: Game, round_number: int) -> int:

    number_of_players = len(game.players)
    max_number_of_dices = 28 // number_of_players
    repeat_rounds = game.max_round_number - (2 * max_number_of_dices)

    if round_number <= max_number_of_dices:
        return round_number

    if round_number <= max_number_of_dices + repeat_rounds:
        return max_number_of_dices

    if round_number <= game.max_round_number - 1:
        remainder = abs(round_number - 2 * max_number_of_dices - repeat_rounds)
        return remainder

    return max_number_of_dices


def get_ending_for_ordered_number(number: int) -> str:
    if number > 9:
        return get_ending_for_ordered_number(number % 10)
    endings = {1: 'st', 2: 'nd', 3: 'rd'}
    return endings.get(number, 'th')
