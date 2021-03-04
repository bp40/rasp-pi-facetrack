import RPi.GPIO as GPIO
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import sys

#print("It's running")


try:
    face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/class1/OpenCV_projects/data/haarcascade_frontalface_default.xml')
    cam = PiCamera()
    cam.resolution = (320,240)  #320x240
    cam.framerate = 60
    #cam.rotation = 180
    rawc = PiRGBArray(cam, size=(320,240))
    
    time.sleep(0.1)

except:
    print("cam error")
    cv2.destroyAllWindows()
    sys.exit()
    
try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    control_pins = [13,11,15,12]
    vertical_pins = [37,35,38,36]
    
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)
    
    for pin in vertical_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)
        
    halfstep_seq = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],  
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1],
    ]
    
    halfstep_seq_reverse =  halfstep_seq[::-1]

except:
     GPIO.cleanup()
     
def turnSearch():
    for i in range(50):
        for halfstep in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
            time.sleep(0.01)
    
def turnLeft(size = 1):
    for i in range(size):
        for halfstep in range(8):
            for hpin in range(4):
                GPIO.output(control_pins[hpin], halfstep_seq[halfstep][hpin])
            time.sleep(0.01)
        
def turnRight(size = 1):
    for i in range(size):
        for halfstep in range(8):
            for hpin in range(4):
                GPIO.output(control_pins[hpin], halfstep_seq_reverse[halfstep][hpin])
            time.sleep(0.01)
            
def tiltUp(size = 1):
    for i in range(size):
        for halfstep in range(8):
            for vpin in range(4):
                GPIO.output(vertical_pins[vpin], halfstep_seq_reverse[halfstep][vpin])
            time.sleep(0.01)

def tiltDown(size = 1):
    for i in range(size):
        for halfstep in range(8):
            for vpin in range(4):
                GPIO.output(vertical_pins[vpin], halfstep_seq[halfstep][vpin])
            time.sleep(0.01)
    
try:
    
    turnLeft(5)
    time.sleep(1)
    turnRight(5)
    
    for frame in cam.capture_continuous(rawc, format="bgr", use_video_port=True):
        img = frame.array
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            
            #cv2.rectangle(img, (x,y), (x + w, y + h), (255,0,0),2)

            horizontalMidpoint = ((x+w) + x)/2
            verticalMidPoint = ((y+h) + y) / 2 

            if horizontalMidpoint > 220:
                print("Turning left")
                turnLeft()
                time.sleep(0.05)
            if horizontalMidpoint < 90: 
                print("Turning right")
                turnRight()
                time.sleep(0.05)
                
            time.sleep(0.01)
                
            if verticalMidPoint < 80:
                print("Tilting Up")
                tiltUp()
                time.sleep(0.05)
                
            if verticalMidPoint > 170:
                print("Tilting Down")
                tiltDown()
                time.sleep(0.05)
                
            break
        
            #face_gray = gray[y:y+h, x:x+w]
            #face_color = img[y:y+h, x:x+w]
        
        #cv2.rectangle(img, (90, 60), (220, 180), (0,0,255),2)
        #cv2.imshow("Frame", img)
        
        key = cv2.waitKey(1) & 0xFF
        
        rawc.truncate(0)
        
        if key == ord("q"):
            break
        
finally:
    cv2.destroyAllWindows()
    GPIO.cleanup()
#print('It ran')


