import requests
import datetime
import base64
from urllib.parse import urlparse

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric import padding

from kalshi_bot.config import KalshiConfig


class KalshiClientError(Exception):
    """Custom exception for KalshiCLient errors."""
    pass


class KalshiClient:

    def __init__(self, config: KalshiConfig) -> None:
        self.api_key_id = config.api_key_id
        self.private_key = self._load_private_key(config.private_key_path)
        self.base_url = config.base_url

    def _load_private_key(self, private_key_path) -> RSAPrivateKey:
        try:
            with open(private_key_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )

            if not isinstance(private_key, RSAPrivateKey):
                raise TypeError("Expected an RSA private key")

            return private_key

        except Exception as e:
            raise KalshiClientError(f"Failed to load private key: {e}")

    def _create_signature(self, timestamp, method, path) -> str:
        """Create request signature per Kalshi docs.

        :param timestamp: Request timestamp in milliseconds
        :param method: HTTP method
        :param path: Request path
        :return: Base64 encoded signature
        """
        message = (timestamp + method + path).encode('utf-8')

        signature = self.private_key.sign(
            message,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.DIGEST_LENGTH),
            hashes.SHA256()
        )

        return base64.b64encode(signature).decode('utf-8')

    # From Kalshi API docs for testing
    def get(self, path):
        """Make an authenticated GET request to the Kalshi API."""
        timestamp = str(int(datetime.datetime.now().timestamp() * 1000))
        # Signing requires the full URL path from root (e.g. /trade-api/v2/portfolio/balance)
        sign_path = urlparse(self.base_url + path).path
        signature = self._create_signature(timestamp, "GET", sign_path)

        headers = {
            'KALSHI-ACCESS-KEY': self.api_key_id,
            'KALSHI-ACCESS-SIGNATURE': signature,
            'KALSHI-ACCESS-TIMESTAMP': timestamp
        }

        return requests.get(self.base_url + path, headers=headers)
