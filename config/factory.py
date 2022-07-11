from config.config import Config, EnvConfig
from config.type import ConfigType


class ConfigFactory:
    def get_config(self) -> Config:
        raise NotImplementedError('The method to get config is not implemented')


class EnvConfigFactory(ConfigFactory):
    def get_config(self) -> EnvConfig:
        return EnvConfig()


def create_config(config_type: ConfigType) -> Config:

    if config_type == ConfigType.ENV:
        factory = EnvConfigFactory()
    else:
        raise ValueError(f'Config type {config_type.value} is not supported')

    return factory.get_config()
