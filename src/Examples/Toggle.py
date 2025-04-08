from machine import Pin
import utime
from neopixel import NeoPixel

# 내장 LED 설정 (보드 상의 LED를 출력 모드로)
led = Pin('LED', Pin.OUT)

# 버튼을 설정버튼을 누르지 않았을 때 1(HIGH), 눌렀을 때 0(LOW) 값을 출력
button = Pin(20, Pin.IN, Pin.PULL_UP)

# 네오픽셀 연결
np0 = NeoPixel(machine.Pin(21), 12)

# 네오픽셀을 빨간색으로 켜는 함수
def np_on():
    for i in range(0, np0.n):  # 모든 LED에 대해 반복
        np0[i] = (255,0,0)     # RGB 값으로 빨간색(255,0,0) 설정
    np0.write()                # 설정 값을 네오픽셀에 적용

# 네오픽셀을 끄는 함수
def np_off():
    for i in range(0, np0.n):  # 모든 LED에 대해 반복
        np0[i] = (0,0,0)       # RGB 값을 (0,0,0)으로 설정하여 LED 끄기
    np0.write()                # 설정 값을 네오픽셀에 적용
    
# 이전 버튼 상태 초기화 (1 = 눌리지 않음)
previous_button_state = 1  
# LED 상태 초기화 (0 = 꺼짐)
led_state = 0
    
# 무한 루프로 계속해서 버튼 상태 확인
while True:
    # 현재 버튼 상태 읽기
    current_button_state = button.value()
    
    # 버튼이 눌리는 순간 감지 (이전 상태 = 안눌림(1), 현재 상태 = 눌림(0))
    if previous_button_state == 1 and current_button_state == 0:
        # LED 상태 토글 (True ↔ False 전환)
        led_state = not led_state
        # 내장 LED에 상태 적용
        led.value(led_state)
        
        # LED 상태에 따라 네오픽셀 제어
        if led_state:
            np_on()            # LED가 켜진 상태면 네오픽셀 켜기
            print("LED 켜짐")   # 상태 변경 메시지 출력
        else:
            np_off()           # LED가 꺼진 상태면 네오픽셀 끄기
            print("LED 꺼짐")   # 상태 변경 메시지 출력
    
    # 다음 반복을 위해 현재 버튼 상태를 이전 상태로 저장
    previous_button_state = current_button_state  
    
    # 0.1초 대기 (버튼 디바운싱 및 CPU 부하 감소)
    utime.sleep(0.1)
    
    
    