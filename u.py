#!/usr/bin/python
#
# ultrasonic_2.py
# SHIT DETECTOR
#
# Author : Andrew Ho
# Date   : October 8, 2013

# -----------------------
# Python libraries
# -----------------------
import time
import RPi.GPIO as GPIO
from httplib2 import Http
from urllib import urlencode

# -----------------------
# Function defines
# -----------------------

def measure():
  # pulse input
  GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)

  # set it back to input
  GPIO.setup(GPIO_TRIGGER, GPIO.IN)
  start = time.time()

  while GPIO.input(GPIO_TRIGGER)==0:
    start = time.time()

  while GPIO.input(GPIO_TRIGGER)==1:
    stop = time.time()

  # we know speed of sound, so we can get the distance, booyah
  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

def measure_average():
  # This function takes 3 measurements and
  # returns the average.
  distance1=measure()
  time.sleep(0.3)
  distance2=measure()
  time.sleep(0.3)
  distance3=measure()
  distance = distance1 + distance2 + distance3
  distance = distance / 3
  return distance

# -----------------------
# Main Script
# -----------------------

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_TRIGGER = 4

print "Measurement"

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)

# try catch so we can break with ctrl-c
try:

  while True:

    # distance = measure_average()
    distance = measure();
    h = Http()
    data = dict(d=distance)
    resp, content = h.request("http://10.0.1.166:3000/sensor", "POST", urlencode(data))
    print resp
    print "Distance : %.1f" % distance
    time.sleep(2)

except KeyboardInterrupt:
  # User pressed CTRL-C
  # Reset GPIO settings
  GPIO.cleanup()
