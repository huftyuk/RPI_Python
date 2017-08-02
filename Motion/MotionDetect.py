import RPi.GPIO as GPIO
import time
from subprocess import call

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(2)
    print "Ready"
    while True:
        if GPIO.input(PIR_PIN):
            print "Motion Detected!"
            #avconv -i rtsp://192.168.1.74/unicast -c:v copy -map 0:0 -f segment -segment_time 5 -segment_format mp4 "Camera%04d.mp4"
            
            TimeString = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            Name = "Camera" + TimeString + ".mp4"
            ##returncode = call(["avconv" , '-i', 'rtsp://192.168.1.74/unicast' , '-c:v',  'copy',  '-map' ,  '0:0', '-format' , 'mp4' , '-t' ,  '00:00:30' , Name])
            time.sleep(1)
        else:
            print "No Motion"
            time.sleep(1)
except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
