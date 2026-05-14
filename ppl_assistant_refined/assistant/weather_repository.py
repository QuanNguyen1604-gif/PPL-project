"""
assistant/weather_repository.py

Lớp trung gian quyết định nguồn dữ liệu thời tiết.
Thứ tự ưu tiên:
  1) Cache trong file cache_weather.json (TTL 1 giờ)
  2) OpenWeather API (nếu có key + có mạng)
  3) Fallback về weather_data.json (data tĩnh có sẵn)
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

# Cấu hình API và cach
OPENWEATHER_API_KEY: str = "6c0afa7ef7e1ac6694a2b6c5dbc79c21"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
CACHE_TTL_SECONDS = 60 * 60  # 1 giờ
CACHE_FILE = Path(__file__).parent.parent / "data" / "cache_weather.json"
CACHE_VERSION = "v2" 
REQUEST_TIMEOUT = 5

CITY_QUERY_MAP = {
    "hanoi":         {"api_query": "Hanoi,VN",            "display": "Hanoi"},
    "hochiminh":     {"api_query": "Ho Chi Minh City,VN", "display": "Ho Chi Minh City"},
    "hochiminhcity": {"api_query": "Ho Chi Minh City,VN", "display": "Ho Chi Minh City"},
    "saigon":        {"api_query": "Ho Chi Minh City,VN", "display": "Ho Chi Minh City"},
    "danang":        {"api_query": "Da Nang,VN",          "display": "Da Nang"},
    "haiphong":      {"api_query": "Hai Phong,VN",        "display": "Hai Phong"},
    "cantho":        {"api_query": "Can Tho,VN",          "display": "Can Tho"},
    "hue":           {"api_query": "Hue,VN",              "display": "Hue"},
    "nhatrang":      {"api_query": "Nha Trang,VN",        "display": "Nha Trang"},
    "vungtau":       {"api_query": "Vung Tau,VN",         "display": "Vung Tau"},
    "dalat":         {"api_query": "Da Lat,VN",           "display": "Da Lat"},
    "phuquoc":       {"api_query": "Phu Quoc,VN",         "display": "Phu Quoc"},
}


def resolve_city_query(normalized_query: str) -> tuple[str, Optional[str]]:
    """
    Chuyển query của user thành (api_query, display_name).

    Nếu nằm trong map → dùng giá trị đã định nghĩa.
    Nếu không → giữ nguyên query (cho city quốc tế).
    """
    if normalized_query in CITY_QUERY_MAP:
        info = CITY_QUERY_MAP[normalized_query]
        return info["api_query"], info["display"]
    return normalized_query, None


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

    def get_weather(self, city: str, date: str) -> Optional[dict]:
        # 1. Cache
        cached = self._read_cache(city, date)
        if cached:
            return cached

        # 2. API
        if self.api_key:
            api_data = self._fetch_from_api(city, date)
            if api_data:
                self._write_cache(city, date, api_data)
                return api_data

        # 3. Fallback
        return self._read_fallback(city, date)

    def list_cities_for_date(self, date: str) -> list[str]:
        try:
            data = json.loads(self.fallback_file.read_text(encoding="utf-8"))
            entries = data.get(date, [])
            return [e["city"]["findname"].replace(" ", "").lower() for e in entries]
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return []

    # ── CACHE ────────────────────────────────────────────────────────────
    def _read_cache(self, city: str, date: str) -> Optional[dict]:
        if not self.cache_file.exists():
            return None
        try:
            cache = json.loads(self.cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None

        entry = cache.get(self._cache_key(city, date))
        if not entry:
            return None
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
        # Version prefix: khi đổi CACHE_VERSION → tự động invalidate cache cũ
        return f"{CACHE_VERSION}|{city}|{date}"

    # ── API ──────────────────────────────────────────────────────────────
    def _fetch_from_api(self, city: str, date: str) -> Optional[dict]:
        try:
            target_date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            return None

        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        delta_days = (target_date - today).days

        # Quá 5 ngày hoặc quá khứ → API free không hỗ trợ
        if delta_days < 0 or delta_days > 5:
            return None

        # Resolve query về tên thật mà OpenWeather hiểu
        api_query, display_name = resolve_city_query(city)

        try:
            if delta_days == 0:
                return self._fetch_current(api_query, display_name)
            return self._fetch_forecast(api_query, target_date, display_name)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, KeyError):
            # Lỗi mạng / API → để None để rơi xuống fallback
            return None

    def _fetch_current(self, api_query: str, display_name: Optional[str]) -> Optional[dict]:
        params = urllib.parse.urlencode({"q": api_query, "appid": self.api_key})
        url = f"{OPENWEATHER_BASE_URL}/weather?{params}"

        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        return self._normalize_api_response(payload, display_name)

    def _fetch_forecast(self, api_query: str, target_date: datetime, display_name: Optional[str]) -> Optional[dict]:
        params = urllib.parse.urlencode({"q": api_query, "appid": self.api_key})
        url = f"{OPENWEATHER_BASE_URL}/forecast?{params}"

        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

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

        city_info = payload.get("city", {})
        return self._normalize_api_response({
            **best,
            "name": city_info.get("name", api_query),
            "id": city_info.get("id", 0),
            "sys": {"country": city_info.get("country", "")},
            "coord": city_info.get("coord", {}),
        }, display_name)

    @staticmethod
    def _normalize_api_response(payload: dict, display_name: Optional[str] = None) -> dict:
        """Chuyển API response sang format giống weather_data.json."""
        # Ưu tiên display_name override → fallback về tên API trả về
        api_name = payload.get("name", "")
        final_name = display_name or api_name

        return {
            "city": {
                "id": payload.get("id", 0),
                "name": final_name,
                "findname": final_name.upper(),
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

    # ── FALLBACK ─────────────────────────────────────────────────────────
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