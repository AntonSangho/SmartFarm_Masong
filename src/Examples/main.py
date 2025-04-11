import time, machine
from ds3231_port import DS3231
from machine import I2C, Pin, PWM
import ahtx0
from bh1750 import BH1750
import neopixel

#--------- 핀 설정 및 센서 초기화 ---------#

# 내장 LED 설정
led = Pin('LED', Pin.OUT)

# 버튼 설정 (눌렀을 때 0, 평소에는 1을 반환하는 PULL_UP 방식)
button = Pin(20, Pin.IN, Pin.PULL_UP)

# 부저 설정
buzzer = PWM(Pin(22))

# NeoPixel LED 설정 (핀 21, 12개의 LED)
np0 = neopixel.NeoPixel(Pin(21), 12)

# I2C 버스 0번 설정 (RTC와 조도 센서용)
i2c0 = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)
# 시간 모듈(RTC) 초기화
rtc = DS3231(i2c0)
# 조도 센서 초기화
bh1750 = BH1750(0x23, i2c0)

# 온습도 센서 통신 설정
i2c1 = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)
# 온습도 센서 초기화
sensor = ahtx0.AHT20(i2c1)

# 기록 간격 설정 (30분 = 1800초)
recording_interval = 30
last_record_time = 0
data_file = None

#--------- 기능 함수 정의 ---------#

# 네오픽셀 켜기
def np_on():
   for i in range(0, np0.n):
       np0[i] = (80,40,220)  # 성장기에 좋은 색으로 설정 (보라색)
   np0.write()  # LED에 변경사항 적용

# 네오픽셀 끄기
def np_off():
   for i in range(0, np0.n):
       np0[i] = (0,0,0)  # LED 끄기 (검은색)
   np0.write()  # LED에 변경사항 적용

# 버튼 눌렀을 때 짧은 부저음
def button_buzzer(freq):
    buzzer.duty_u16(30000)  # 부저 켜기 (소리 크기 설정)
    buzzer.freq(freq)       # 주파수 설정 (높은 값 = 높은 소리)
    time.sleep(0.1)         # 0.1초 동안 소리내기
    buzzer.duty_u16(0)      # 부저 끄기

# 프로그램 시작 시 멜로디 부저음
def start_buzzer():
    # 점점 높아지는 3단계 소리
    buzzer.freq(1000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    
    buzzer.freq(2000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    
    buzzer.freq(3000)
    buzzer.duty_u16(30000)
    time.sleep(0.1)
    
    buzzer.duty_u16(0)  # 부저 끄기

# 데이터 기록 함수
def record_data():
    global data_file, last_record_time
    
    # 현재 시간 가져오기
    now = rtc.get_time()
    current_time = time.time()
    
    # 센서에서 데이터 읽기
    humidity = sensor.relative_humidity
    temperature = sensor.temperature
    light = bh1750.measurement
    
    # 측정값 출력
    print("Time: {}/{}/{} {}:{}:{}".format(now[0], now[1], now[2], now[3], now[4], now[5]))
    print("Humidity: {:.2f}%".format(humidity))
    print("Temperature: {:.2f}C".format(temperature))
    print("Light: {:.2f} lux".format(light))
    
    # 파일이 없으면 열기
    if data_file is None:
        try:
            data_file = open('data.csv', 'a')
            # 빈 파일인지 확인하고 필요하면 헤더 추가
            if data_file.seek(0, 2) == 0:  # 파일 끝이 0이면 빈 파일
                data_file.write("Time, Temperature, Humidity, Light\n")
        except:
            print("파일을 열 수 없습니다.")
            return
    
    # 정해진 간격마다 데이터 기록
    if current_time - last_record_time >= recording_interval:
        try:
            # 파일에 데이터 기록
            data_file.write("{}/{}/{} {}:{}:{}, {:.2f}, {:.2f}, {:.2f}\n".format(
                now[0], now[1], now[2], now[3], now[4], now[5], 
                temperature, humidity, light))
            
            # 버퍼에 있는 데이터를 즉시 디스크에 기록
            data_file.flush()
            
            # 파일을 닫았다가 다시 열어 데이터 안전성 확보
            data_file.close()
            data_file = open('data.csv', 'a')
            
            last_record_time = current_time
            print("데이터 기록 완료!")
        except Exception as e:
            print("데이터 기록 중 오류 발생:", e)

#--------- 메인 프로그램 ---------#

# 상태 변수 초기화
recording_active = False  # 기록 활성화 상태
button_pressed = False    # 버튼 상태 추적

# 시작 시 설정
np_off()                  # 네오픽셀 끄기
led.on()                  # 내장 LED 켜기 (프로그램 실행 중 표시)
start_buzzer()            # 시작 멜로디 재생

# 안내 메시지 출력
print("프로그램이 시작되었습니다.")
print("온습도,조도를 측정합니다.")
print("버튼을 누르면 기록과 네오픽셀이 시작/중지됩니다.")

try:
    # 메인 루프
    while True:
        # 1. 버튼 상태 확인 및 처리
        if button.value() == 0 and not button_pressed:  # 버튼이 새로 눌렸을 때
            button_pressed = True  # 버튼 상태 기록
            
            # 기록 상태 전환 (켜기 <-> 끄기)
            recording_active = not recording_active
            
            if recording_active:
                print("기록과 네오픽셀이 시작되었습니다.")
                np_on()               # 네오픽셀 켜기
                button_buzzer(2000)   # 시작 부저음 (높은 음)
                
                # 파일 열기
                if data_file is None:
                    data_file = open('data.csv', 'a')
                    # 빈 파일이면 헤더 추가
                    if data_file.seek(0, 2) == 0:
                        data_file.write("Time, Temperature, Humidity, Light\n")
                
                # 시작하자마자 첫 기록 수행
                last_record_time = time.time() - recording_interval  # 즉시 기록되도록 설정
            else:
                print("기록과 네오픽셀이 중지되었습니다.")
                np_off()              # 네오픽셀 끄기
                button_buzzer(1000)   # 중지 부저음 (낮은 음)
                
                # 파일 안전하게 닫기
                if data_file is not None:
                    data_file.flush()
                    data_file.close()
                    data_file = None
                
            # 버튼이 떼어질 때까지 대기 (중복 인식 방지)
            while button.value() == 0:
                time.sleep(0.1)
                
        elif button.value() == 1 and button_pressed:  # 버튼이 떼어졌을 때
            button_pressed = False  # 버튼 상태 초기화
            time.sleep(0.2)         # 디바운스 (버튼 신호 안정화)
        
        # 2. 기록이 활성화된 경우에만 데이터 측정 및 저장
        if recording_active:
            record_data()
        
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:  # Ctrl+C로 프로그램 중단 시
    pass
finally:  # 프로그램 종료 시 항상 실행
    print("프로그램을 종료합니다.")
    np_off()               # 네오픽셀 끄기
    button_buzzer(500)     # 프로그램 종료 부저음 (매우 낮은 음)
    
    # 파일 안전하게 닫기
    if data_file is not None:
        data_file.flush()
        data_file.close()