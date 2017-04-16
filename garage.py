# Imports
import webiopi,time, subprocess, os, signal

#webiopi.utils.setDebug()

os.chdir("/home/pi/GarageDoorOpener/")

# Retrieve GPIO lib
#GPIO = webiopi.GPIO
import RPi.GPIO as GPIO

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

# Garage Door 
GD1=23  # Garage Door 1
GD2=24  # Garage Door 2

# -------------------------------------------------- #
# Define Macros                                      #
# -------------------------------------------------- #

def toggle_garagedoor1():
    GPIO.output(GD1, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GD1, GPIO.HIGH)

def toggle_garagedoor2():
    GPIO.output(GD2, GPIO.LOW)
    time.sleep(1)
    GPIO.output(GD2, GPIO.HIGH)
    
# -------------------------------------------------- #
# Initialization part                                #
# -------------------------------------------------- #

# Setup GPIOs
GPIO.setmode(GPIO.BCM)

GPIO.setup(GD1, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(GD2, GPIO.OUT, initial=GPIO.HIGH)

# -------------------------------------------------- #
# Start Webcam Sever                                 #
# -------------------------------------------------- #

webcam = subprocess.Popen('./stream.sh')
time.sleep(1)

# -------------------------------------------------- #
# Main server part                                   #
# -------------------------------------------------- #


# Instantiate the server on the port 8000, it starts immediately in its own thread
server = webiopi.Server(port=8000, coap_port=None, login="", password="")

# Register the macros so you can call it with Javascript and/or REST API

server.addMacro(toggle_garagedoor1)
server.addMacro(toggle_garagedoor2)

# -------------------------------------------------- #
# Loop execution part                                #
# -------------------------------------------------- #

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()

# -------------------------------------------------- #
# Termination part                                   #
# -------------------------------------------------- #

# Stop the server
server.stop()
time.sleep(1)

# Reset GPIO functions
GPIO.cleanup()
time.sleep(1)

# Stop the webcamera
os.kill(webcam.pid, signal.SIGTERM)
time.sleep(1)
