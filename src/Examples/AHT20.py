from utime import sleep
from machine import Pin, I2C
import ahtx0

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

sensor = ahtx0.AHT20(i2c)

while True:
    fahrenheit = sensor.temperature * 9 / 5 + 32
    print("\nTemperature: %0.2f F" % fahrenheit)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    sleep(1)