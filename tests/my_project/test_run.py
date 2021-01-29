from unittest.mock import MagicMock

from my_project._run import run


def test_run():
    run(MagicMock())
