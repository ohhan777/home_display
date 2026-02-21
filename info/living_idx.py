import threading
import urllib.request
import json
import time
import global_vars
from datetime import datetime


class LivingIdx(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.service_key = 'R9%2F1qr2soj0pNReafYodqrc48suo%2FqPNTBa85r2PFlToOcZ3INOTHGYRcjZRzQNZj6qGI8IjhFdPGoSOZBtvDQ%3D%3D'
        self.area_no = '3020055000' # Sinseong-dong, Yuseong-gu, Daejeon
        # services = ['WindChillIdx', 'DiscomfortIdx', 'FreezeIdx', 'UVIdx', 'AirDiffusionIdx', 'HeatFeelingIdx']
        services = ['UVIdx']
        self.val = {}
        for s in services:
            self.val[s] = {}
        self.max_conn_trials = 5
        # current position
        self.nx, self.ny = 67, 101
        self.count = 0
        self.interval = 1200

    def run(self):
        while global_vars.is_thread_continued:
            if self.val['is_valid'] == False or self.count % self.interval == 0:
                if global_vars.living_idx_conn_trials < self.max_conn_trials:
                    # update living index via Internet
                    self.val = self.update_living_idx(self)
                elif global_vars.living_idx_conn_trials == self.max_conn_trials:
                    now = datetime.now()
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    print("[%s](Short-term weather info) Internet connection failed..." % date_time)
                    print("Wait until the next init....")
                    global_vars.living_idx_conn_trials += 1
                else:
                    global_vars.living_idx_conn_trials += 1

                if self.val["is_valid"] is not False:
                    print('l', end='')
                    global_vars.living_idx_conn_trials = 0
                    global_vars.living_idx_val = self.val
                    print('ok..living idx')
                    # print(time.strftime("%m/%d/%Y, %H:%M:%S", recent_data_tm))
                    # print('Fine Dust: ' + str(global_vars.fine_dust))
                    # print('Very Fine Dust: ' + str(global_vars.very_fine_dust))
                else:  # connection failed
                    global_vars.is_living_idx_valid = False
                    global_vars.living_idx_conn_trials += 1

            self.count += 1
            time.sleep(1.0)

    @staticmethod
    def update_living_idx(param):
        curr_time = time.time()
        curr_tm = time.localtime(curr_time)

        # weather status
        if (curr_tm.tm_min <= 40):
            base_tm = time.localtime(curr_time - 60 * 60)
        else:
            base_tm = time.localtime(curr_time)

        base_datetime = '{:04d}{:02d}{:02d}{:02d}'.format(base_tm.tm_year, base_tm.tm_mon,
                                                          base_tm.tm_mday, base_tm.tm_hour)

        try:
            for key in param.val.keys():
                url = 'http://apis.data.go.kr/1360000/LivingWthrIdxService/get' + key \
                      + '?ServiceKey=' + param.service_key + '&time=' + base_datetime + '&areaNo=' + param.area_no \
                      + '&pageNo=1&numOfRows=100&dataType=JSON'
                print(url)

                request = urllib.request.urlopen(url)
                response = request.read().decode('utf-8')
                response = json.loads(response)
                param.val[key] = response['response']['body']['items']['item'][0]


            param.val['is_valid'] = True
            return param.val

        except:
            print('Failed to get short-term weather status')
            param.val['is_valid'] = False
            return param.val



if __name__ == '__main__':
    living_idx_th = LivingIdx()
    living_idx_th.start()
    living_idx_th.join()

