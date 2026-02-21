import threading
import time
import logging
import os
from dotenv import load_dotenv
import aiohttp
import asyncio
import pysmartthings
import global_vars

# Load environment variables
load_dotenv('/home/pi/home_display/.env')

logger = logging.getLogger('home_display.smartthings')


class Smartthings(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.token = os.getenv('SMARTTHINGS_TOKEN')
        if not self.token:
            logger.error('SMARTTHINGS_TOKEN not found in environment variables')
            raise ValueError('SMARTTHINGS_TOKEN is required')
        
        self.device = None
        self.val = {
            'is_valid': False,
            'is_motion_detected': False,
            'living_room_temp': 0.0,
            'last_motion_time': time.time()  # Initialize to current time
        }
        global_vars.smartthings_val = self.val
        self.count = 0
        self.interval = 5
        self.consecutive_failures = 0
        self.max_failures = 10

    async def get_device(self):
        """Get SmartThings motion sensor device"""
        try:
            async with aiohttp.ClientSession() as session:
                api = pysmartthings.SmartThings(session, self.token)
                devices = await api.devices()
                for i, item in enumerate(devices):
                    logger.debug(f'Found device: {item.label}')
                    if item.label == 'Motion Sensor':
                        device = devices[i]
                        await device.status.refresh()
                        return device
                logger.error('Motion Sensor device not found')
                return None
        except Exception as e:
            logger.error(f'Error getting device list: {e}')
            return None

    def run(self):
        logger.info('SmartThings thread started')
        while global_vars.is_thread_continued:
            if not self.val['is_valid'] or self.count % self.interval == 0:
                self.update_smartthings_info(self)
                
                if self.val["is_valid"]:
                    global_vars.smartthings_val = self.val
                    self.consecutive_failures = 0
                else:
                    self.consecutive_failures += 1
                    if self.consecutive_failures >= self.max_failures:
                        logger.error(f'SmartThings connection failed {self.max_failures} times consecutively')
            
            self.count += 1
            time.sleep(1.0)
        
        logger.info('SmartThings thread stopped')

    @staticmethod
    def update_smartthings_info(param):
        """Update SmartThings sensor information"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            device = loop.run_until_complete(param.get_device())
            loop.close()
            
            if device is None:
                raise Exception('Device not available')
            
            param.val['is_motion_detected'] = device.status.motion
            if device.status.motion:
                param.val['last_motion_time'] = time.time()
                logger.info('Motion detected!')
            
            param.val['living_room_temp'] = device.status.temperature
            param.val['is_valid'] = True
            
            logger.debug(f'SmartThings update: motion={device.status.motion}, '
                        f'temp={device.status.temperature}°C')
            return param.val
            
        except Exception as e:
            logger.error(f"Failed to get SmartThings info: {e}")
            param.val["is_valid"] = False
            # Keep last_motion_time to prevent display issues
            return param.val
