from datetime import datetime
from typing import Dict, Any, Optional

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://telegrambot-96f0c-default-rtdb.firebaseio.com"})

# Access the Firestore database
ref = db.reference("/")


def get_user(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve user data from the database.

    Args:
        user_id (str): The ID of the user.

    Returns:
        Optional[Dict[str, Any]]: The user data as a dictionary, or None if user does not exist.
    """
    return ref.child(user_id).get()


def user_exist(user_id: str) -> bool:
    """
    Check if a user exists in the database.

    Args:
        user_id (str): The ID of the user.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return get_user(user_id) is not None


def add_user_indication(user_id: str, date: datetime, **kwargs: Dict) -> None:
    """
    Add user indication data to the database for a specific date.

    Args:
        user_id (str): The ID of the user.
        date (datetime): The date and time of the indication.
        **kwargs (Dict): Additional data to be added as key-value pairs.
    """
    date_str = date.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
    user_ref = ref.child(user_id)
    user_data = user_ref.get()

    if user_data is None:
        user_ref.set({date_str: kwargs})
    else:
        user_ref.child(date_str).set(kwargs)
