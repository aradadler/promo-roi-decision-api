import os


def get_fred_api_key() -> str | None:
    return os.getenv("FRED_API_KEY")