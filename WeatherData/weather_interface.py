import requests
from datetime import datetime
import os
from shared.consts import WEATHER_ENDPOINT
from typing import Dict, Optional


def get_date_weather(date: str, location: str) -> Optional[Dict]:
    """
    Get weather data for a specific date and location.

    Args:
        date (datetime): The date for which weather data is requested.
        location (str): The location for which weather data is requested.

    Returns:
        dict: A dictionary containing weather information for the specified date and location.
              Returns None if weather data is not available.
    """
    api_key = os.getenv("WEATHER_API")
    params = {
        "key": api_key,
        "q": location,
        "dt": date,
    }

    try:
        response = requests.get(WEATHER_ENDPOINT, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()
        forecast = data.get('forecast', {})
        forecastday = forecast.get('forecastday', [])
        if forecastday:
            day_data = forecastday[0].get('day', {})
            condition = day_data.get('condition')
            if day_data:
                return {
                    'avgtemp_c': day_data.get('avgtemp_c'),
                    'avghumidity': day_data.get('avghumidity'),
                    'condition': condition.get('text')
                }
        return None
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error occurred: {e}")
        return None
