from dataclasses import dataclass
import os
from dotenv import load_dotenv


def _require_env(var_name: str) -> str:
    """Gets an environment variable.

    :param var_name: Name of the environment variable. 
    :raises EnvironmentError: If the variable is not set.
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


def get_kalshi_config() -> KalshiConfig:
    """Build and return Kalshi configuration from environment variables.

    :return: Kalshi API creds.
    """
    return KalshiConfig(
        api_key_id=_require_env("KALSHI_API_KEY_ID"),
        private_key_path=_require_env("KALSHI_PRIVATE_KEY_PATH")
    )
