import os
from pathlib import Path

from common import SingletonMetaClass


class Config(metaclass=SingletonMetaClass):
    def __init__(self) -> None:
        self._root_path = Path(__file__).parent.parent.resolve()
        self._token = self._get_token()
        self._data_service_url = self._get_data_service_url()
        self._messages_path = self._root_path / 'bot' / 'messages' / 'en'

    @property
    def message_path(self) -> Path:
        return self._messages_path

    @property
    def data_service_url(self) -> str:
        return self._data_service_url

    @property
    def token(self) -> str:
        return self._token

    @staticmethod
    def _get_required_var(env_variable_name: str) -> str:
        raise NotImplementedError('The method to get a required variable is not implemented')

    @staticmethod
    def _get_var(env_variable_name: str) -> str:
        raise NotImplementedError('The method to get a variable is not implemented')

    @classmethod
    def _get_token(cls) -> str:
        return cls._get_required_var('TOKEN')

    @classmethod
    def _get_data_service_url(cls) -> str:
        return cls._get_required_var('DATABASE_URI')

    @classmethod
    def _get_host(cls) -> str:
        return cls._get_var('HOST')

    @classmethod
    def _get_port(cls) -> str:
        return cls._get_var('PORT')


class EnvConfig(Config):
    @staticmethod
    def _get_required_var(env_variable_name: str) -> str:
        value = os.getenv(env_variable_name)
        if value is None:
            raise ValueError(f'The {env_variable_name} variable is not set')
        return value

    @staticmethod
    def _get_var(env_variable_name: str) -> str:
        return os.getenv(env_variable_name)
