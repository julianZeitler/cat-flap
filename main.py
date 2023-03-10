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
    np_array = cam.capture_array()
    print(np_array)
    cam.capture_file("cap-{}.jpg".format(count))
    cam.stop()
    count += 1

def arduino_pi_comms(ser, sensitivity_timer, current_time):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
                
            # Change sensitivity_time to 10 seconds (default 30 seconds) to execute a motion trigger
            print("Motion Detected | Sensitivity Timeout", sensitivity_timer, "|", "Time since last motion trigger",time.time()- current_time)
     
            
            if(line == "1"): #if pir sensor value = 1/high
                detected = True
            
            # only send email notification if motion is detected after X seconds
            if(int(time.time() - current_time) > sensitivity_timer):
                
                current_time = time.time()
                print("Arduino Output:", line) # print output from Arduino Comms
                if(detected == True):
                    detected = False
                    take_picture()

if __name__ == "__main__":
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.reset_input_buffer()
        
        if ser:
            # Create a thread for parallel processing/ multithreading (camera stream and PIR Sensor trigger)
            arduino_comms_thread = threading.Thread(target=arduino_pi_comms, args=(ser, sensitivity_timer, current_time))
            arduino_comms_thread.daemon = True
            arduino_comms_thread.start()
    except:
        print("Arduino not recognised")
    while True:
        pass