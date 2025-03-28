from machine import Pin, PWM  # 버저를 제어하기 위한 라이브러리 가져오기
from utime import sleep  # 노트 사이에 지연을 만들기 위한 sleep 함수 가져오기
import notes  # 음표에 대한 주파수 값을 포함하는 모듈 가져오기

# 22번 핀에 버저 초기화
buzzer = PWM(Pin(22))

# 멜로디(노래) 정의, "P"는 쉬는 부분을 의미
song = [
    "E5", "E5", "P", "E5", "P", "C5", "E5", "P", "G5", "P", "P", "P", "G4", "P", "P", "P",
    "C5", "P", "P", "G4", "P", "P", "E4", "P", "P", "A4", "P", "B4", "P", "AS4", "A4",
    "G4", "E5", "G5", "A5", "F5", "G5", "P", "E5", "C5", "D5", "B4", "P", "P",
    "C5", "P", "P", "G4", "P", "P", "E4", "P", "P", "A4", "P", "B4", "P", "AS4", "A4",
    "G4", "E5", "G5", "A5", "F5", "G5", "P", "E5", "C5", "D5", "B4", "P", "P"
]

# 음표를 재생하는 함수
def playtone(frequency):
    if frequency == 0:  # 주파수가 0일 때(쉼표)
        buzzer.duty_u16(0)
    else:
        buzzer.duty_u16(3000)  # 소리의 크기(볼륨) 설정
        buzzer.freq(frequency)  # 주파수 설정

# 소리를 끄는 함수
def bequiet():
    buzzer.duty_u16(0)

# 노래를 재생하는 함수
def playsong(mysong):
    for note in mysong:
        if note == "P":  # 쉼표일 때
            bequiet()
        else:
            playtone(notes.tones[note])  # 음표 재생
        sleep(0.2)  # 노트 사이의 지연 (속도 설정 부분)
    bequiet()

# 메인 함수 실행
playsong(song)




# 1. 멜로디 곡의 제목은?
# 이 멜로디는 "슈퍼마리오"의 주제곡입니다.

# 2. 멜로디의 속도를 정하는 코드는 어느 부분일까?
# 노트 사이의 지연을 설정하는 부분은 "sleep(0.2)"입니다.

# 3. 소리의 크기를 정하는 코드는 어느 부분일까?
# 소리의 크기(볼륨)는 "buzzer.duty_u16(3000)" 부분에서 설정됩니다.