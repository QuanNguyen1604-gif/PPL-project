"""OpenWeatherMap API service for fetching real-time weather data."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional

import requests

from assistant.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL

logger = logging.getLogger(__name__)

# Mapping of Vietnamese city names (no diacritics) to search queries
CITY_ALIASES: dict[str, str] = {
    'thanh pho ho chi minh': 'Ho Chi Minh City,VN',
    'ho chi minh': 'Ho Chi Minh City,VN',
    'hochiminh': 'Ho Chi Minh City,VN',
    'hcm': 'Ho Chi Minh City,VN',
    'vung tau': 'Vung Tau,VN',
    'vungtau': 'Vung Tau,VN',
    'quang ngai': 'Quang Ngai,VN',
    'quangngai': 'Quang Ngai,VN',
    'ha noi': 'Hanoi,VN',
    'hanoi': 'Hanoi,VN',
    'da nang': 'Da Nang,VN',
    'danang': 'Da Nang,VN',
    'hue': 'Hue,VN',
    'can tho': 'Can Tho,VN',
    'cantho': 'Can Tho,VN',
    'nha trang': 'Nha Trang,VN',
    'nhatrang': 'Nha Trang,VN',
    'da lat': 'Da Lat,VN',
    'dalat': 'Da Lat,VN',
    'hai phong': 'Hai Phong,VN',
    'haiphong': 'Hai Phong,VN',
    'bien hoa': 'Bien Hoa,VN',
    'bienhoa': 'Bien Hoa,VN',
    'quy nhon': 'Quy Nhon,VN',
    'quynhon': 'Quy Nhon,VN',
    'phan thiet': 'Phan Thiet,VN',
    'phanthiet': 'Phan Thiet,VN',
}


def _resolve_city(city_input: str) -> str:
    """Resolve a user-provided city name to an OpenWeatherMap search query."""
    normalized = city_input.strip().lower().replace(' ', '')
    # Try normalized (no spaces) first
    if normalized in CITY_ALIASES:
        return CITY_ALIASES[normalized]
    # Try with spaces
    city_lower = city_input.strip().lower()
    if city_lower in CITY_ALIASES:
        return CITY_ALIASES[city_lower]
    # Default: pass through as-is
    return city_input.strip()


def _api_available() -> bool:
    """Check whether the API key is configured."""
    return bool(OPENWEATHER_API_KEY)


def _convert_to_internal_format(api_data: dict, city_query: str) -> dict:
    """Convert OpenWeatherMap API response to the internal format used by WeatherModule."""
    city_name = api_data.get('name', city_query)
    return {
        'city': {
            'id': api_data.get('id', 0),
            'name': city_name,
            'findname': city_name.upper(),
        },
        'main': {
            'temp': api_data['main']['temp'],
            'pressure': api_data['main'].get('pressure', 0),
            'humidity': api_data['main'].get('humidity', 0),
        },
        'wind': {
            'speed': api_data.get('wind', {}).get('speed', 0),
            'deg': api_data.get('wind', {}).get('deg', 0),
        },
        'weather': [
            {
                'main': api_data['weather'][0]['main'],
                'description': api_data['weather'][0]['description'],
            }
        ],
    }


def _convert_forecast_item(item: dict, city_info: dict) -> dict:
    """Convert a single forecast list item to internal format."""
    return {
        'city': {
            'id': city_info.get('id', 0),
            'name': city_info.get('name', ''),
            'findname': city_info.get('name', '').upper(),
        },
        'main': {
            'temp': item['main']['temp'],
            'pressure': item['main'].get('pressure', 0),
            'humidity': item['main'].get('humidity', 0),
        },
        'wind': {
            'speed': item.get('wind', {}).get('speed', 0),
            'deg': item.get('wind', {}).get('deg', 0),
        },
        'weather': [
            {
                'main': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
            }
        ],
    }


def fetch_current_weather(city: str) -> Optional[dict]:
    """Fetch current weather from OpenWeatherMap API.

    Returns the data in internal format matching Mock_weather_data.json structure,
    or None if the API call fails.
    """
    if not _api_available():
        logger.debug('No API key configured, skipping live weather fetch.')
        return None

    city_query = _resolve_city(city)
    try:
        resp = requests.get(
            f'{OPENWEATHER_BASE_URL}/weather',
            params={
                'q': city_query,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric',
            },
            timeout=10,
        )
        if resp.status_code == 404:
            logger.info('City "%s" not found via API.', city)
            return None
        resp.raise_for_status()
        data = resp.json()
        result = _convert_to_internal_format(data, city_query)
        # When using metric units, temp is already in Celsius.
        # WeatherModule does `temp - 273.15`, so we convert back to Kelvin
        # to keep compatibility.
        result['main']['temp'] = data['main']['temp'] + 273.15
        return result
    except requests.RequestException as exc:
        logger.debug('Weather API request failed: %s', exc)
        return None


def fetch_forecast_for_date(city: str, target_date_str: str) -> Optional[dict]:
    """Fetch weather forecast for a specific date from OpenWeatherMap API.

    Args:
        city: City name as provided by user.
        target_date_str: Date in DD/MM/YYYY format.

    Returns the data in internal format, or None if the API call fails
    or the date is not within the 5-day forecast range.
    """
    if not _api_available():
        logger.debug('No API key configured, skipping live forecast fetch.')
        return None

    # Parse target date
    try:
        target_date = datetime.strptime(target_date_str, '%d/%m/%Y').date()
    except ValueError:
        logger.debug('Cannot parse date "%s" for forecast.', target_date_str)
        return None

    # Check if within forecast range (today + 5 days)
    today = datetime.now().date()
    if target_date < today or target_date > today + timedelta(days=5):
        logger.debug('Date %s is outside forecast range.', target_date_str)
        return None

    city_query = _resolve_city(city)
    try:
        resp = requests.get(
            f'{OPENWEATHER_BASE_URL}/forecast',
            params={
                'q': city_query,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric',
            },
            timeout=10,
        )
        if resp.status_code == 404:
            logger.info('City "%s" not found via forecast API.', city)
            return None
        resp.raise_for_status()
        data = resp.json()

        # Find the forecast entry closest to noon on the target date
        target_noon = datetime.combine(target_date, datetime.min.time().replace(hour=12))
        best_item = None
        best_diff = float('inf')

        for item in data.get('list', []):
            item_dt = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
            diff = abs((item_dt - target_noon).total_seconds())
            if diff < best_diff:
                best_diff = diff
                best_item = item

        if best_item is None:
            return None

        city_info = data.get('city', {})
        result = _convert_forecast_item(best_item, city_info)
        # Convert back to Kelvin for WeatherModule compatibility
        result['main']['temp'] = best_item['main']['temp'] + 273.15
        return result
    except requests.RequestException as exc:
        logger.debug('Forecast API request failed: %s', exc)
        return None
