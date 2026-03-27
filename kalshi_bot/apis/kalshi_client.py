import requests
import os
from pathlib import Path

from kalshi_bot.config import KalshiConfig

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes


class KalshiClientError(Exception):
    """Custom exception for KalshiCLient errors."""
    pass


class KalshiClient:

    def __init__(self, config: KalshiConfig) -> None:
        self.api_key_id = config.api_key_id
        self.private_key_path = config.private_key_path

    def _load_private_key(self) -> PrivateKeyTypes:
        try:
            fpath = Path(self.private_key_path)
            if not fpath.exists():
                raise KalshiClientError(
                    f"Private key file not found at: {self.private_key_path}")

            with open(fpath, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )

            return private_key

        except Exception as e:
            raise KalshiClientError(f"Failed to load private key: {e}")
