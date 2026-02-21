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

logger = logging.getLogger('home_display.weather')


class Weather(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.service_key = os.getenv('KMA_API_KEY')
        if not self.service_key:
            logger.error('KMA_API_KEY not found in environment variables')
            raise ValueError('KMA_API_KEY is required')
        
        self.val = {
            'T1H': 0.0, 'REH': 0, 'RN1': 0, 'SKY': 0, 'UUU': 0.0,
            'VVV': 0.0, 'PTY': 0, 'LGT': 0, 'VEC': 0, 'WSD': 0.0,
            'is_valid': False
        }
        self.max_conn_trials = 15
        
        # Get grid coordinates from env
        self.nx = int(os.getenv('WEATHER_GRID_NX', '67'))
        self.ny = int(os.getenv('WEATHER_GRID_NY', '101'))
        
        self.count = 0
        self.interval = 300  # Update every 5 minutes
        global_vars.weather_val = self.val

    def run(self):
        logger.info('Weather thread started')
        while global_vars.is_thread_continued:
            if not self.val['is_valid'] or self.count % self.interval == 0:
                if global_vars.weather_conn_trials < self.max_conn_trials:
                    self.val = self.update_short_term_weather(self)
                elif global_vars.weather_conn_trials == self.max_conn_trials:
                    logger.warning('Weather: Max connection trials reached, waiting for next reset')
                    global_vars.weather_conn_trials += 1

                if self.val["is_valid"]:
                    logger.debug('Weather data updated successfully')
                    global_vars.weather_conn_trials = 0
                    global_vars.weather_val = self.val
                    global_vars.weather_val_lgt = self.val['LGT']
                else:
                    global_vars.is_weather_valid = False
                    global_vars.weather_conn_trials += 1
                    
            self.count += 1
            time.sleep(1.0)
        
        logger.info('Weather thread stopped')

    @staticmethod
    def update_short_term_weather(param):
        """Update short-term weather information"""
        try:
            curr_time = time.time()
            curr_tm = time.localtime(curr_time)

            # Weather status - available 40 minutes after the hour
            base_tm0 = time.localtime(curr_time - 3600) if curr_tm.tm_min <= 40 else curr_tm

            # Weather forecast - available 45 minutes after the hour
            base_tm1 = time.localtime(curr_time - 3600) if curr_tm.tm_min <= 45 else curr_tm

            base_date0 = f'{base_tm0.tm_year:04d}{base_tm0.tm_mon:02d}{base_tm0.tm_mday:02d}'
            base_time0 = f'{base_tm0.tm_hour:02d}00'
            base_date1 = f'{base_tm1.tm_year:04d}{base_tm1.tm_mon:02d}{base_tm1.tm_mday:02d}'
            base_time1 = f'{base_tm1.tm_hour:02d}00'

            # Ultra short-term status (actual observations)
            url0 = (f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
                   f'?ServiceKey={param.service_key}'
                   f'&base_date={base_date0}&base_time={base_time0}'
                   f'&nx={param.nx}&ny={param.ny}'
                   f'&pageNo=1&numOfRows=10&dataType=JSON')

            # Ultra short-term forecast
            url1 = (f'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
                   f'?ServiceKey={param.service_key}'
                   f'&base_date={base_date1}&base_time={base_time1}'
                   f'&nx={param.nx}&ny={param.ny}'
                   f'&pageNo=1&numOfRows=10&dataType=JSON')

            logger.debug(f'Fetching weather data: {base_date0} {base_time0}')

            with urllib.request.urlopen(url0, timeout=10) as request0:
                response0 = json.loads(request0.read().decode('utf-8'))
            
            with urllib.request.urlopen(url1, timeout=10) as request1:
                response1 = json.loads(request1.read().decode('utf-8'))

            # Parse response
            for key in param.val.keys():
                if key in ['T1H', 'UUU', 'VVV', 'WSD']:
                    for item in response0["response"]["body"]["items"]["item"]:
                        if item["category"] == key:
                            param.val[key] = float(item["obsrValue"])
                            break
                elif key in ['SKY', 'LGT']:  # Forecast values
                    for item in response1["response"]["body"]["items"]["item"]:
                        if item["category"] == key:
                            param.val[key] = int(float(item["fcstValue"]))
                            break
                elif key == 'is_valid':
                    param.val[key] = True
                else:  # Status values
                    for item in response0["response"]["body"]["items"]["item"]:
                        if item["category"] == key:
                            param.val[key] = int(float(item["obsrValue"]))
                            break
            
            logger.info(f'Weather updated: Temp={param.val["T1H"]}°C, '
                       f'Humidity={param.val["REH"]}%, Sky={param.val["SKY"]}')
            return param.val

        except urllib.error.URLError as e:
            logger.error(f'Network error fetching weather: {e}')
            param.val['is_valid'] = False
            return param.val
        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error in weather response: {e}')
            param.val['is_valid'] = False
            return param.val
        except Exception as e:
            logger.error(f'Failed to get short-term weather: {e}')
            param.val['is_valid'] = False
            return param.val
