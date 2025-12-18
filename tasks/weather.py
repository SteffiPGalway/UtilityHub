import requests

def get_weather(api_key, city):
    """Fetch weather data for a given city using OpenWeatherMap API.
    Args:
        api_key (str): OpenWeatherMap API key   
        city (str): City name
    Returns:
        tuple: (temperature (°C), weather description, humidity (%))
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    response = response.json()
    temp = response['main']['temp']
    weather_description = response['weather'][0]['description']
    humidity = response['main']['humidity']
    return temp, weather_description, humidity
