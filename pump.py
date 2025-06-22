from time import sleep
import RPi.GPIO as GPIO

mot = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(mot, GPIO.OUT)
GPIO.output(mot,GPIO.LOW)
print('START WORKING')
GPIO.output(mot, GPIO.HIGH)
sleep(7)
GPIO.output(mot, GPIO.LOW)