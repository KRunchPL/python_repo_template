import sys

from loguru import logger

from my_project._run import run


def _setup_logger() -> None:
    logger.remove()
    logger.add(sys.stdout)


def main(argv: list[str] | None = None) -> int:
    """
    Run the application.

    :param argv: arguments to run the application with, if not given sys.argv will be used
    :return: return code
    """
    if argv is None:
        argv = sys.argv

    _setup_logger()

    try:
        run(argv[1:])
    except Exception:  # noqa: BLE001
        logger.exception('Uncaught exception')
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))  # pragma: no cover
