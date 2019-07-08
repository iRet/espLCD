from machine import Pin, RTC, I2C
from esp32_gpio_lcd import GpioLcd
from utime import sleep_ms, ticks_ms

import urequests 
import _thread
import time

from htu21d import HTU21D

DEBUG = False

ow_appid = 'CHANGE_ME_OPENWEATHER_TOKEN'
ow_q     = 'Vancouver,CA'
ow_units = 'metric'

tzdb_token = 'CHANGE_ME_TZDB_TOKEN'
tzdb_zone = 'America/Vancouver'
tzdb_endpoint = ('http://api.timezonedb.com/v2.1/get-time-zone?format=json&' 
                 'key=' + tzdb_token + '&by=zone&zone=' + tzdb_zone)

MY_I2C = I2C(scl = Pin(0), sda = Pin(15), freq = 100000)

ow_endpoint = ('http://api.openweathermap.org/data/2.5/weather?'
               'q=' + ow_q + '&appid=' + ow_appid + '&units=' + ow_units)

rtc = RTC()
degree = bytearray([0x06,0x09,0x09,0x06,0x0,0x0,0x0,0x0])
clock  = bytearray([0x00,0x0e,0x15,0x17,0x11,0x0e,0x00,0x00])


def debug(msg):
    if DEBUG: print(msg)


class TZ:
    offset = 0

    @classmethod
    def update(self):
        response = urequests.get(tzdb_endpoint)
        json = response.json()
        self.offset = int(json['gmtOffset']) / 3600

class Weather:
    ow = {}
    temp = 0
    wind = 0
    humidity = 0
    success = False

    @classmethod
    def update(self):
        while True:
            try:
                debug('[DEBUG] Fetching weather:')

                response = urequests.get(ow_endpoint)
                self.ow = response.json()
                
                debug(self.ow)
                
                self.temp = self.ow['main']['temp']
                self.wind = self.ow['wind']['speed']
                self.humidity = self.ow['main']['humidity']
                self.success = True

            except:
                debug('Exception ocurred')
                self.success = False
            
            sleep_ms(60000)

class Sensor:
    htu = HTU21D(i2c = MY_I2C)
    temp = 0
    humidity = 0
    
    @classmethod
    def update(self):
        while True:
            self.temp = self.htu.temperature()     
            self.humidity = self.htu.humidity()
            sleep_ms(10000)


def main_loop():
    debug('[INFO] Warming up!') 
    TZ.update()

    lcd = GpioLcd(rs_pin=Pin(14),
                  enable_pin=Pin(13),
                  d4_pin=Pin(27),
                  d5_pin=Pin(26),
                  d6_pin=Pin(25),
                  d7_pin=Pin(33),
                  num_lines=2, num_columns=16)

    lcd.custom_char(1, clock)
    lcd.custom_char(2, degree)

    _thread.start_new_thread(Weather.update, ())
    _thread.start_new_thread(Sensor.update, ())

    lcd.putstr("Warming up...\nStay tuned!\n")
    sleep_ms(1000)
    lcd.clear()

    lcd.move_to(5, 1)
    lcd.putchar(chr(1))

    lcd.move_to(2, 0)
    lcd.putchar(chr(2))
    lcd.putchar('C')

    tick = True

    while True:   
        lcd.move_to(0, 1)
        lcd.putstr("%.1f" % Sensor.temp)     
        
        lcd.move_to(12, 1)
        lcd.putstr("%.1f" % Sensor.humidity)

        lcd.move_to(0, 0)
        lcd.putstr("%2d" % Weather.temp)
        lcd.move_to(4, 0)

        if Weather.success:
            lcd.putstr("%3d m/s" % Weather.wind)
        else:
            lcd.putstr("No data")

        lcd.move_to(12, 0)
        lcd.putstr("%3d%%" % Weather.humidity)

        dt = rtc.datetime()
        lcd.move_to(6, 1)
        
        hours = (dt[4] + TZ.offset) % 12
        if hours == 0: 
            hours = 12
            
        lcd.putstr("%2d" % hours)

        lcd.move_to(8, 1)
        lcd.putstr(':' if tick else ' ')

        lcd.move_to(9, 1)
        lcd.putstr("%02d" % dt[5]) 

        tick = not tick
        sleep_ms(1000)

