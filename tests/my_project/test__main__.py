from unittest.mock import ANY, call, MagicMock

import pytest
from loguru import logger
from pytest_mock import MockerFixture

from my_project.__main__ import main


_TESTED_MODULE = main.__module__


@pytest.fixture
def settings_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(_TESTED_MODULE + '.Settings')


@pytest.fixture
def run_mock(mocker: MockerFixture) -> MagicMock:
    return mocker.patch(_TESTED_MODULE + '.run')


def test_main_loads_settings(mocker: MockerFixture):
    mock = MagicMock()
    for function_name in ('Settings', 'run'):
        mock.attach_mock(
            mocker.patch(_TESTED_MODULE + f'.{function_name}'),
            function_name,
        )

    main()

    assert mock.mock_calls == [
        call.Settings(),
        call.run(ANY),
    ]


@pytest.mark.parametrize(
    ['run_exception', 'expected_code'],
    [
        (None, 0),
        (ValueError, 1),
    ],
)
@pytest.mark.usefixtures('settings_mock')
def test_main_return_code(
    run_mock: MagicMock,
    run_exception: Exception | None,
    expected_code: int,
):
    run_mock.side_effect = run_exception

    assert main() == expected_code


@pytest.mark.usefixtures('settings_mock')
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
