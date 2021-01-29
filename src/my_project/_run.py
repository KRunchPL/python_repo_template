from loguru import logger


def run(arguments: list[str]) -> None:
    """
    Execute application logic.

    :param arguments: list of arguments to run the application with
    """
    logger.info(f'Hello World! {arguments}')
