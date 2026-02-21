import os
os.nice(17)
from info import air_dust, weather, weather_forecast, sun_moon, smartthings
import gui_main

if __name__ == '__main__':
    # indoor_sensor_th = indoor_sensor_ble.IndoorSensorBle()
    smartthings_th = smartthings.Smartthings()
    air_dust_th = air_dust.AirDust()
    weather_th = weather.Weather()
    weather_forecast_th = weather_forecast.WeatherForecast()
    sun_moon_th = sun_moon.SunMoon()

    # indoor_sensor_th.start()
    smartthings_th.start()
    air_dust_th.start()
    weather_th.start()
    weather_forecast_th.start()
    sun_moon_th.start()

    gui = gui_main.GuiMain()
    gui.Go()

    # indoor_sensor_th.join()
    smartthings_th.join()
    air_dust_th.join()
    weather_th.join()
    weather_forecast_th.join()
    sun_moon_th.join()

    print('Exit')
