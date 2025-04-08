from machine import Pin
import utime

led = Pin('LED', Pin.OUT)

# GPIO 20번 핀에 연결된 버튼을 입력 모드로 설정합니다. 내부 풀업 저항을 활성화합니다.
button = Pin(20, Pin.IN, Pin.PULL_UP)

# LED 상태를 저장할 변수 (False: 꺼짐, True: 켜짐)
led_state = False

# 이전 버튼 상태를 저장할 변수 (버튼 상태 변화 감지용)
previous_button_state = 1  # 기본값은 버튼이 눌리지 않은 상태(1)

# LED 초기 상태 설정
led.value(led_state)

# 무한 루프를 통해 버튼의 상태를 지속적으로 확인하고 LED를 제어합니다.
while True:
    # 현재 버튼 상태 읽기
    current_button_state = button.value()
    
    # 버튼이 눌렸을 때 (이전 상태는 1, 현재 상태는 0)
    if previous_button_state == 1 and current_button_state == 0:
        # LED 상태 토글
        led_state = not led_state
        # LED 상태 적용
        led.value(led_state)
        
        # 상태가 변경되었음을 출력
        if led_state:
            print("LED 켜짐")
        else:
            print("LED 꺼짐")
    
    # 현재 버튼 상태를 이전 상태로 저장
    previous_button_state = current_button_state
    
    # 0.1초 대기 (버튼 디바운싱 및 CPU 부하 감소)
    utime.sleep(0.1)