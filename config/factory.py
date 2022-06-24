from config.config import Config, EnvConfig
from config.type import ConfigType

class ConfigFactory:
    def get_config() -> Config:
        raise NotImplementedError('The method to get config is not impimented')


class EnvConfigFactory(ConfigFactory):
    def get_config() -> EnvConfig:
        return EnvConfig()

def create_config(config_type: ConfigType) -> ConfigType:
    factory = None
    
    if config_type == ConfigType.ENV:
        factory = EnvConfigFactory
    else:
        raise ValueError(f'Config type {config_type.value} is not supported')
    
    return factory.get_config()
