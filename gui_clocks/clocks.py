from tkinter import *
import time
import global_vars
import os
import random




class OrigClock(Frame):
    # display
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.config(background='black', cursor='none')
        self.controller = controller
        self.controller.config(background='black', cursor='none')
        #self.bind("<Button-1>", lambda e: controller.ShowFrame("CurrInfoPage"))
        self.curr_tm = controller.curr_tm

        self.date_text = StringVar()
        self.time_text = StringVar()
        self.wday_text = StringVar()
        self.sec_text = StringVar()
        self.am_pm_text = StringVar()

        self.date_label = Label(self, textvariable=self.date_text, font=("넥슨 풋볼고딕 B", 75), foreground="white",
                                background="black")
        self.date_label.place(x=controller.w / 2 - 30, y=controller.h / 2 - 125, anchor=CENTER)

        self.wday_label = Label(self, textvariable=self.wday_text, font=("넥슨 풋볼고딕 B", 65), foreground="white",
                                background="black")
        self.wday_label.place(x=controller.w / 2 + 300, y=controller.h / 2 - 135, anchor=CENTER)

        self.time_label = Label(self, textvariable=self.time_text, font=("넥슨 풋볼고딕 B", 180), foreground="yellow",
                                background="black")
        self.time_label.place(x=controller.w / 2 - 80, y=controller.h / 2 + 60, anchor=CENTER)
        self.sec_label = Label(self, textvariable=self.sec_text, font=("넥슨 풋볼고딕 B", 85), foreground="yellow",
                               background="black")
        self.sec_label.place(x=controller.w / 2 + 235, y=controller.h / 2 - 70)

        self.am_pm_label = Label(self, textvariable=self.am_pm_text, font=("넥슨 풋볼고딕 B", 70), foreground="white",
                                 background="black")
        self.am_pm_label.place(x=controller.w / 2 + 220, y=controller.h / 2 + 40)

        self.Update()

    def Update(self):


        self.curr_tm = time.localtime(time.time())

        self.date_text.set(time.strftime("%Y/%m/%d", self.curr_tm))
        if (self.curr_tm.tm_wday == 0):
            self.wday_label.config(foreground='white')
            self.wday_text.set('월')
        elif (self.curr_tm.tm_wday == 1):
            self.wday_label.config(foreground='white')
            self.wday_text.set('화')
        elif (self.curr_tm.tm_wday == 2):
            self.wday_label.config(foreground='white')
            self.wday_text.set('수')
        elif (self.curr_tm.tm_wday == 3):
            self.wday_label.config(foreground='white')
            self.wday_text.set('목')
        elif (self.curr_tm.tm_wday == 4):
            self.wday_label.config(foreground='white')
            self.wday_text.set('금')
        elif (self.curr_tm.tm_wday == 5):
            self.wday_label.config(foreground='blue')
            self.wday_text.set('토')
        elif (self.curr_tm.tm_wday == 6):
            self.wday_label.config(foreground='red')
            self.wday_text.set('일')

        self.time_text.set(time.strftime("%I:%M", self.curr_tm))
        self.sec_text.set(time.strftime("%S", self.curr_tm))
        if (self.curr_tm.tm_hour >= 0 and self.curr_tm.tm_hour < 12):
            self.am_pm_text.set('오전')
        else:
            self.am_pm_text.set('오후')


class NeoClock(Frame):
    # display
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_color = '#49A'
        self.config(background=bg_color, cursor='none')
        self.controller = controller
        self.controller.config(background='black', cursor='none')

        self.curr_tm = controller.curr_tm

        self.month_abb = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        self.wday_abb = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.date_text = StringVar()
        self.time_text = StringVar()
        self.wday_text = StringVar()
        self.sec_text = StringVar()
        self.am_pm_text = StringVar()

        self.date_label = Label(self, textvariable=self.date_text, font=("Bauhaus", 50), foreground="white",
                                background=bg_color)
        self.date_label.place(x=controller.w / 2, y=controller.h / 2 - 135, anchor=CENTER)

        self.wday_label = Label(self, textvariable=self.wday_text, font=("Bauhaus", 50), foreground="white",
                                background=bg_color)
        self.wday_label.place(x=controller.w / 2, y=controller.h / 2 + 160, anchor=CENTER)

        self.time_label = Label(self, textvariable=self.time_text, font=("Bauhaus", 155), foreground="white",
                                background=bg_color)
        self.time_label.place(x=controller.w / 2, y=controller.h / 2 + 15, anchor=CENTER)
        # self.sec_label = Label(self, textvariable=self.sec_text, font=("Bauhaus", 85), foreground="white",
        #                        background=bg_color)
        # self.sec_label.place(x=controller.w / 2 + 235, y=controller.h / 2 - 70)

        # self.am_pm_label = Label(self, textvariable=self.am_pm_text, font=("Bauhaus", 50), foreground="white",
        #                          background=bg_color)
        # self.am_pm_label.place(x=controller.w / 2 - 350, y=controller.h / 2 - 120)

        self.Update()

    def Update(self):


        self.curr_tm = time.localtime(time.time())

        self.date_text.set(self.month_abb[self.curr_tm.tm_mon - 1] + " {}".format(self.curr_tm.tm_mday))
        self.wday_label.config(foreground='white')
        self.wday_text.set(self.wday_abb[self.curr_tm.tm_wday])

        self.time_text.set(time.strftime("%H:%M:%S", self.curr_tm))
        # self.sec_text.set(time.strftime("%S", self.curr_tm))
        # if (self.curr_tm.tm_hour >= 0 and self.curr_tm.tm_hour < 12):
        #     self.am_pm_text.set('am')
        # else:
        #     self.am_pm_text.set('pm')

class RainClock(Frame):
    # display
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_color = '#49A'
        self.config(background=bg_color, cursor='none')
        self.controller = controller
        self.controller.config(background='black', cursor='none')

        self.curr_tm = controller.curr_tm
        self.w = self.controller.w
        self.h = self.controller.h

        self.month_abb = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        self.wday_abb = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        self.canvas = Canvas(self, width=self.w, height=self.h, bd=0, highlightthickness=0)
        self.canvas.pack()

        bg_img = PhotoImage(file=r'/home/pi/home_display/gui_clocks/rainy_window.png')
        self.bg_img = bg_img  # prevents bg_img from garbage collecting
        self.canvas.create_image(0, 0, image=self.bg_img, anchor=NW)
        self.time_label = self.canvas.create_text((self.w/2+10, self.h/2), font=("Candara", 170), fill='white')
        self.sec_label = self.canvas.create_text((self.w/2+315, self.h/2-50), font=("Candara", 70), fill='white')
        self.am_pm_label = self.canvas.create_text((self.w/2-310, self.h/2-50), font=("Candara", 60), fill='white')
        self.date_label = self.canvas.create_text((self.w/2, self.h/2+170), font=("Candara", 40), fill='white')
        self.temp_label = self.canvas.create_text((self.w/2+270, self.h/2-190), font=("Candara", 50), fill='white')

    def Update(self):

        curr_tm = time.localtime(time.time())
        time_text = time.strftime("%I:%M", curr_tm)
        sec_text = '{:02d}'.format(curr_tm.tm_sec)
        am_pm_text = 'am' if curr_tm.tm_hour < 12 else 'pm'
        date_text = '{} {}'.format(self.month_abb[curr_tm.tm_mon - 1], curr_tm.tm_mday)
        indoor_temp, outdoor_temp = int(global_vars.indoor_temp +0.5), int(global_vars.weather_val['T1H'] + 0.5)
        temp_text = '{}\N{DEGREE SIGN} | {}\N{DEGREE SIGN}'.format(indoor_temp, outdoor_temp)

        self.canvas.itemconfigure(self.time_label, text=time_text)
        self.canvas.itemconfigure(self.sec_label, text=sec_text)
        self.canvas.itemconfigure(self.am_pm_label, text=am_pm_text)
        self.canvas.itemconfigure(self.date_label, text=date_text)
        self.canvas.itemconfigure(self.temp_label, text=temp_text)


class GraphicClock(Frame):
    # display
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        bg_color = '#49A'
        self.config(background=bg_color, cursor='none')
        self.controller = controller
        self.controller.config(background='black', cursor='none')

        self.curr_tm = controller.curr_tm
        self.w = self.controller.w
        self.h = self.controller.h

        self.wday_abb = ['월', '화', '수', '목', '금', '토', '일']

        self.canvas = Canvas(self, width=self.w, height=self.h, bd=0, highlightthickness=0)
        self.canvas.pack()

        self.no_bg_img = True
        self.bg_img_day_list = []
        self.bg_img_night_list = []
        for i in range(5):
            bg_img_day = PhotoImage(file=r'/home/pi/home_display/gui_clocks/day%d.png' % i)
            bg_img_night = PhotoImage(file=r'/home/pi/home_display/gui_clocks/night%d.png' % i)
            self.bg_img_day_list.append(bg_img_day)
            self.bg_img_night_list.append(bg_img_night)

        self.bg_img = self.bg_img_day_list[0]
        self.day_time = False

        self.bg_img_label = self.canvas.create_image(0, 0, anchor=NW)
        self.time_label = self.canvas.create_text((self.w/2-40, self.h/2+15), font=("SeoulNamsan", 180), fill='white')
        self.sec_label = self.canvas.create_text((self.w/2+325, self.h/2+5), font=("SeoulNamsan", 70), fill='white')
        self.am_pm_label = self.canvas.create_text((self.w/2-270, self.h/2-170), font=("SeoulNamsan", 50), fill='white')
        self.date_label = self.canvas.create_text((self.w/2, self.h/2+170), font=("SeoulNamsan", 50), fill='white')
        self.temp_label = self.canvas.create_text((self.w/2+260, self.h/2-170), font=("SeoulNamsan", 50), fill='white')
        # self.motion_label = self.canvas.create_text((self.w/2+280, self.h/2+170), font=("SeoulNamsan", 30), fill='white')

    def Update(self):
        curr_t = time.time()
        curr_tm = time.localtime(curr_t)
        time_text = time.strftime("%I:%M", curr_tm)
        sec_text = '{:02d}'.format(curr_tm.tm_sec)
        am_pm_text = '오전' if curr_tm.tm_hour < 12 else '오후'
        date_text = '{}월 {}일 {}요일'.format(curr_tm.tm_mon, curr_tm.tm_mday, self.wday_abb[curr_tm.tm_wday])
        temp_text = ''
        if global_vars.smartthings_val['is_valid']:
            temp_text = '%s\N{DEGREE SIGN} | ' % int(global_vars.smartthings_val['living_room_temp'] + 0.5)
        else:
            temp_text = '- \N{DEGREE SIGN} | '
        if global_vars.weather_val['is_valid']:
            temp_text += '%s\N{DEGREE SIGN}' % int(global_vars.weather_val['T1H'] + 0.5)
        else:
            temp_text += '- \N{DEGREE SIGN}'
        sunrise_tm = time.localtime(time.mktime(global_vars.sunrise_datetime.timetuple()))
        sunset_tm = time.localtime(time.mktime(global_vars.sunset_datetime.timetuple()))

        day_time = False
        if sunrise_tm.tm_hour <= curr_tm.tm_hour <= sunset_tm.tm_hour:
            if sunrise_tm.tm_hour == curr_tm.tm_hour and sunrise_tm.tm_min > curr_tm.tm_min:
                day_time = False
            elif sunset_tm.tm_hour == curr_tm.tm_hour and sunset_tm.tm_min < curr_tm.tm_min:
                day_time = False
            else:
                day_time = True

        if self.day_time != day_time:
            self.day_time = day_time
            change_bg_img = True
        else:
            change_bg_img = False


        if self.no_bg_img or change_bg_img or (curr_tm.tm_min == 0 and curr_tm.tm_sec == 0):
            i = random.randint(0, 4)
            if day_time:
                self.bg_img = self.bg_img_day_list[i]
            else:
                self.bg_img = self.bg_img_night_list[i]
            self.no_bg_img = False

        self.canvas.itemconfigure(self.bg_img_label, image=self.bg_img)
        self.canvas.itemconfigure(self.time_label, text=time_text)
        self.canvas.itemconfigure(self.sec_label, text=sec_text)
        self.canvas.itemconfigure(self.am_pm_label, text=am_pm_text)
        self.canvas.itemconfigure(self.date_label, text=date_text)
        self.canvas.itemconfigure(self.temp_label, text=temp_text)

        # motion_text = '%s' % int(time.time() - global_vars.smartthings_val['last_motion_time'])
        # self.canvas.itemconfigure(self.motion_label, text=motion_text)


