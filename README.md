# weather-widget

Weather widget for my [Polybar](https://github.com/polybar/polybar) setup. It uses the OpenWeatherMap API free tier.

Requires a OpenWeatherMap API Key, insert your key in ```weather.py: line 6: APIkey = "KEY HERE"```

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

To use it in [Polybar](https://github.com/polybar/polybar) you need to make a custom module in your config, check the [Polybar](https://github.com/polybar/polybar) wiki on how to do that.

### Example Module

```text
[module/weather]
type = custom/script

exec = python <path to script> small <location>

; refresh every 30 minutes
interval = 1800.0

format =<label>
label =%output%

click-right = <Open new instance of your terminal without closing> python <path to script> full <location>
```
