from __future__ import annotations

import json
import logging
from datetime import datetime
from difflib import get_close_matches
from pathlib import Path

from assistant.config import RESPONSE_FILE, USE_LIVE_API, WEATHER_FILE
from assistant.models import Command
from assistant.modules.base import Module
from assistant.modules.weather_api import fetch_current_weather, fetch_forecast_for_date

logger = logging.getLogger(__name__)


def find_closest(city_name: str, cities: list[str]) -> str | None:
    matches = get_close_matches(city_name, cities, n=1, cutoff=0.6)
    return matches[0] if matches else None


class WeatherModule(Module):
    def __init__(self, command: Command, *, weather_file: Path = WEATHER_FILE, response_file: Path = RESPONSE_FILE):
        super().__init__(command)
        self.weather_file = weather_file
        self.response_file = response_file

    def respond(self) -> str:
        responses = json.loads(self.response_file.read_text(encoding='utf-8'))

        if not self.command.location:
            return responses['error_handler']['location_404'].format(location='')

        # --- Try live API first ---
        if USE_LIVE_API:
            api_result = self._try_api(responses)
            if api_result is not None:
                return api_result
            logger.debug('API did not return data, falling back to local JSON.')

        # --- Fallback: read from local JSON file ---
        return self._respond_from_file(responses)

    def _try_api(self, responses: dict) -> str | None:
        """Attempt to get weather data from OpenWeatherMap API.

        Returns a formatted response string, or None if the API call fails.
        """
        location = self.command.location
        date = self.command.date

        # Determine whether to use current weather or forecast
        is_today = False
        if date is None or date == 'today':
            is_today = True
        else:
            try:
                target = datetime.strptime(date, '%d/%m/%Y').date()
                if target == datetime.now().date():
                    is_today = True
            except ValueError:
                pass

        weather_info = None
        if is_today:
            weather_info = fetch_current_weather(location)
        else:
            weather_info = fetch_forecast_for_date(location, date)

        if weather_info is None:
            return None

        # Format response (same logic as file-based)
        city = weather_info['city']['name']
        description = weather_info['weather'][0]['description']
        temperature = weather_info['main']['temp'] - 273.15
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed']

        if self.command.verb == 'show':
            return responses['weather']['show'].format(
                city=city,
                description=description,
                temperature=f'{temperature:.1f}°C',
                humidity=humidity,
                wind_speed=wind_speed,
            )

        if self.command.verb == 'tell':
            if not self.command.query:
                return responses['error_handler']['query_404']
            if self._description_matches(self.command.query, description):
                return f'Yes, {city} is {self.command.query}.'
            return f'No, {city} is not {self.command.query}.'

        return None

    def _respond_from_file(self, responses: dict) -> str:
        """Original file-based weather response (fallback)."""
        data = json.loads(self.weather_file.read_text(encoding='utf-8'))

        date = self.command.date or '15/12/2024'
        date_weather_info = data.get(date)
        if not date_weather_info:
            return responses['error_handler']['date_404']

        normalized_location = self.command.location.replace(' ', '').lower()
        weather_info = next(
            (
                item
                for item in date_weather_info
                if item['city']['findname'].replace(' ', '').lower() == normalized_location
            ),
            None,
        )

        if weather_info is None:
            city_findnames = [item['city']['findname'].replace(' ', '').lower() for item in date_weather_info]
            closest_city = find_closest(normalized_location, city_findnames)
            if closest_city:
                match = next(item for item in date_weather_info if item['city']['findname'].replace(' ', '').lower() == closest_city)
                return responses['error_handler']['closest_match'].format(closest_city_name=match['city']['name'])
            return responses['error_handler']['location_404'].format(location=self.command.location)

        city = weather_info['city']['name']
        description = weather_info['weather'][0]['description']
        temperature = weather_info['main']['temp'] - 273.15
        humidity = weather_info['main']['humidity']
        wind_speed = weather_info['wind']['speed']

        if self.command.verb == 'show':
            return responses['weather']['show'].format(
                city=city,
                description=description,
                temperature=f'{temperature:.1f}°C',
                humidity=humidity,
                wind_speed=wind_speed,
            )

        if self.command.verb == 'tell':
            if not self.command.query:
                return responses['error_handler']['query_404']
            if self._description_matches(self.command.query, description):
                return f'Yes, {city} is {self.command.query}.'
            return f'No, {city} is not {self.command.query}.'

        return responses['wrong_input']['missing_object']

    @staticmethod
    def _description_matches(query: str, description: str) -> bool:
        synonyms = {
            'sunny': 'sun',
            'sun': 'sun',
            'rainy': 'rain',
            'rain': 'rain',
            'cloudy': 'cloud',
            'clouds': 'cloud',
            'windy': 'wind',
            'snowy': 'snow',
            'foggy': 'fog',
            'clear': 'clear',
            'fog': 'fog',
        }
        query_norm = synonyms.get(query.lower(), query.lower())
        description_tokens = description.lower().replace('-', ' ').split()
        description_norm_tokens = {synonyms.get(token, token) for token in description_tokens}
        return query_norm in description_norm_tokens or query.lower() in description.lower()
