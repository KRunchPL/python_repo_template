import os
from typing import Annotated

from pydantic import AfterValidator
from pydantic_settings import BaseSettings, CliSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict

from my_project._logger_configurator import configure_logger, LoggerConfiguration


_DOTENV_VARIABLE_NAME = 'MY_PROJECT_DOTENV_FILE'


class Settings(BaseSettings):
    """
    Application settings.
    """

    logger_config: Annotated[LoggerConfiguration, AfterValidator(configure_logger)] = LoggerConfiguration()

    # Model configuration for the settings class.
    model_config = SettingsConfigDict(
        env_file=os.getenv(_DOTENV_VARIABLE_NAME, '.env'),
        env_file_encoding='utf-8',
        extra='ignore',
        validate_default=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            CliSettingsSource(settings_cls, cli_parse_args=True, cli_implicit_flags=True),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
