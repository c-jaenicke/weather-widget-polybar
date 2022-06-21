import requests
from sys import argv
import datetime

# set api key
APIkey = "KEY HERE"

def geocoding():
    """OpenWeatherMap geocoding api to get coordinates of the location
    https://openweathermap.org/api/geocoding-api

    Returns:
        lat, lon: coordinates of location as float
    
    Raise:
        if location argument is missing, as IndexError
        if HTTP request fails, as HTTPError
    """
    # try if location argument is there    
    try:
       location = argv[2]
    except:
        print("Err: Missing location")
        raise IndexError

    # http://api.openweathermap.org/geo/1.0/direct?q={city name},{state code},{country code}&limit={limit}&appid={API key}
    url = "http://api.openweathermap.org/geo/1.0/direct?q={0}&limit=1&appid={1}".format(location, APIkey)    

    try:
        resp = requests.get(url)
        data = resp.json()
        lat = str(data[0]["lat"])
        lon = str(data[0]["lon"])
        return lat, lon
    except requests.exceptions.HTTPError as error:
        print("Err: geocoding failed")
        raise

def get_weather_data():
    """Get weather data from request

    Return:
        data: json containing all data from request    
    
    Raise:
        if HTTP request fails, as HTTPError
    """
    # get lat and lon coordinates
    lat, lon = geocoding()

    # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    # optional used &units=metric
    # url = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units=metric".format(lat, lon, APIkey)

    # https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API key}
    # using onecall api, but version 2.5 since 3.0 needs billing data
    url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=minutely,daily,alerts&appid={}&units=metric".format(lat, lon, APIkey)

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data
    except requests.exceptions.HTTPError as error:
        print("Err: getting data failed")
        raise

def weather_small():
    """Print small weather data, used for module in bar
    """
    data = get_weather_data()
    weather = str(data["current"]["weather"][0]["description"])
    temp = str(data["current"]["temp"])
    print(temp + "°C " + weather)

def weather_full():
    """Print full weather data from time of request
    """
    data = get_weather_data()

    time = convert_time(int(data["current"]["dt"]))
    weather = str(data["current"]["weather"][0]["main"])
    weather_desc = str(data["current"]["weather"][0]["description"])
    temp = str(data["current"]["temp"])
    humidity = str(data["current"]["humidity"])
    pressure = str(data["current"]["pressure"])
    wind_speed = str(data["current"]["wind_speed"])
    wind_deg = str(data["current"]["wind_deg"])
    # TODO turn wind degrees into real direction

    print("""Current Weather {0}-UTC :
    {1}, {2}
    Current temp: {3}°C
    Humidity: {4}%
    Pressure: {5} hPa
    Wind:
        Speed: {6} m/s
        Direction: {7}
    """.format(
        time,
        weather,
        weather_desc,
        temp,
        humidity,
        pressure,
        wind_speed,
        wind_deg
    ))

def get_forecast():
    """Print full forecast for the coming 12 hours
    """
    data = get_weather_data()
    forecastString = "Forecast: "
    i = 0

    for entry in data["hourly"]:
        if i == 12:
            break
        i = i + 1
        tempString = """\nTime {0}-UTC:
        Weather:
            {1}, {2}
        Temperature: {3}°C
        Humidity: {4}%
        Pressure: {5} hPa
        Wind:
            Speed: {6} m/s
            Direction: {7}
        """.format(
            convert_time(entry["dt"]),
            str(entry["weather"][0]["main"]),
            str(entry["weather"][0]["description"]),
            str(entry["temp"]),
            str(entry["humidity"]),
            str(entry["pressure"]),
            str(entry["wind_speed"]),
            str(entry["wind_deg"]),
        )   
        forecastString = forecastString + tempString

    print(forecastString)

def convert_time(utime):
    """Convert linux time string to utc time

    Args:
        utime: unix time string, taken from weather api request data

    Returns:
        utc time string, format as Hour:Minutes
    """
    return datetime.datetime.utcfromtimestamp(utime).strftime("%H:%M")

if __name__ == "__main__":
    arguments = argv
    
    # do some lidl argument parsing
    if arguments[1] == "help":
        print("weather.py <operation> <location>\nOperations: small: current temp and weather; full: current and forecast for few hours, opens in terminal")
    elif arguments[1] == "small":
        weather_small()
    elif arguments[1] == "full":
        weather_full()
        get_forecast()
    else:
        print("weather.py <operation> <location>\nOperations: small: current temp and weather; full: current and forecast for few hours, opens in terminal")
