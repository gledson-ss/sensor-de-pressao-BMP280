from bmp280 import *
from machine import Pin, I2C
import utime
from time import sleep
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
i2c = I2C(0, sda = Pin(0), scl = Pin(1), freq = 400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.skip_info(0,0)
lcd.putstr("Weather Station")
lcd.skip_info(0,1)
lcd.putstr("Raspberry PiPico")
ERROR = -3 
sclPin = Pin(1) 
sdaPin = Pin(0) 
i2c_object = I2C(0,              
                 scl = sclPin,   
                 sda = sdaPin,   
                 freq = 1000000) 

result = I2C.scan(i2c_object)
print("I2C scan result : ", result) 
if result != []:
    print("I2C connection successfull")
else:
    print("No devices found !")



bmp280_object = BMP280(i2c_object,
                       addr = 0x76, 
                       use_case = value_from_BMP280_CASE_WEATHER)

bmp280_object.power_mode = value_from_BMP280_POWER_NORMAL
bmp280_object.oversample = value_from_BMP280_OS_HIGH
bmp280_object.temp_os = value_from_BMP280_TEMP_OS_8
bmp280_object.press_os = value_from_BMP280_TEMP_OS_4
bmp280_object.standby = value_from_BMP280_STANDBY_250
bmp280_object.iir = value_from_BMP280_IIR_FILTER_2

print("BMP Object created successfully !")
utime.sleep(2) 
print("\n")




def altitude_HYP(hPa , temperature):
    
    temperature = temperature
    local_pressure = hPa
    sea_level_pressure = 1013.25 
    pressure_ratio = sea_level_pressure/local_pressure 
    h = (((pressure_ratio**(1/5.257)) - 1) * temperature ) / 0.0065
    return h

def altitude_IBF(pressure):
    local_pressure = pressure    
    sea_level_pressure = 1013.25 
    pressure_ratio = local_pressure / sea_level_pressure
    altitude = 44330*(1-(pressure_ratio**(1/5.255)))
    return altitude

while True:
    temperature_c = bmp280_object.temperature 
    temperature_k = temperature_c + 273.15
    pressure = bmp280_object.pressure  
    pressure_hPa = ( pressure * 0.01 ) + ERROR 
    h = altitude_HYP(pressure_hPa, temperature_k)
    altitude = altitude_IBF(pressure_hPa)
    press = "{:.2f}".format(pressure_hPa)
    h_alti = "{:.2f}".format(h)
    i_alti = "{:.2f}".format(altitude)

    lcd.skip_info(0,0)
    lcd.putstr("Temp: ")
    lcd.putstr(str(temperature_c))
    lcd.putstr(" C")
    lcd.skip_info(0,1)
    lcd.putstr("                ")
    lcd.skip_info(0,1)
    lcd.putstr("Press:")
    lcd.putstr(str (press))
    lcd.putstr(" hPa")
    sleep(3)
    lcd.skip_info(0,1)
    lcd.putstr("                ")
    lcd.skip_info(0,1)
    lcd.putstr("Alt: ")
    lcd.putstr(str (i_alti))
    lcd.putstr(" mtr")
    sleep(3)
    

