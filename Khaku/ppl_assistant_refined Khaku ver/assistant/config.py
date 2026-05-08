import os
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = PACKAGE_DIR.parent
DATA_DIR = PROJECT_DIR / 'data'
GRAMMAR_FILE = PROJECT_DIR / 'Cfg.g4'
GENERATED_DIR = PACKAGE_DIR / 'generated'

CALENDAR_FILE = DATA_DIR / 'Data_Calendar.json'
POMODORO_FILE = DATA_DIR / 'Data_Pomodoro.json'
RESPONSE_FILE = DATA_DIR / 'Data_Response.json'
TEMP_FILE = DATA_DIR / 'Data_temp.json'
WEATHER_FILE = DATA_DIR / 'Mock_weather_data.json'

# --- OpenWeatherMap API configuration ---
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
USE_LIVE_API = bool(OPENWEATHER_API_KEY)
