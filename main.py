import os

from dotenv import load_dotenv
from telegram_interface.bot import run

if __name__ == "__main__":
    load_dotenv()
    run(os.getenv('TELEGRAM_TOKEN'))
