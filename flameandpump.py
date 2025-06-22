import RPi.GPIO as GPIO
import time

#flame_sensor_pins = [16 , 1, 7]
pump_pin = 26
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)
GPIO.setup(26, GPIO.OUT)
try:
    while True:
        #GPIO.output(pump_pin, GPIO.LOW)
        if GPIO.input(16)==False:
            print("Flame detected!Turning on the pump")
            GPIO.output(pump_pin, GPIO.HIGH)
            time.sleep(2)
        else:
            print("no fire detected")
            GPIO.output(pump_pin, GPIO.LOW)
            time.sleep(1)      
  
except KeyboardInterrupt:
    print("program stopped by user") 
finally:
    GPIO.cleanup()