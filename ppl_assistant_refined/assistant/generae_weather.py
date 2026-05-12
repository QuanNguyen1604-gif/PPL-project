"""
Generate weather_data.json đúng format code yêu cầu:
{
  "DD/MM/YYYY": [
    { city, main, weather, wind, clouds },
    ...
  ]
}

5 thành phố Việt Nam × 60 ngày từ 07/05/2026.
Khí hậu phù hợp VN tháng 5-7 (đầu hè): nóng ẩm, mưa rào.
"""
import json
import random
from datetime import datetime, timedelta

TODAY = datetime(2026, 5, 7)
NUM_DAYS = 60

# 5 thành phố lớn VN với toạ độ thật
CITIES = [
    {
        "id": 1581130,
        "name": "Hanoi",
        "findname": "HANOI",
        "country": "VN",
        "coord": {"lon": 105.840836, "lat": 21.024357},
        "zoom": 7,
    },
    {
        "id": 1566083,
        "name": "Ho Chi Minh City",
        "findname": "HO CHI MINH CITY",
        "country": "VN",
        "coord": {"lon": 106.629662, "lat": 10.822891},
        "zoom": 7,
    },
    {
        "id": 1583992,
        "name": "Da Nang",
        "findname": "DA NANG",
        "country": "VN",
        "coord": {"lon": 108.220833, "lat": 16.06778},
        "zoom": 8,
    },
    {
        "id": 1581298,
        "name": "Hai Phong",
        "findname": "HAI PHONG",
        "country": "VN",
        "coord": {"lon": 106.683334, "lat": 20.866667},
        "zoom": 8,
    },
    {
        "id": 1586203,
        "name": "Can Tho",
        "findname": "CAN THO",
        "country": "VN",
        "coord": {"lon": 105.78306, "lat": 10.03278},
        "zoom": 8,
    },
]

# Trạng thái thời tiết VN mùa hè (xác suất khác nhau)
# (id, main, description, icon, weight)
WEATHER_TYPES = [
    (800, "Clear",   "clear sky",          "01d", 15),  # nắng đẹp
    (801, "Clouds",  "few clouds",         "02d", 20),  # ít mây
    (802, "Clouds",  "scattered clouds",   "03d", 18),  # nhiều mây
    (803, "Clouds",  "broken clouds",      "04d", 12),  # mây dày
    (500, "Rain",    "light rain",         "10d", 15),  # mưa nhẹ
    (501, "Rain",    "moderate rain",      "10d", 10),  # mưa rào
    (502, "Rain",    "heavy intensity rain","10d", 5),  # mưa to
    (200, "Thunderstorm", "thunderstorm",  "11d", 5),   # giông
]

# Khí hậu khác nhau giữa các vùng (nhiệt độ tham chiếu, °C)
CITY_CLIMATE = {
    "Hanoi":            {"temp_base": 30, "temp_var": 4, "humidity_base": 75},
    "Ho Chi Minh City": {"temp_base": 32, "temp_var": 3, "humidity_base": 80},
    "Da Nang":          {"temp_base": 31, "temp_var": 3, "humidity_base": 78},
    "Hai Phong":        {"temp_base": 29, "temp_var": 4, "humidity_base": 78},
    "Can Tho":          {"temp_base": 32, "temp_var": 2, "humidity_base": 82},
}


def kelvin(celsius):
    """°C → Kelvin (giống format OpenWeather API)."""
    return round(celsius + 273.15, 2)


def random_weather_type():
    """Pick weather type theo trọng số."""
    types = [w for w in WEATHER_TYPES]
    weights = [w[4] for w in WEATHER_TYPES]
    chosen = random.choices(types, weights=weights, k=1)[0]
    return {
        "id": chosen[0],
        "main": chosen[1],
        "description": chosen[2],
        "icon": chosen[3],
    }


def generate_city_weather(city, date_obj):
    """Tạo entry weather cho 1 city tại 1 ngày."""
    climate = CITY_CLIMATE[city["name"]]
    weather = random_weather_type()

    # Nhiệt độ random theo climate
    base = climate["temp_base"]
    var = climate["temp_var"]
    temp_c = base + random.uniform(-var, var)

    # Nếu mưa thì mát hơn 2-4°C
    if weather["main"] in ("Rain", "Thunderstorm"):
        temp_c -= random.uniform(2, 4)

    temp_min_c = temp_c - random.uniform(1, 3)
    temp_max_c = temp_c + random.uniform(1, 3)

    # Độ ẩm cao hơn khi mưa
    humidity = climate["humidity_base"] + random.randint(-10, 10)
    if weather["main"] in ("Rain", "Thunderstorm"):
        humidity = min(humidity + random.randint(5, 15), 100)
    humidity = max(40, min(100, humidity))

    # Wind
    wind_speed = round(random.uniform(1.5, 7.5), 2)
    wind_deg = random.randint(0, 359)

    # Clouds %
    if weather["main"] == "Clear":
        clouds = random.randint(0, 15)
    elif weather["main"] == "Clouds":
        clouds = random.randint(30, 90)
    else:
        clouds = random.randint(70, 100)

    entry = {
        "city": city,
        "time": int(date_obj.timestamp()),
        "main": {
            "temp": kelvin(temp_c),
            "pressure": random.randint(1008, 1018),
            "humidity": humidity,
            "temp_min": kelvin(temp_min_c),
            "temp_max": kelvin(temp_max_c),
        },
        "wind": {"speed": wind_speed, "deg": wind_deg},
        "clouds": {"all": clouds},
        "weather": [weather],
    }

    # Nếu có mưa, thêm field rain (giống format OpenWeather)
    if weather["main"] == "Rain":
        entry["rain"] = {"3h": round(random.uniform(0.3, 5.0), 2)}
    elif weather["main"] == "Thunderstorm":
        entry["rain"] = {"3h": round(random.uniform(3.0, 15.0), 2)}

    return entry


def main():
    random.seed(42)
    output = {}

    for i in range(NUM_DAYS):
        date_obj = TODAY + timedelta(days=i)
        date_key = date_obj.strftime("%d/%m/%Y")
        day_entries = []
        for city in CITIES:
            day_entries.append(generate_city_weather(city, date_obj))
        output[date_key] = day_entries

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Generated weather for {NUM_DAYS} days × {len(CITIES)} cities")
    print(f"Total entries: {NUM_DAYS * len(CITIES)}")
    print(f"Date range: {TODAY.strftime('%d/%m/%Y')} → "
          f"{(TODAY + timedelta(days=NUM_DAYS-1)).strftime('%d/%m/%Y')}")
    print(f"Saved to weather_data.json")


if __name__ == "__main__":
    main()