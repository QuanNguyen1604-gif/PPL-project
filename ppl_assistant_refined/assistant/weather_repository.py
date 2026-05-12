"""
assistant/weather_repository.py

Lớp trung gian quyết định nguồn dữ liệu thời tiết.
Thứ tự ưu tiên:
  1) Cache trong file cache_weather.json (TTL 1 giờ)
  2) OpenWeather API (nếu có key + có mạng)
  3) Fallback về weather_data.json (data tĩnh có sẵn)

WeatherModule không cần biết data đến từ đâu —
chỉ cần gọi repository.get_weather(city, date) là xong.
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import urllib.request
import urllib.parse
import urllib.error

from assistant.config import WEATHER_FILE

#Cấu hình API

OPENWEATHER_API_KEY: str = "6c0afa7ef7e1ac6694a2b6c5dbc79c21"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
CACHE_TTL_SECONDS = 60 * 60  # 1 giờ
CACHE_FILE = Path(__file__).parent.parent / "data" / "cache_weather.json"
REQUEST_TIMEOUT = 5  #giây

CITY_NAME_OVERRIDE = {
    "danang":         "Da Nang",
    "hochiminh":      "Ho Chi Minh City",
    "hochiminhcity":  "Ho Chi Minh City",
    "saigon":         "Ho Chi Minh City",
    "hanoi":          "Hanoi",
    "haiphong":       "Hai Phong",
    "cantho":         "Can Tho",
    "hue":            "Hue",
    "nhatrang":       "Nha Trang",
    "vungtau":        "Vung Tau",
    "dalat":          "Da Lat",
    "haiduong":       "Hai Duong",
    "quangninh":      "Quang Ninh",
    "phuquoc":        "Phu Quoc",
}


class WeatherRepository:
    """Quản lý 3 nguồn data: cache → API → fallback JSON."""

    def __init__(
        self,
        *,
        api_key: str = OPENWEATHER_API_KEY,
        cache_file: Path = CACHE_FILE,
        fallback_file: Path = WEATHER_FILE,
    ):
        self.api_key = api_key
        self.cache_file = cache_file
        self.fallback_file = fallback_file

    
    #PUBLIC API: WeatherModule chỉ gọi hàm này

    def get_weather(self, city: str, date: str) -> Optional[dict]:
        """
        Trả về 1 entry weather (dict) hoặc None nếu không tìm thấy.

        Args:
            city: tên thành phố (đã chuẩn hoá lowercase, không khoảng trắng)
            date: 'DD/MM/YYYY'

        Returns:
            dict cùng format với weather_data.json hiện có, hoặc None.
        """
        # 1. Thử cache trước
        cached = self._read_cache(city, date)
        if cached:
            return cached

        # 2. Gọi API nếu có key
        if self.api_key:
            api_data = self._fetch_from_api(city, date)
            if api_data:
                self._write_cache(city, date, api_data)
                return api_data

        # 3. Fallback về JSON tĩnh
        return self._read_fallback(city, date)

    def list_cities_for_date(self, date: str) -> list[str]:
        """Trả về list 'findname' của các city có data cho ngày này (dùng cho fuzzy match)."""
        # Cache không lưu hết tất cả city, nên fallback file là nguồn duy nhất cho fuzzy
        try:
            data = json.loads(self.fallback_file.read_text(encoding="utf-8"))
            entries = data.get(date, [])
            return [e["city"]["findname"].replace(" ", "").lower() for e in entries]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return []

    def _read_cache(self, city: str, date: str) -> Optional[dict]:
        if not self.cache_file.exists():
            return None
        try:
            cache = json.loads(self.cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

        key = self._cache_key(city, date)
        entry = cache.get(key)
        if not entry:
            return None

        # Kiểm tra TTL
        if time.time() - entry.get("_cached_at", 0) > CACHE_TTL_SECONDS:
            return None

        return entry.get("data")

    def _write_cache(self, city: str, date: str, data: dict) -> None:
        cache: dict = {}
        if self.cache_file.exists():
            try:
                cache = json.loads(self.cache_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                cache = {}

        cache[self._cache_key(city, date)] = {
            "_cached_at": time.time(),
            "data": data,
        }

        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(
            json.dumps(cache, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    @staticmethod
    def _cache_key(city: str, date: str) -> str:
        return f"{city}|{date}"

    def _fetch_from_api(self, city: str, date: str) -> Optional[dict]:
        """
        Gọi 1 trong 2 endpoint:
        - /weather    cho hôm nay
        - /forecast   cho ngày trong 5 ngày tới (3-hour intervals)
        """
        try:
            target_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return None

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        delta_days = (target_date - today).days

        # Quá 5 ngày hoặc quá khứ → API free không hỗ trợ
        if delta_days < 0 or delta_days > 5:
            return None

        try:
            if delta_days == 0:
                return self._fetch_current(city)
            return self._fetch_forecast(city, target_date)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, KeyError):
            # Lỗi mạng / API → để None để rơi xuống fallback
            return None

    def _fetch_current(self, city: str) -> Optional[dict]:
        params = urllib.parse.urlencode({"q": city, "appid": self.api_key})
        url = f"{OPENWEATHER_BASE_URL}/weather?{params}"

        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        return self._normalize_api_response(payload, query=city)

    def _fetch_forecast(self, city: str, target_date: datetime) -> Optional[dict]:
        params = urllib.parse.urlencode({"q": city, "appid": self.api_key})
        url = f"{OPENWEATHER_BASE_URL}/forecast?{params}"

        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        # /forecast trả về list 40 entries (5 ngày × 8 mốc 3h)
        # Pick mốc gần 12:00 trưa nhất của ngày target
        target_noon = target_date.replace(hour=12)
        best = None
        best_diff = float("inf")

        for entry in payload.get("list", []):
            entry_time = datetime.fromtimestamp(entry["dt"])
            if entry_time.date() != target_date.date():
                continue
            diff = abs((entry_time - target_noon).total_seconds())
            if diff < best_diff:
                best_diff = diff
                best = entry

        if not best:
            return None

        # Cần thêm city info vì /forecast trả khác /weather
        city_info = payload.get("city", {})
        normalized = self._normalize_api_response({
            **best,
            "name": city_info.get("name", city),
            "id": city_info.get("id", 0),
            "sys": {"country": city_info.get("country", "")},
            "coord": city_info.get("coord", {}),
        }, query=city)
        return normalized

    @staticmethod
    def _normalize_api_response(payload: dict, query: str = "") -> dict:
        """
        Chuyển response của OpenWeather sang format giống weather_data.json
        để WeatherModule dùng được không cần sửa code.

        query: tên gốc user nhập (để override tên sai từ OpenWeather).
        """
        api_name = payload.get("name", "")
        # Áp dụng override nếu có (vd: "Turan" → "Da Nang")
        normalized_query = query.replace(" ", "").lower()
        display_name = CITY_NAME_OVERRIDE.get(normalized_query, api_name)

        return {
            "city": {
                "id": payload.get("id", 0),
                "name": display_name,
                "findname": display_name.upper(),
                "country": payload.get("sys", {}).get("country", ""),
                "coord": payload.get("coord", {}),
                "zoom": 7,
            },
            "time": payload.get("dt", int(time.time())),
            "main": payload.get("main", {}),
            "wind": payload.get("wind", {}),
            "clouds": payload.get("clouds", {"all": 0}),
            "weather": payload.get("weather", []),
        }

    def _read_fallback(self, city: str, date: str) -> Optional[dict]:
        try:
            data = json.loads(self.fallback_file.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            return None

        entries = data.get(date, [])
        normalized_query = city.replace(" ", "").lower()
        for entry in entries:
            findname = entry.get("city", {}).get("findname", "").replace(" ", "").lower()
            if findname == normalized_query:
                return entry
        return None