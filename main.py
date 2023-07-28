import cv2
import numpy as np
import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()
def empty(img):
    pass
video = cv2.VideoCapture(0)
cv2.namedWindow("TrackBar")
cv2.resizeWindow("TrackBar", 600, 300)
cv2.createTrackbar("hue_min", "TrackBar", 0, 179, empty)
cv2.createTrackbar("hue_max", "TrackBar", 179, 179, empty)
cv2.createTrackbar("sat_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("sat_max", "TrackBar", 255, 255, empty)
cv2.createTrackbar("val_min", "TrackBar", 0, 255, empty)
cv2.createTrackbar("val_max", "TrackBar", 255, 255, empty)
while True:
    ret, img= video.read()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos("hue_min", "TrackBar")
    hue_max = cv2.getTrackbarPos("hue_max", "TrackBar")
    sat_min = cv2.getTrackbarPos("sat_min", "TrackBar")
    sat_max = cv2.getTrackbarPos("sat_max", "TrackBar")
    val_min = cv2.getTrackbarPos("val_min", "TrackBar")
    val_max = cv2.getTrackbarPos("val_max", "TrackBar")

    lower = np.array([hue_min,sat_min,val_min])
    upper = np.array([hue_max,sat_max,val_max])
    mask = cv2.inRange(hsv, lower, upper)

    cnts, hei = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cnts:
        area= cv2.contourArea(c)
        if area>300:
            peri= cv2.arcLength(c, True)
            approx= cv2.approxPolyDP(c, 0.02*peri,True)
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img, (x,y),(x+w, y+h),(0,255,0),2)
            cv2.putText(img, "Points:" + str(len(approx)), (x + w + 20, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
        if len(approx)==6:
            ser.write(b"5\n")
            cv2.putText(img,"LUCGIAC",(x+w+20, y+h+45), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0,255,255),2)
        elif len(approx)==3:
            ser.write(b"3\n")
            cv2.putText(img, "TAMGIAC", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (255, 255, 0), 2)
        else:
            cv2.putText(img, "Circle", (x + w + 20, y + h + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (255, 255, 255), 2)

    cv2.imshow("Frame", img)
    cv2.imshow("hsv", hsv)
    cv2.imshow("Mask", mask)
    k= cv2.waitKey(1)
    if k==ord('q'):
        break
video.release()
cv2.destroyAllWindows()
