from utime import sleep
from machine import Pin, I2C
import ahtx0

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

sensor = ahtx0.AHT20(i2c)

while True:
    celsius = sensor.temperature  # 센서에서 이미 섭씨 온도를 제공하므로 변환 불필요
    print("\nTemperature: %0.2f C" % celsius)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    sleep(1)