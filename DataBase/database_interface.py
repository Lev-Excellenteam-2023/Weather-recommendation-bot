from datetime import datetime
from typing import Dict, Any, Optional
import firebase_admin
from firebase_admin import credentials, db
from shared.consts import DATABASE_URL, SERVICE_ACCOUNT_KEY_PATH


class FirebaseHandler:
    """
    A utility class for interacting with Firebase Realtime Database.
    """

    def __init__(self):
        """
        Initialize the FirebaseHandler instance.

        Reads the credentials from the provided service account key file and
        initializes the Firebase app with the specified database URL.

        Note:
            Make sure to configure the 'DATABASE_URL' and 'service_account_key_path'
            constants in the 'const' module.

        """
        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {'databaseURL': DATABASE_URL})
        self.ref = db.reference("/")

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user data from the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            Optional[Dict[str, Any]]: The user data as a dictionary, or None if user does not exist.
        ValueError: If user_id is not a string, or user_id begins with '/'.
        """
        return self.ref.child(user_id).get()

    def user_exist(self, user_id: str) -> bool:
        """
        Check if a user exists in the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            bool: True if the user exists, False otherwise.
        ValueError: If user_id is not a string, or user_id begins with '/'.
        """
        return self.get_user(user_id) is not None

    def add_user_indication(self, user_id: str, date: datetime, k_args: Dict) -> None:
        """
        Add user indication data to the database for a specific date.

        Args:
            user_id (str): The ID of the user.
            date (datetime): The date and time of the indication.
            k_args (Dict): Additional data to be added as key-value pairs.
        """
        date_str = date.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
        user_ref = self.ref.child(user_id)
        user_data = user_ref.get()

        if user_data is None:
            user_ref.set({date_str: k_args})
        else:
            user_ref.child(date_str).set(k_args)
