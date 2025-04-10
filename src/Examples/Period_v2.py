from machine import Pin, PWM
import neopixel
import time

led = Pin('LED', Pin.OUT)

buzzer = PWM(Pin(22))

# 부저를 울리는 함수
def button_buzzer(freq):
    buzzer.duty_u16(30000)
    buzzer.freq(freq)
    time.sleep(0.1)
    buzzer.duty_u16(0)

# 부팅을 알리는 부저 소리
def start_buzzer():
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    buzzer.duty_u16(0)

# NeoPixel 설정
np0 = neopixel.NeoPixel(Pin(21), 12)  # LED 설정

def np_on():
   for i in range(0, np0.n):
       np0[i] = (130,30,235)  # 성장기 색으로 설정
   np0.write()

def np_off():
   for i in range(0, np0.n):
       np0[i] = (0,0,0)  # LED 끄기
   np0.write()

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
button_pressed = False  # 버튼 상태 추적을 위한 변수 추가

# 프로그램을 알리는 음
start_buzzer()
print("프로그램이 시작되었습니다.")
print("버튼을 누르면 LED 주기가 시작/중지됩니다.")

while True:
    # 버튼 상태 확인
    if button.value() == 0 and not button_pressed:  # 버튼이 눌리고 이전에 눌리지 않았을 때
        button_pressed = True  # 버튼이 눌렸음을 기록
        
        # 자동 주기 상태 토글
        auto_cycle_started = not auto_cycle_started
        
        if auto_cycle_started:
            print("자동 주기가 시작되었습니다.")
            light_is_on = True
            light_counter = 0
            np_on()
            button_buzzer(2000)
            print(f"LED가 켜졌습니다. {light_duration}초 동안 켜져 있습니다.")
        else:
            print("자동 주기가 중지되었습니다.")
            np_off()  # LED 끄기
            button_buzzer(1000)  # 다른 주파수로 중지 알림
            
        # 버튼이 떼어질 때까지 대기
        while button.value() == 0:
            time.sleep(0.1)
            
    elif button.value() == 1 and button_pressed:  # 버튼이 떼어졌을 때
        button_pressed = False  # 버튼 상태 초기화
        time.sleep(0.2)  # 디바운스를 위한 짧은 지연
    
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