import threading
import ephem
import time
from datetime import timedelta, datetime
import ephem
import global_vars


class SunMoon(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.home = ephem.Observer()
        self.home.lat = '36:23.3'
        self.home.lon = '127:19.6'
        self.home.elev = 90
        self.val = {'sun_next_rise_datetime': 0, 'sun_next_set_datetime': 0,
                    'moon_next_rise_datetime': 0, 'moon_next_set_datetime': 0, 'moon_phase': 0.0,
                    'is_valid': False}
        self.count = 0
        self.interval = 3600

    def run(self):
        while global_vars.is_thread_continued:
            if self.val['is_valid'] == False or self.count % self.interval == 0:
                self.update_sun_moon_info(self)

                if self.val["is_valid"] is not False:
                    global_vars.sunrise_datetime = self.val["sun_next_rise_datetime"]
                    global_vars.sunset_datetime = self.val["sun_next_set_datetime"]
                    print('Sunrise: ' + global_vars.sunrise_datetime.strftime("%m/%d/%Y, %H:%M:%S"))
                    print('Sunset: ' + global_vars.sunset_datetime.strftime("%m/%d/%Y, %H:%M:%S"))

            self.count += 1
            time.sleep(1.0)

    @staticmethod
    def update_sun_moon_info(param):
        try:
            sun = ephem.Sun()
            moon = ephem.Moon()
            param.home.date = datetime.now()

            sun_next_rise = param.home.next_rising(sun)
            param.val['sun_next_rise_datetime'] = ephem.localtime(sun_next_rise)

            sun_next_set = param.home.next_setting(sun)
            param.val['sun_next_set_datetime'] = ephem.localtime(sun_next_set)

            moon_next_rise = param.home.next_rising(moon)
            param.val['moon_next_rise_datetime'] = ephem.localtime(moon_next_rise)

            moon_next_set = param.home.next_setting(moon)
            param.val['moon_next_set_datetime'] = ephem.localtime(moon_next_set)

            now = ephem.now()
            moon.compute(now)
            param.val['moon_phase'] = moon.phase        # 0: full, 1: no moon

            param.val['is_valid'] = True
            return param.val

        except:
            print("Failed to get sun and moon info")
            param.val["is_valid"] = False
            return param.val