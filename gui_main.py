from tkinter import *
import time
from gui_clocks.clocks import *
import global_vars
import os
import subprocess
import logging

logger = logging.getLogger('home_display.gui')

def mouse_click(event):
    """Handle mouse click to turn on display"""
    logger.info(f'Mouse clicked at ({event.x}, {event.y})')
    result = set_display_power(True)
    if result:
        global_vars.screen_on = True
        logger.info('Display turned on by mouse click')


def set_display_power(on: bool) -> bool:
    """
    Control display power with proper error handling
    Returns True if successful, False otherwise
    """
    command = f'vcgencmd display_power {1 if on else 0}'
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.info(f'Display power set to {"ON" if on else "OFF"}')
            return True
        else:
            logger.error(f'Failed to set display power: {result.stderr}')
            return False
    except subprocess.TimeoutExpired:
        logger.error('Display power command timed out')
        return False
    except Exception as e:
        logger.error(f'Error setting display power: {e}')
        return False


class GuiMain(Tk):
    w = 0
    h = 0
    curr_tm = time.localtime(time.time())
    last_display_check = 0
    display_check_interval = 1.0  # Check display state every second

    def __init__(self, *args, **kwargs):
        # Tkinter
        Tk.__init__(self, *args, **kwargs)
        self.attributes('-fullscreen', True)
        self.title("Home Display App")
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (self.w, self.h))
        self.focus_set()
        self.bind("<Button-1>", mouse_click)
        self.bind('<Escape>', lambda e: self.Destroy(self))

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Initialize screen as ON
        global_vars.screen_on = True
        set_display_power(True)
        logger.info('GUI initialized, display turned on')

        self.frames = {}
        for F in (OrigClock, NeoClock, RainClock, GraphicClock):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.ShowFrame("GraphicClock")

    def ShowFrame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def UpdateFrame(self, page_name):
        frame = self.frames[page_name]
        frame.Update()

    def Go(self):
        self.Update()
        self.mainloop()

    def Update(self):
        self.curr_tm = time.localtime(time.time())
        current_time = time.time()
        
        # Only check display state at intervals to reduce overhead
        if current_time - self.last_display_check >= self.display_check_interval:
            self.last_display_check = current_time
            self.check_display_state()

        # Reset connection trials hourly
        if self.curr_tm.tm_min == 0 and self.curr_tm.tm_sec == 0:
            global_vars.weather_conn_trials = 0
            global_vars.weather_forecast_conn_trials = 0
            global_vars.ble_conn_trials = 0
            global_vars.air_dust_conn_trials = 0
            global_vars.living_idx_conn_trials = 0

        # Update and show clock
        clock_name = 'GraphicClock'
        self.UpdateFrame(clock_name)
        self.ShowFrame(clock_name)

        # Calculate precise delay for next update
        curr_t = time.time()
        delay = (1 - curr_t + int(curr_t)) * 1000
        return self.after(int(delay) + 1, self.Update)

    def check_display_state(self):
        """Check if display should be on or off based on motion sensor"""
        # Determine if we're in working hours
        working_hour = self.is_working_hour()
        
        # Get motion timeout based on time of day
        delta_seconds = 900 if working_hour else 600
        
        # CRITICAL FIX: Check if smartthings data is valid before using it
        if not global_vars.smartthings_val.get('is_valid', False):
            logger.warning('SmartThings data not valid, keeping display on')
            if not global_vars.screen_on:
                if set_display_power(True):
                    global_vars.screen_on = True
            return
        
        last_motion = global_vars.smartthings_val.get('last_motion_time', 0)
        
        # CRITICAL FIX: If last_motion is 0 or None, treat as recent motion
        if last_motion == 0 or last_motion is None:
            logger.warning('No valid last_motion_time, treating as recent motion')
            time_since_motion = 0
        else:
            time_since_motion = time.time() - last_motion
        
        should_be_off = time_since_motion > delta_seconds
        
        # Log motion status periodically (every 60 seconds)
        if int(time.time()) % 60 == 0:
            logger.info(f'Motion status: last={time_since_motion:.0f}s ago, '
                       f'threshold={delta_seconds}s, screen={"ON" if global_vars.screen_on else "OFF"}')
        
        # Turn off screen if needed
        if global_vars.screen_on and should_be_off:
            logger.info(f'Turning display OFF (no motion for {time_since_motion:.0f}s)')
            if set_display_power(False):
                global_vars.screen_on = False
        
        # Turn on screen if needed
        elif not global_vars.screen_on and not should_be_off:
            logger.info(f'Turning display ON (motion detected {time_since_motion:.0f}s ago)')
            if set_display_power(True):
                global_vars.screen_on = True

    def is_working_hour(self) -> bool:
        """Determine if current time is within 'working hours' for display"""
        if self.curr_tm.tm_wday < 5:  # Weekdays (Mon-Fri)
            if 6 <= self.curr_tm.tm_hour <= 10:
                return True
            elif 16 <= self.curr_tm.tm_hour < 24:
                return True
        else:  # Weekends (Sat-Sun)
            if 6 <= self.curr_tm.tm_hour < 24:
                return True
        return False

    @staticmethod
    def Destroy(self):
        logger.info('Application terminating...')
        global_vars.is_thread_continued = False
        self.destroy()
