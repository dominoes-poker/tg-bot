
from sqlalchemy.exc import IntegrityError

from bot.errors.errors import PlayerDatabaseError, UsernameExistsError, IdentificatorExistsError


def create_db_player_error(error: IntegrityError) -> PlayerDatabaseError:
    error_message = str(error).strip()

    error_classes = [UsernameExistsError, IdentificatorExistsError]

    for error_class in error_classes:
        it_is_me, details = error_class.looks_like_me(error_message)
        if it_is_me:
            return error_class(*details)
