import time
import threading
import os
import sys
import serial

from picamera2 import Picamera2


current_time = time.time()
sensitivity_timer = 30

cam = Picamera2()
config = cam.create_still_configuration()
cam.configure(config)

count = 1

def take_picture():
    cam.start()
    for _ in range(100):
        cam.capture_file("cap-{}.jpg".format(count))
        time.sleep(0.1)
        count += 1
    cam.stop()

def arduino_pi_comms(ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            
            if(line == "1"): #if pir sensor value = 1/high
                print("Arduino Output:", line) # print output from Arduino Comms
                if(detected == True):
                    detected = False
                    take_picture()

if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.reset_input_buffer()
        
        if ser:
            arduino_pi_comms(ser)
    except:
        print("Arduino not recognised")