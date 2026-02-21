import threading
import urllib.request
import urllib.parse
import json
import time
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
import global_vars

# Load environment variables
load_dotenv('/home/pi/home_display/.env')

logger = logging.getLogger('home_display.air_dust')


class AirDust(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.service_key = os.getenv('KMA_API_KEY')
        if not self.service_key:
            logger.error('KMA_API_KEY not found in environment variables')
            raise ValueError('KMA_API_KEY is required')
        
        self.station_name = os.getenv('AIR_QUALITY_STATION', '노은동')
        
        self.val = {
            'dataTime': 0, "so2Value": 0.0, "coValue": 0.0, "o3Value": 0.0,
            "no2Value": 0.0, "pm10Value": 0, "pm10Value24": 0, "pm25Value": 0,
            "pm25Value24": 0, "khaiValue": 0, "khaiGrade": 0, "so2Grade": 0,
            "coGrade": 0, "o3Grade": 0, "no2Grade": 0, "pm10Grade": 0,
            "pm25Grade": 0, "pm10Grade1h": 0, "pm25Grade1h": 0, "is_valid": False
        }
        self.max_conn_trials = 5
        self.count = 0
        self.interval = 900  # Update every 15 minutes

    def run(self):
        logger.info('Air Dust thread started')
        while global_vars.is_thread_continued:
            if not self.val['is_valid'] or self.count % self.interval == 0:
                if global_vars.air_dust_conn_trials < self.max_conn_trials:
                    logger.debug(f'Air dust connection attempt {global_vars.air_dust_conn_trials + 1}')
                    self.val = self.update_air_dust(self)
                elif global_vars.air_dust_conn_trials == self.max_conn_trials:
                    logger.warning('Air dust: Max connection trials reached')
                    global_vars.air_dust_conn_trials += 1

                if self.val["is_valid"]:
                    logger.info(f'Air dust updated: PM10={self.val["pm10Value"]}, '
                              f'PM2.5={self.val["pm25Value"]}')
                    global_vars.is_air_dust_valid = True
                    global_vars.air_dust_conn_trials = 0
                    global_vars.fine_dust = self.val["pm10Value"]
                    global_vars.very_fine_dust = self.val["pm25Value"]
                else:
                    global_vars.is_air_dust_valid = False
                    global_vars.air_dust_conn_trials += 1
                    self.count = 0
                    
            self.count += 1
            time.sleep(1.0)
        
        logger.info('Air Dust thread stopped')

    @staticmethod
    def update_air_dust(param):
        """Update air quality information"""
        try:
            url_station_name = urllib.parse.quote_plus(param.station_name)
            url = (f'http://openapi.airkorea.or.kr/openapi/services/rest/'
                  f'ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
                  f'?stationName={url_station_name}'
                  f'&ver=1.3&dataTerm=month&pageNo=1&numOfRows=10'
                  f'&serviceKey={param.service_key}&_returnType=json')
            
            with urllib.request.urlopen(url, timeout=10) as request:
                response = json.loads(request.read().decode('utf-8'))
            
            # Parse response
            for key in param.val.keys():
                if key == 'dataTime':
                    str_time = response["list"][0][key]
                    tm = time.strptime(str_time, "%Y-%m-%d %H:%M")
                    param.val[key] = time.mktime(tm)
                elif key in ['so2Value', 'coValue', 'o3Value', 'no2Value']:
                    param.val[key] = float(response["list"][0][key])
                elif key == 'is_valid':
                    param.val[key] = True
                else:
                    param.val[key] = int(response["list"][0][key])
            
            return param.val

        except urllib.error.URLError as e:
            logger.error(f'Network error fetching air quality: {e}')
            param.val["is_valid"] = False
            return param.val
        except (KeyError, IndexError) as e:
            logger.error(f'Invalid air quality data format: {e}')
            param.val["is_valid"] = False
            return param.val
        except Exception as e:
            logger.error(f"Failed to get air dust info: {e}")
            param.val["is_valid"] = False
            return param.val
