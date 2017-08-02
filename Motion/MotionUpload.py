import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

#Assumes this has been executed.
#avconv -i rtsp://192.168.1.74/unicast -c:v copy -c:a copy -f mpegts udp://localhost:1234
#ffmpeg -f lavfi -i color=black:WxH:r=FPS:d=30 -i camera_input \
#       -filter_complex "[0][1]concat[v]" -map "[v]" StreamingOutput
#    ffmpeg -f lavfi -i nullsrc=s=WxH:d=N -an -i rtsp://stream-ip:port -filter_complex "concat" -an -r 10 -tune zerolatency -preset fast -vcodec libx264 -f mpegts udp://outgoing-ip:port
try:
    print "PIR Module Test (CTRL+C to exit)"
    time.sleep(2)
    print "Ready"
    while True:
        # Outer loop sits in idle waiting for motion.
        if GPIO.input(PIR_PIN):
            print "Motion Detected!"
            #So lets get some capture started
            #time.sleep(1)
            #avconv -i rtsp://192.168.1.74/unicast -c:v copy -map 0:0 -f segment -segment_time 5 -segment_format mp4 "Camera%04d.mp4"
            #avconv -i  -c:v copy -map 0:0 -t 00:00:30 "Camera1.mp4"
            
            TimeString = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            Name = "Camera" + TimeString + ".mp4"
            #returncode = subprocess.call(["avconv" , '-i', 'udp://localhost:1235?multicast=1','-c:v','copy','-map','0:0','-t','00:05:00' , Name])
            p1 = subprocess.Popen(["avconv" , '-i', 'udp://localhost:1234?multicast=1','-c:v','copy','-c:a','copy','-map','0:0' , Name])
            tsincemotion = 0
            while tsincemotion < 30:
                if GPIO.input(PIR_PIN):
                    print("More motion")
                    tsincemotion = 0
                #Loop until the action stops
                time.sleep(1)
                tsincemotion = tsincemotion + 1
            print("No motion for specified period so stopping")
            #time.sleep(20)
            p1.terminate()
            NameArg = "--title=" + Name
            SecretArg =  "--client-secrets=/home/pi/Motion/client_secret_542273631401-5afokng7qre7hvetqme0ug2vovihliq7.apps.googleusercontent.com.json"
            ##returncode = call(["youtube-upload" ,NameArg , Name])
            p2 = subprocess.Popen(["youtube-upload" ,NameArg , SecretArg , Name])
        else:
            #print "No Motion"
            time.sleep(0.1)
except KeyboardInterrupt:
    print "Quit"
    GPIO.cleanup()
