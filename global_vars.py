# -*- coding: utf-8 -*-
"""Global variables module with thread-safe access"""
import threading
import logging

# Thread safety lock
_lock = threading.RLock()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('/home/pi/home_display/home_display.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('home_display')

# App control
is_thread_continued = True
screen_on = False

# Indoor sensor (BLE - currently disabled)
is_ble_conn = False
ble_conn_trials = 0
indoor_val = {}

# SmartThings
smartthings_val = {
    'is_valid': False,
    'is_motion_detected': False,
    'living_room_temp': 0.0,
    'last_motion_time': 0.0
}

# Air dust
air_dust_conn_trials = 0
is_air_dust_valid = False
fine_dust = 0
very_fine_dust = 0
air_dust_val = {}

# Short-term weather
weather_conn_trials = 0
is_weather_valid = False
weather_val_lgt = 0
weather_val = {'is_valid': False, 'T1H': 0.0}

# Weather forecast
weather_forecast_conn_trials = 0
is_weather_forecast_valid = False
weather_forecast_val = {}

# Living index
living_idx_conn_trials = 0
is_living_idx_valid = False
living_idx_val = {}

# Sun and moon
sunrise_datetime = None
sunset_datetime = None


def get_value(key):
    """Thread-safe getter"""
    with _lock:
        return globals().get(key)


def set_value(key, value):
    """Thread-safe setter"""
    with _lock:
        globals()[key] = value


def update_dict(dict_name, updates):
    """Thread-safe dictionary update"""
    with _lock:
        target_dict = globals().get(dict_name)
        if isinstance(target_dict, dict):
            target_dict.update(updates)
