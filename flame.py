import RPi.GPIO as GPIO
import time

#يمكن تحتاجي تعرفي السينسور

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN)

try:
    while True:
        
        if GPIO.input(16)==False:
            print("Flame detected!Turning on the pump")
# يمكن تحتاجي sleep هون 
        else:
            print("no fire detected")
# برضو يمكن تحتاجي sleep هون 
  
except KeyboardInterrupt:
    print("program stopped by user") 
finally:
    GPIO.cleanup()