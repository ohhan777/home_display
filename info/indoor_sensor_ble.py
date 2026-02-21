import os
import threading
from bluepy.btle import UUID, Peripheral, BTLEException
import struct
import time
import global_vars
from datetime import datetime


class IndoorSensorBle(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sensor_service_uuid = "19b10000-e8f2-537e-4f6c-d104768a8918"
        self.val = {'temp': 0.0, 'humid': 0.0, 'voc': 0, 'co2': 0, 'lux': 0, 'dust': 0.0, 'is_valid': False}
        self.ch = None
        self.max_conn_trials = 10
        global_vars.indoor_val = self.val

    def run(self):
        while global_vars.is_thread_continued:
            if global_vars.is_ble_conn is False:
                if global_vars.ble_conn_trials < self.max_conn_trials:
                    now = datetime.now()
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    print('[%s] BLE connection attempt %d...' % (date_time, global_vars.ble_conn_trials))
                    self.ch = self.connect(self)
                elif global_vars.ble_conn_trials == self.max_conn_trials:
                    now = datetime.now()
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    print("[%s] BLE connection failed..." % date_time)
                    print("Wait until the next init....")
                    global_vars.ble_conn_trials += 1
                else:
                    global_vars.ble_conn_trials += 1

            if self.ch is not None:
                global_vars.is_ble_conn = True
                global_vars.ble_conn_trials = 0
                self.val = self.get_values(self)
                if self.val['is_valid']:
                    print('b', end='')
                    global_vars.indoor_val = self.val
                    now = datetime.now()
                    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    # print('[%s] temp=%.1f, humid=%.1f, lux=%g, dust=%.1f'
                    #       % (date_time, global_vars.indoor_val['temp'], global_vars.indoor_val['humid'],
                    #          global_vars.indoor_val['lux'], global_vars.indoor_val['dust']))
                    # os.system("vcgencmd measure_temp | egrep -o \'[0-9]*\.[0-9]*\'")
                else:
                    global_vars.is_ble_conn = False
                    self.ch = None
            else:   # connection failed
                global_vars.is_ble_conn = False
                global_vars.ble_conn_trials += 1

            time.sleep(1.0)

    @staticmethod
    def connect(param):
        try:
            p = Peripheral("98:4F:EE:0F:B5:7D", "public")
            service = p.getServiceByUUID(param.sensor_service_uuid)
            ch = service.getCharacteristics()[0]
            return ch
        except:
            print("Failed to connect to peripheral")
            return None

    @staticmethod
    def get_values(param):
        try:
            val = struct.unpack('<hhhhhih', param.ch.read())
            param.val['temp'] = val[0] / 100.0 - 2.7
            param.val['humid'] = min(val[1] / 100.0 + 2.3, 99.9)
            param.val['voc'] = val[2]
            param.val['co2'] = val[3]
            param.val['lux'] = val[4]
            param.val['dust'] = val[5] / 100.0
            param.val['is_valid'] = True
            return param.val
        except:
            param.val['is_valid'] = False
            return param.val
