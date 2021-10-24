from bmp280 import *
from machine import Pin, I2C
import utime
from time import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)


sclPin = Pin(1) 
sdaPin = Pin(0) 
i2c_object = I2C(0,              
                 scl = sclPin,   
                 sda = sdaPin,   
                 freq = 1000000) 

result = I2C.scan(i2c_object)

if result != []:
    pass
else:
    print("Sensor nao encontrado ")



bmp280_object = BMP280(i2c_object,
                       addr = 0x76, 
                       use_case = value_from_BMP280_CASE_WEATHER)

bmp280_object.power_mode = value_from_BMP280_POWER_NORMAL
bmp280_object.oversample = value_from_BMP280_OS_HIGH
bmp280_object.temp_os = value_from_BMP280_TEMP_OS_8
bmp280_object.press_os = value_from_BMP280_TEMP_OS_4
bmp280_object.standby = value_from_BMP280_STANDBY_250
bmp280_object.iir = value_from_BMP280_IIR_FILTER_2

mostrador = 0

while True:
    temperature_c = bmp280_object.temperature 

    pressure = bmp280_object.pressure  
    altitude = bmp280_object.altitude_IBF(pressure)

    press = "{:.2f}".format(pressure)
    i_alti = "{:.2f}".format(altitude)

    lcd.skip_info(0,0)
    lcd.putstr("Temp.: ")
    lcd.putstr(str(temperature_c))
    lcd.putstr(" C")

    if mostrador:
        lcd.skip_info(0,1)
        lcd.putstr("                ")
        lcd.skip_info(0,1)
        lcd.putstr("Press.:")
        lcd.putstr(str (press))
        lcd.putstr(" hPa")
    else:
        lcd.skip_info(0,1)
        lcd.putstr("                ")
        lcd.skip_info(0,1)
        lcd.putstr("Alt: ")
        lcd.putstr(str (i_alti))
        lcd.putstr(" mtr")


    sleep(3)
    mostrador = not mostrador