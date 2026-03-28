from kalshi_bot.config import KalshiConfig, get_kalshi_config
from kalshi_bot.apis.kalshi_client import KalshiClient


def main() -> None:
    kalshi_conf = get_kalshi_config()
    kalshi_client = KalshiClient(kalshi_conf)

    res = kalshi_client.get('/portfolio/balance')
    print(res.json())


if __name__ == "__main__":
    main()
