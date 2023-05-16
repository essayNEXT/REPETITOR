import os
import logging
from dotenv import load_dotenv

load_dotenv()

try:
    BOT_TOKEN = os.environ["BOT_TOKEN"]
except KeyError as err:
    logging.critical(f"Can`t read token from environment variable. Message: {err}")
    raise KeyError(err)
