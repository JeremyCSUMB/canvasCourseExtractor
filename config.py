import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    api_key = os.getenv("CANVAS_API_KEY")
    domain = os.getenv("CANVAS_DOMAIN")

    if not api_key or not domain:
        raise ValueError("CANVAS_API_KEY and CANVAS_DOMAIN must be set in the .env file")

    return {
        "api_key": api_key,
        "domain": domain
    }
