from machine import Pin, I2C
import neopixel
import time
import ahtx0

# Led핀은 출력으로 설정
led = Pin('LED', Pin.OUT)

# NeoPixel 설정
np0 = neopixel.NeoPixel(Pin(21), 12)  # LED 설정

def np_on():
   for i in range(0, np0.n):
       np0[i] = (255,0,0)  # 빨간색으로 설정
   np0.write()

def np_off():
   for i in range(0, np0.n):
       np0[i] = (0,0,0)  # LED 끄기
   np0.write()
   
# 온습도 센서와 통신 설정
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)

# 온습도 센서와 RTC 센서 연결
sensor = ahtx0.AHT20(i2c)

# 버튼 설정 (실제 사용하는 핀 번호로 변경하세요)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# LED가 켜져 있을 시간 (초 단위)
light_duration = 5  # 5초 동안 켜짐

# 카운터 변수
light_counter = 1
light_is_on = True

# 처음 네오픽셀은 꺼져있도록하기
np_off()

# 동작을 알리는 LED
led.on()

while True:    
   # 버튼이 눌렸는지 확인 (버튼이 눌리면 값이 0)
   if button.value() == 0:
       np_on()  # LED 켜기
       light_is_on = True
       light_counter = 0  # 카운터 초기화
       print(f"LED가 {light_duration}초 간 켜집니다")
   
   # LED가 켜져 있고 카운터가 설정 시간보다 작으면
   if light_is_on == True:
       light_counter = light_counter + 1  # 카운터 증가
       
       # 설정한 시간(초)에 도달하면 LED 끄기
       if light_counter >= light_duration:
           np_off()  # LED 끄기
           light_is_on = False
           print(f"LED가 꺼집니다.")
   
   time.sleep(1)  # 1초 대기