import sys
from unittest.mock import ANY, call, MagicMock

import pytest
from loguru import logger
from pytest_mock import MockerFixture

from my_project.__main__ import _setup_logger, main


_TESTED_MODULE = _setup_logger.__module__


def test_setup_logger(mocker: MockerFixture):
    logger_mock = mocker.patch(_TESTED_MODULE + '.logger')

    _setup_logger()

    assert logger_mock.mock_calls == [
        call.remove(),
        call.add(sys.stdout),
    ]


@pytest.fixture
def setup_logger_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(_TESTED_MODULE + '._setup_logger')


@pytest.fixture
def run_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(_TESTED_MODULE + '.run')


def test_main_setup_logger_before_running_mock(mocker: MockerFixture):
    mock = MagicMock()
    for function_name in ('_setup_logger', 'run'):
        mock.attach_mock(
            mocker.patch(_TESTED_MODULE + f'.{function_name}'),
            function_name,
        )

    main()

    assert mock.mock_calls == [
        call._setup_logger(),
        call.run(ANY),
    ]


@pytest.mark.usefixtures('setup_logger_mock')
def test_main_uses_sys_argv(
    mocker: MockerFixture,
    run_mock: MagicMock,
):
    sys_argv_mock = mocker.patch.object(sys, 'argv')

    main()

    run_mock.assert_called_once_with(sys_argv_mock[1:])


@pytest.mark.usefixtures('setup_logger_mock')
def test_main_uses_provided_argv(run_mock: MagicMock):
    my_argv = MagicMock()

    main(my_argv)

    run_mock.assert_called_once_with(my_argv[1:])


@pytest.mark.parametrize(
    ['run_exception', 'expected_code'],
    [
        (None, 0),
        (ValueError, 1),
    ],
)
@pytest.mark.usefixtures('setup_logger_mock')
def test_main_return_code(
    run_mock: MagicMock,
    run_exception: Exception | None,
    expected_code: int,
):
    run_mock.side_effect = run_exception

    assert main() == expected_code


@pytest.mark.usefixtures('setup_logger_mock')
def test_main_logs_exception(run_mock: MagicMock):
    run_exception = ValueError('OH NO! SOMETHING WENT WRONG!')
    run_mock.side_effect = run_exception
    log_messages = []

    def custom_sink(message):
        log_messages.append(message)

    logger.remove()
    logger.add(custom_sink, format='{message}')

    main()

    assert str(run_exception) in ''.join(log_messages)
