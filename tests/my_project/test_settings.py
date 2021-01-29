import importlib
from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest

import my_project._settings
from my_project._settings import _DOTENV_VARIABLE_NAME


@pytest.fixture
def env_vars_mock(request: SubRequest, monkeypatch: pytest.MonkeyPatch) -> dict[str, str | None]:
    value: dict[str, str | None] = request.param
    for env_var, mock_value in value.items():
        if mock_value is not None:
            monkeypatch.setenv(env_var, str(mock_value))
        else:
            monkeypatch.delenv(env_var, raising=False)
    return value


@pytest.fixture
def cli_vars_mock(request: SubRequest, monkeypatch: pytest.MonkeyPatch) -> list[str]:
    value: list[str] = request.param
    monkeypatch.setattr('sys.argv', ['test_script.py', *value])
    return value


@pytest.fixture
def dotenv_file_mock(request: SubRequest, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, str]:
    value: dict[str, str] = request.param
    dotenv_file_path = tmp_path / '.env'
    dotenv_file_path.write_text('\n'.join(f'{key}={val}' for key, val in value.items()))
    monkeypatch.setenv(_DOTENV_VARIABLE_NAME, str(dotenv_file_path))
    return value


@pytest.mark.parametrize(
    ['env_vars_mock', 'dotenv_file'],
    indirect=['env_vars_mock'],
    argvalues=[
        ({_DOTENV_VARIABLE_NAME: None}, '.env'),
        ({_DOTENV_VARIABLE_NAME: '.dotenv.dummy.test'}, '.dotenv.dummy.test'),
    ],
)
def test_model_configuration(env_vars_mock: dict[str, str | None], dotenv_file: str):
    _ = env_vars_mock
    importlib.reload(my_project._settings)

    assert my_project._settings.Settings.model_config['env_file'] == dotenv_file
    assert my_project._settings.Settings.model_config['env_file_encoding'] == 'utf-8'
    assert my_project._settings.Settings.model_config['env_prefix'] == ''
    assert my_project._settings.Settings.model_config['extra'] == 'ignore'
    assert my_project._settings.Settings.model_config['validate_default'] is True


@pytest.mark.parametrize(
    ['init', 'cli_vars_mock', 'env_vars_mock', 'dotenv_file_mock', 'expected_file_prefix'],
    indirect=['env_vars_mock', 'cli_vars_mock', 'dotenv_file_mock'],
    argvalues=[
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            [],
            {},
            {},
            'INIT_TEST',
        ),
        (
            {},
            ['--logger_config.file_prefix=CLI_TEST'],
            {},
            {},
            'CLI_TEST',
        ),
        (
            {},
            [],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {},
            'ENV_TEST',
        ),
        (
            {},
            [],
            {},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'DOTENV_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            ['--logger_config.file_prefix=CLI_TEST'],
            {},
            {},
            'INIT_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            [],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {},
            'INIT_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            [],
            {},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'INIT_TEST',
        ),
        (
            {},
            ['--logger_config.file_prefix=CLI_TEST'],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {},
            'CLI_TEST',
        ),
        (
            {},
            ['--logger_config.file_prefix=CLI_TEST'],
            {},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'CLI_TEST',
        ),
        (
            {},
            [],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'ENV_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            ['--logger_config.file_prefix=CLI_TEST'],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {},
            'INIT_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            ['--logger_config.file_prefix=CLI_TEST'],
            {},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'INIT_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            [],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'INIT_TEST',
        ),
        (
            {},
            ['--logger_config.file_prefix=CLI_TEST'],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'CLI_TEST',
        ),
        (
            {'logger_config': {'file_prefix': 'INIT_TEST'}},
            ['--logger_config.file_prefix=CLI_TEST'],
            {'LOGGER_CONFIG': r'{"file_prefix": "ENV_TEST"}'},
            {'LOGGER_CONFIG': r'{"file_prefix": "DOTENV_TEST"}'},
            'INIT_TEST',
        ),
    ],
)
def test_settings_priority(
    init: dict[str, str],
    env_vars_mock: dict[str, str | None],
    cli_vars_mock: list[str],
    dotenv_file_mock: dict[str, str],
    expected_file_prefix: str,
):
    _ = env_vars_mock, cli_vars_mock, dotenv_file_mock
    importlib.reload(my_project._settings)
    settings = my_project._settings.Settings.model_validate(init)
    assert settings.logger_config.file_prefix == expected_file_prefix
