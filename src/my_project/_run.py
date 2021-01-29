from loguru import logger

from my_project._settings import Settings


def run(settings: Settings) -> None:
    """
    Execute application logic.

    :param settings: application settings
    """
    logger.info('Hello World! {}', settings.model_dump_json(fallback=str))
