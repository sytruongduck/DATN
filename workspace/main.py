import time
import math
import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP0, eQEP2

"""MotorA"""
IN1 = "P8_7"
IN2 = "P8_8"

"""MotorB"""
IN3 = "P8_9"
IN4 = "P8_10"

GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)

"""PWM"""
PWMA = "P9_14"
PWMB = "P9_16"

#PWM duty cycle. It must have a value from 0 to 100.
PWM.start(PWMA, 100, 2000, 1)
PWM.start(PWMB, 100, 2000, 1)

# Khởi tạo lớp để truy cập kênh eQEP1, eQEP2 và chỉ khởi tạo kênh đó
myEncoderA = RotaryEncoder(eQEP0)       #eQEP0    P9.27    P9.42
myEncoderB = RotaryEncoder(eQEP2)       #eQEP2    P8.11    P8.12
# Chế độ tuyệt đối: vị trí bắt đầu từ 0 và được tăng hoặc giảm theo chuyển động của bộ mã hóa
myEncoderA.setAbsolute()
myEncoderB.setAbsolute()

"""Ultrasonic Sensor"""
GPIO.setup("P9_15",GPIO.OUT) #Trigger
GPIO.setup("P9_12",GPIO.IN)  #Echo

#Security
GPIO.output("P9_15", False)
time.sleep(0.5)


def Stopmotor():
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    PWM.set_duty_cycle(PWMA, 0)
    PWM.set_duty_cycle(PWMB, 0)
def Backward():
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    PWM.set_duty_cycle(PWMA, 25)
    PWM.set_duty_cycle(PWMB, 25)
def Forward():
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)
    PWM.set_duty_cycle(PWMA, 25)
    PWM.set_duty_cycle(PWMB, 25)
def Right():
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)
    PWM.set_duty_cycle(PWMB, 25)
def Left():
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)
    PWM.set_duty_cycle(PWMA, 25)
    
# Xe quay 1 góc 90 độ

# Xe quay ngược 1 góc 90 độ

# Xe quay 1 góc 180 độ

# Xe quay ngược 1 góc 180 độ

def DistanceMeasurement(TRIG,ECHO):
    GPIO.output(TRIG, True)     # set Trigger to HIGH
    time.sleep(0.00001)         # set Trigger after 0.01ms to LOW
    GPIO.output(TRIG, False)

    pulseStart = 0
    pulseEnd = 0

    while GPIO.input(ECHO) == 0:
        pulseStart = time.time()
    while GPIO.input(ECHO) == 1:
        pulseEnd = time.time()

    pulseDuration = pulseEnd - pulseStart
    distance = pulseDuration * 17150        # multiply with the sonic speed (34300 cm/s)
    distance = round(distance, 2)   # Làm tròn
    return distance

"""
    Đường kính bánh xe: Dn = 95mm
    pi = 3.14
    Chu vi bánh xe: Dn*pi=95*3.14=298.3 (mm)
    Độ phân giải encoder 2400 xung/vòng
    Số mm/1xung=298.3/2400=0,1242916666666667 (mm)
"""
def Encoder_Wheel():
    # Nhận vị trí hiện tại
    positionA = myEncoderA.position
    positionB = myEncoderB.position
    # Pulse -> Distance
    wheel_A = positionA*(298.3/2400)
    print ("Distance_Wheel_A: ",wheel_A,"mm")
    wheel_B = positionB*(298.3/2400)
    print ("Distance_Wheel_B: ",wheel_B,"mm")

def Position(x_old, y_old, angle_old):
    b = 30  # Khoảng cánh giữa 2 bánh xe
    global wheel_A
    global wheel_B
    
    midpoint = (wheel_A + wheel_B) / 2        # Độ dịch chuyển tương đối của điểm trung tâm
    angle_new = (wheel_A + wheel_B) / b         # Góc xoay của xe

    angle_i = angle_old + angle_new       # Hướng tương đối của xe tại thời điểm i

    x_i = x_old + midpoint * math.cos(angle_i)          # Vị trí tương đối trục x của xe tại thời điểm i
    y_i = y_old + midpoint * math.sin(angle_i)         # Vị trí tương đối trục y của xe tại thời điểm i
    print ("x: %f" % x_i, "y: %f" % y_i, "angle: %f" % angle_i)

while True:
    Position(0,0,0)
    control = input("Control DC Motor: ")
    if control == "0":
        Stopmotor()
    elif control == "1":
        Forward()
    elif control == "2":
        Backward()
    elif control == "3":
        Left()
    elif control == "4":
        Right()
    else:
        PWM.stop(PWMA)
        PWM.stop(PWMB)
        PWM.cleanup()
        myEncoderA.zero()   # Đặt lại vị trí encoderA về 0
        myEncoderB.zero()   # Đặt lại vị trí encoderB về 0
    Encoder_Wheel()


    