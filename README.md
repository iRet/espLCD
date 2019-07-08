# espLCD
esp32 weather station using micro python

## Hardware
esp32 board with pre-installed micro python
i2c connected text lcd display (1602)
i2c connected temperature and humidity sensor (htu21d)

## API tokens
Project uses two data providers:
- [OpenWeather](https://openweathermap.org/)
- [TimeZoneDB](https://timezonedb.com)

## Libraries
- [python_lcd](https://github.com/dhylands/python_lcd)
- [htu21d-esp8266](https://github.com/julianhille/htu21d-esp8266)

## Tools
It is highly recommended to use [rshell](https://github.com/dhylands/rshell) to upload scripts

## Upload
`rshell -p /dev/tty.SLAB_USBtoUART`

Internal storage is available as /pyboard

Update api tokens and wifi credentials beforehand

```shell
cp htu21d.py /pyboard
cp lcd_api.py /pyboard
cp esp32_gpio_lcd.py /pyboard
cp boot.py /pyboard
cp lcd.py /pyboard
```
