import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

from dataclasses import dataclass
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / 'config.yaml'


class ConfigError(Exception):
    """Custom exception for errors that occur when loading config files or environment variables."""
    pass


def _require_yaml_dict(dict_name: str) -> dict[str, Any]:
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = yaml.safe_load(f)

        return data.get(dict_name)

    except Exception as e:
        raise ConfigError(f"Failed to load config.yaml: {e}")


def _require_env_variable(var_name: str) -> str:
    """Gets an environment variable.

    :param var_name: Name of the environment variable
    :raises EnvironmentError: If the variable is not set
    :return: The value of the environment variable
    """
    load_dotenv()
    value = os.getenv(var_name)

    if not value:
        raise EnvironmentError(f"{var_name} environment variable not set.")

    return value


@dataclass
class KalshiConfig:
    """Configuration variables needed to create a Kalshi API client."""
    api_key_id: str
    private_key_path: str
    base_url: str


def get_kalshi_config() -> KalshiConfig:
    """Build and return Kalshi configuration from environment variables.

    :return: Kalshi API creds
    """
    config = _require_yaml_dict('kalshi')

    return KalshiConfig(
        api_key_id=_require_env_variable('KALSHI_API_KEY_ID'),
        private_key_path=_require_env_variable('KALSHI_PRIVATE_KEY_PATH'),
        base_url=config['base_url']
    )
