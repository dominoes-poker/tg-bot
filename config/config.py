import os

from common import SingletonMetaClass


class Config(metaclass=SingletonMetaClass):
    def __init__(self) -> None:
        self._token = self._get_token()
        self._data_service_url = self._get_data_service_url()

    @property
    def data_service_url(self) -> str:
        return self._data_service_url

    @property
    def token(self) -> str:
        return self._token

    @staticmethod
    def _get_required_var(env_variable_name: str) -> str:
        raise NotImplementedError('The method to get variable is not implemented')

    @classmethod
    def _get_token(cls, *args, **kwargs) -> str:
        return cls._get_required_var('TOKEN')
   
    @classmethod
    def _get_data_service_url(cls, *args, **kwargs) -> str:
        return cls._get_required_var('DATA_SERVICE_URL')


class EnvConfig(Config): 
    @staticmethod
    def _get_required_var(env_variable_name: str) -> str:
        value = os.getenv(env_variable_name)
        if value is None:
            raise ValueError(f'The {env_variable_name} variable isnot set')
        return value

