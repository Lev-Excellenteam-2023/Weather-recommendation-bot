from enum import Enum
from os import path


class FeelingCategories(Enum):
    VERY_HOT = "very hot"
    HOT = "hot"
    PLEASANT = "pleasant"
    COLD = "cold"
    VERY_COLD = "very cold"


DATABASE_URL = "https://telegrambot-96f0c-default-rtdb.firebaseio.com"
SERVICE_ACCOUNT_KEY_PATH = path.join('DataBase', "serviceAccountKey.json")
