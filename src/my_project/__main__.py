import sys

from loguru import logger

from my_project._run import run
from my_project._settings import Settings


def main() -> int:
    """
    Run the application.

    :return: return code
    """
    settings = Settings()  # Load settings and configure logger

    try:
        run(settings)
    except Exception:  # noqa: BLE001
        logger.exception('Uncaught exception')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
