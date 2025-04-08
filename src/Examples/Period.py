from machine import Pin, I2C
import neopixel
import time
import ahtx0

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

# 시간 설정 (초 단위)
light_duration = 5  # LED가 켜져 있는 시간
off_duration = 10   # LED가 꺼져 있는 시간

# 카운터 변수
light_counter = 0  # LED가 켜진 후 경과 시간
off_counter = 0    # LED가 꺼진 후 경과 시간
light_is_on = False  # LED 상태 (시작 시 꺼짐)

# 시작할 때 LED는 꺼진 상태로 설정
np_off()

# 동작을 알리는 내장 LED
led.on()  # 내장 LED를 켜서 프로그램이 실행 중임을 표시

# 제어 변수 추가
auto_cycle_started = False  # 자동 주기가 시작되었는지 확인

print("프로그램이 시작되었습니다.")
print("버튼을 누르면 LED 주기가 시작됩니다.")

while True:
    # 버튼 상태 확인
    if button.value() == 0:  # 버튼이 눌림
        if not auto_cycle_started:
            auto_cycle_started = True
            print("자동 주기가 시작되었습니다.")
            
        # 주기 재시작
        light_is_on = True
        light_counter = 0
        np_on()
        print(f"버튼이 눌렸습니다! LED 주기를 재시작합니다. {light_duration}초 동안 켜집니다.")
        
        # 버튼이 떼어질 때까지 대기
        while button.value() == 0:
            time.sleep(0.1)
    
    # 자동 LED 제어 (이미 자동 주기가 시작된 경우에만)
    if auto_cycle_started:
        if light_is_on:
            light_counter += 1  # 켜진 후 경과 시간 증가
            
            # 설정한 시간(초)에 도달하면 LED 끄기
            if light_counter >= light_duration:
                np_off()
                light_is_on = False
                off_counter = 0  # 꺼짐 카운터 초기화
                print(f"LED가 꺼집니다. {off_duration}초 후에 다시 켜집니다.")
        else:
            off_counter += 1  # 꺼진 후 경과 시간 증가
            
            # 설정한 시간(초)에 도달하면 LED 켜기
            if off_counter >= off_duration:
                np_on()
                light_is_on = True
                light_counter = 0  # 켜짐 카운터 초기화
                print(f"LED가 켜집니다. {light_duration}초 동안 켜져 있습니다.")
   
    time.sleep(1)  # 1초 대기