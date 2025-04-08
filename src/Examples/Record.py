import time, machine
from ds3231_port import DS3231
from machine import I2C, Pin
import ahtx0

# 컴퓨터 시간과 통신을 설정합니다.
i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
rtc = DS3231(i2c0)
    
# 온습도 센서과 통신을 설정합니다. 
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

# 온습도 센서와 RTC 센서를 연결합니다.
sensor = ahtx0.AHT20(i2c)

#데이터를 기록할 파일을 생성합니다.
f = open('data.csv', 'a')
# 파일에 시간, 온도, 습도 순서로 기록합니다.
f.write("Time, Temperature, Humidity\n")

print("ATH21의 온도와 습도를 측정합니다.")


def record_data():
    while True :
        now = rtc.get_time()
        humidity = sensor.relative_humidity
        temperature = sensor.temperature
        # format: 년도, 월, 일, 시간, 분, 초 
        print("Time: {}/{}/{} {}:{}:{}".format(now[0], now[1], now[2], now[3], now[4], now[5]))
        print("Humidity: {:.2f}%".format(humidity))
        print("Temperature: {:.2f}C".format(temperature))
        # 시간, 분, 초, 온도, 습도를 파일에 저장합니다.
        f.write("{}/{}/{} {}:{}:{}, {:.2f}, {:.2f}\n".format(now[0], now[1], now[2], now[3], now[4], now[5], temperature, humidity))
        # 기록 주기를 1초로 설정합니다.
        time.sleep(1)

try:
    record_data()
# stop를 눌러서 프로그램 종료하기
except KeyboardInterrupt:
    pass
finally:
    print("프로그램을 종료합니다.")
    f.close()





