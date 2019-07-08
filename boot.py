import machine
import lcd
import _thread
from ntptime import settime

def connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('AP_NAME', 'AP_PASSWORD')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def no_debug():
    import esp
    esp.osdebug(None)


no_debug()
connect()
settime()

_thread.start_new_thread(lcd.main_loop(), ())
