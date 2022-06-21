# weather-widget

Weather widget for my Polybar setup. It uses the OpenWeatherMap API free tier.

Requires a OpenWeatherMap API Key, insert your key in line 6 ```python APIkey = "HERE"```

## Preview

Small in bar:

![Small](https://raw.githubusercontent.com/c-jaenicke/weather-widget-polybar/main/img/widget-small.png)

Full in terminal:

![Full](https://raw.githubusercontent.com/c-jaenicke/weather-widget-polybar/main/img/widget-full.png)

## Usage

```text
weather.py <full/small/help> <location>

help: prints arguments needed
small: only prints current temperature and weather
full: prints full weather report for now and 12 hour forecast

location: the location as one string, if more than one word, separate them with commas
```

To use it in polybar you need to make a custom module in your config, check the Polybar wiki on how to do that.
