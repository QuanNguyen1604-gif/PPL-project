"""
assistant/modules/weather.py — REFACTORED

Thay đổi chính:
- Không còn đọc weather_data.json trực tiếp
- Dùng WeatherRepository làm trung gian
- Logic hiển thị + fuzzy matching + synonym KHÔNG đổi
"""
from __future__ import annotations

import json
from datetime import datetime
from difflib import get_close_matches
from pathlib import Path

from assistant.config import RESPONSE_FILE, WEATHER_FILE
from assistant.models import Command
from assistant.modules.base import Module
from assistant.weather_repository import WeatherRepository


def find_closest(city_name: str, cities: list[str]) -> str | None:
    matches = get_close_matches(city_name, cities, n=1, cutoff=0.6)
    return matches[0] if matches else None


class WeatherModule(Module):
    def __init__(
        self,
        command: Command,
        *,
        weather_file: Path = WEATHER_FILE,
        response_file: Path = RESPONSE_FILE,
        repository: WeatherRepository | None = None,
    ):
        super().__init__(command)
        self.weather_file = weather_file
        self.response_file = response_file
        # Cho phép inject repository giả khi test
        self.repository = repository or WeatherRepository(fallback_file=weather_file)

    def respond(self) -> str:
        responses = json.loads(self.response_file.read_text(encoding="utf-8"))

        if not self.command.location:
            return responses["error_handler"]["location_404"].format(location="")

        # Date mặc định = hôm nay (thay đổi nhỏ: trước đây là '15/12/2024')
        date = self.command.date or datetime.today().strftime("%d/%m/%Y")
        normalized_location = self.command.location.replace(" ", "").lower()

        # 1) Hỏi repository — nó tự xử lý cache → API → fallback
        weather_info = self.repository.get_weather(normalized_location, date)

        # 2) Không tìm thấy → thử fuzzy matching trong fallback
        if weather_info is None:
            available_cities = self.repository.list_cities_for_date(date)
            if not available_cities:
                return responses["error_handler"]["date_404"]

            closest = find_closest(normalized_location, available_cities)
            if closest:
                # Lấy entry của city gợi ý để có tên đẹp
                suggested = self.repository.get_weather(closest, date)
                if suggested:
                    return responses["error_handler"]["closest_match"].format(
                        closest_city_name=suggested["city"]["name"]
                    )
            return responses["error_handler"]["location_404"].format(
                location=self.command.location
            )

        # 3) Có data → format và trả lời
        return self._format_weather(weather_info, responses)

    def _format_weather(self, weather_info: dict, responses: dict) -> str:
        city = weather_info["city"]["name"]
        description = weather_info["weather"][0]["description"]
        temperature = weather_info["main"]["temp"] - 273.15
        humidity = weather_info["main"]["humidity"]
        wind_speed = weather_info["wind"]["speed"]

        if self.command.verb == "show":
            return responses["weather"]["show"].format(
                city=city,
                description=description,
                temperature=f"{temperature:.1f}°C",
                humidity=humidity,
                wind_speed=wind_speed,
            )

        if self.command.verb == "tell":
            if not self.command.query:
                return responses["error_handler"]["query_404"]
            if self._description_matches(self.command.query, description):
                return f"Yes, {city} is {self.command.query}."
            return f"No, {city} is not {self.command.query}."

        return responses["wrong_input"]["missing_object"]

    @staticmethod
    def _description_matches(query: str, description: str) -> bool:
        synonyms = {
            "sunny": "sun", "sun": "sun",
            "rainy": "rain", "rain": "rain",
            "cloudy": "cloud", "clouds": "cloud",
            "windy": "wind",
            "snowy": "snow",
            "foggy": "fog", "fog": "fog",
            "clear": "clear",
        }
        query_norm = synonyms.get(query.lower(), query.lower())
        description_tokens = description.lower().replace("-", " ").split()
        description_norm_tokens = {synonyms.get(t, t) for t in description_tokens}
        return (
            query_norm in description_norm_tokens
            or query.lower() in description.lower()
        )