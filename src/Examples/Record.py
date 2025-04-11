import time, machine
from ds3231_port import DS3231
from machine import I2C, Pin
import ahtx0
from bh1750 import BH1750

i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
rtc = DS3231(i2c0)

bh1750 = BH1750(0x23, i2c0)
    
i2c1 = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

sensor = ahtx0.AHT20(i2c1)

f = open('data.csv', 'a')
f.write("Time, Temperature, Humidity, Light\n")

print("ATH21의 온도와 습도, BH1750의 조도를 측정합니다.")


def record_data():
    while True :
        now = rtc.get_time()
        humidity = sensor.relative_humidity
        temperature = sensor.temperature
        light = bh1750.measurement  # 조도 값을 측정합니다.
        
        # format: 년도, 월, 일, 시간, 분, 초 
        print("Time: {}/{}/{} {}:{}:{}".format(now[0], now[1], now[2], now[3], now[4], now[5]))
        print("Humidity: {:.2f}%".format(humidity))
        print("Temperature: {:.2f}C".format(temperature))
        print("Light: {:.2f} lux".format(light))  # 조도 값 출력
        
        # 시간, 분, 초, 온도, 습도, 조도를 파일에 저장합니다.
        f.write("{}/{}/{} {}:{}:{}, {:.2f}, {:.2f}, {:.2f}\n".format(
            now[0], now[1], now[2], now[3], now[4], now[5], 
            temperature, humidity, light))  # 조도 값 추가
            
        # 기록 주기를 1초로 설정합니다.
        time.sleep(1)

try:
    record_data()
except KeyboardInterrupt:
    pass
finally:
    print("프로그램을 종료합니다.")
    f.close()





