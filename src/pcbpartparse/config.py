from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    JsonConfigSettingsSource,
)
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(json_file="settings.json")

    group_dict: dict = {
        "IC.Semiconductors": "I",
        "Capacitors": "C",
        "Resistors": "R",
        "Diodes": "D",
    }
    output_path: str | os.PathLike = r"./output"
    input_path: str | os.PathLike = r"./input"

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
            JsonConfigSettingsSource(settings_cls),
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
