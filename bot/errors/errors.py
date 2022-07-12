from sre_constants import SRE_FLAG_DOTALL
import re
from typing import Tuple


class BaseBotError(Exception):
    @property
    def message(self):
        raise NotImplementedError


class DatabaseError(BaseBotError):
    ...

    @property
    def message(self):
        return 'Some problem with data. Sorry'


class PlayerDatabaseError(DatabaseError):
    _pattern = None

    @property
    def message(self):
        return 'Some problem with player data. Sorry'

    @classmethod
    def looks_like_me(cls, error_message) -> Tuple[bool, Tuple]:
        match = cls._pattern.match(error_message)
        if match:
            return True, cls._get_details(match)
        return False, ()

    @classmethod
    def _get_details(cls, match) -> Tuple:
        raise NotImplementedError()


class UsernameExistsError(PlayerDatabaseError):
    _pattern = re.compile(r'.*Key \(username\)=\((?P<username>\w+)\).*', flags=SRE_FLAG_DOTALL)

    @property
    def message(self):
        return 'The player with the username already exists. Try another'

    @classmethod
    def _get_details(cls, match) -> Tuple:
        return match.group('username'),


class IdentificatorExistsError(PlayerDatabaseError):
    _pattern = re.compile(r'.*Key \(identificator\)=\((?P<identificator>\w+)\).*', flags=SRE_FLAG_DOTALL)

    @property
    def message(self):
        return 'The player with the identificator already exists. Try another'

    @classmethod
    def _get_details(cls, match) -> Tuple:
        return match.group('identificator'),




