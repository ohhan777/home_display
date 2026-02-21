import threading
import urllib.request
import json
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import global_vars

# Load environment variables
load_dotenv('/home/pi/home_display/.env')

logger = logging.getLogger('home_display.weather_forecast')


class WeatherForecast(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.service_key = os.getenv('KMA_API_KEY')
        if not self.service_key:
            logger.error('KMA_API_KEY not found in environment variables')
            raise ValueError('KMA_API_KEY is required')
        
        self.val = {
            'POP': {}, 'PTY': {}, 'R06': {}, 'REH': {}, 'S06': {},
            'SKY': {}, 'T3H': {}, 'WAV': {}, 'UUU': {}, 'VEC': {},
            'VVV': {}, 'WSD': {}, 'TMN': {}, 'TMX': {}, 'is_valid': False
        }
        self.max_conn_trials = 10
        
        # Get grid coordinates from env
        self.nx = int(os.getenv('WEATHER_GRID_NX', '67'))
        self.ny = int(os.getenv('WEATHER_GRID_NY', '101'))
        
        self.count = 0
        self.interval = 300  # Update every 5 minutes

    def run(self):
        logger.info('Weather Forecast thread started')
        while global_vars.is_thread_continued:
            if not self.val['is_valid'] or self.count % self.interval == 0:
                if global_vars.weather_forecast_conn_trials < self.max_conn_trials:
                    self.val = self.update_weather_forecast(self)
                elif global_vars.weather_forecast_conn_trials == self.max_conn_trials:
                    logger.warning('Weather forecast: Max connection trials reached')
                    global_vars.weather_forecast_conn_trials += 1

                if self.val["is_valid"]:
                    global_vars.weather_forecast_conn_trials = 0
                    global_vars.weather_forecast_val = self.val
                    logger.debug('Weather forecast updated successfully')
                else:
                    global_vars.is_weather_forecast_valid = False
                    global_vars.weather_forecast_conn_trials += 1

            self.count += 1
            time.sleep(1.0)
        
        logger.info('Weather Forecast thread stopped')

    @staticmethod
    def update_weather_forecast(param):
        """Update weather forecast information"""
        try:
            curr_time = time.time()
            base_t = curr_time
            base_tm = time.localtime(base_t)
            
            # Adjust base time based on when data is available
            if base_tm.tm_min <= 30:
                base_t -= 3600
            
            base_tm = time.localtime(base_t)
            hour = base_tm.tm_hour

            # API provides data every 3 hours
            if hour in [0, 3, 6, 9, 12, 15, 18, 21]:
                base_t -= 3600
            elif hour in [1, 4, 7, 10, 13, 16, 19, 22]:
                base_t -= 7200

            base_tm = time.localtime(base_t)
            base_date = f'{base_tm.tm_year:04d}{base_tm.tm_mon:02d}{base_tm.tm_mday:02d}'
            base_time = f'{base_tm.tm_hour:02d}00'

            url = (f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
                  f'?ServiceKey={param.service_key}'
                  f'&base_date={base_date}&base_time={base_time}'
                  f'&nx={param.nx}&ny={param.ny}'
                  f'&pageNo=1&numOfRows=200&dataType=JSON')

            logger.debug(f'Fetching weather forecast: {base_date} {base_time}')

            with urllib.request.urlopen(url, timeout=10) as request:
                response = json.loads(request.read().decode('utf-8'))

            # Convert to numeric for easier calculation
            base_date_num = base_tm.tm_year * 10000 + base_tm.tm_mon * 100 + base_tm.tm_mday
            base_time_num = base_tm.tm_hour * 100 + 400  # 4 hours ahead

            while True:
                if base_time_num == 2400:
                    base_t += 86400  # Add one day
                    base_tm = time.localtime(base_t)
                    base_date_num = base_tm.tm_year * 10000 + base_tm.tm_mon * 100 + base_tm.tm_mday
                    base_time_num = 0

                pop = param.get_value(response, base_date_num, base_time_num, 'POP')
                if pop is None:  # No more data
                    break
                
                # Parse all weather parameters
                for key in param.val.keys():
                    if key in ['POP', 'PTY', 'REH', 'S06', 'SKY', 'T3H', 'VEC', 'WAV']:
                        val = param.get_value(response, base_date_num, base_time_num, key)
                        if val is not None:
                            param.val[key][f"{base_date_num:08d}{base_time_num:04d}"] = int(float(val))
                    elif key in ['R06', 'UUU', 'VVV', 'WSD', 'TMN', 'TMX']:
                        val = param.get_value(response, base_date_num, base_time_num, key)
                        if val is not None:
                            param.val[key][f"{base_date_num:08d}{base_time_num:04d}"] = float(val)
                
                base_time_num += 300  # Next 3-hour interval

            param.val['is_valid'] = True
            logger.info('Weather forecast updated successfully')
            return param.val

        except urllib.error.URLError as e:
            logger.error(f'Network error fetching weather forecast: {e}')
            param.val['is_valid'] = False
            return param.val
        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error in weather forecast: {e}')
            param.val['is_valid'] = False
            return param.val
        except Exception as e:
            logger.error(f'Failed to get weather forecast: {e}')
            param.val['is_valid'] = False
            return param.val

    @staticmethod
    def get_value(response, f_date, f_time, category):
        """Extract specific value from weather forecast response"""
        f_date_str = str(f_date)
        f_time_str = f"{f_time:04d}"
        
        try:
            for item in response['response']["body"]["items"]["item"]:
                if (item["category"] == category and 
                    item["fcstTime"] == f_time_str and 
                    item["fcstDate"] == f_date_str):
                    return item["fcstValue"]
        except (KeyError, TypeError):
            pass
        return None


if __name__ == '__main__':
    weather_forecast_th = WeatherForecast()
    weather_forecast_th.start()
    weather_forecast_th.join()
