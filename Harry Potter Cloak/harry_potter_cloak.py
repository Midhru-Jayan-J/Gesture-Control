import numpy as np
import cv2 

def same(x):
    print("")

cap=cv2.VideoCapture(0)
bars=cv2.namedWindow("bars")

cv2.createTrackbar("upper_hue","bars",110,180,same)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, same)
cv2.createTrackbar("upper_value", "bars", 255, 255, same)
cv2.createTrackbar("lower_hue", "bars", 68, 180, same)
cv2.createTrackbar("lower_saturation", "bars", 55, 255, same)
cv2.createTrackbar("lower_value", "bars", 54, 255, same)

while(True):
    cv2.waitKey(2000)
    ret,init_frame=cap.read()
    if(ret):
        break
while(True):
    ret,frame=cap.read()
    inspect=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    upper_hue=cv2.getTrackbarPos("upper_hue","bars")
    upper_saturation=cv2.getTrackbarPos("upper_saturation","bars")
    upper_value=cv2.getTrackbarPos("upper_value","bars")
    lower_value=cv2.getTrackbarPos("lower_value","bars")
    lower_hue=cv2.getTrackbarPos("lower_hue","bars")
    lower_saturation=cv2.getTrackbarPos("lower_saturation","bars")
    
    kernel=np.ones((3,3),np.int8)
    
    upper_hsv=np.array([upper_hue,upper_saturation,upper_value])
    lower_hsv=np.array([lower_hue,lower_saturation,lower_value])
    
    #Creates a mask
    #In the kernel range - white and othes all black
    mask=cv2.inRange(inspect,lower_hsv,upper_hsv)
    
    mask=cv2.medianBlur(mask,3)
    mask_inv=255-mask
    mask=cv2.dilate(mask,kernel,5)
    
    b= frame[:,:,0]
    g = frame[:,:,1]
    r = frame[:,:,2]
    b = cv2.bitwise_and(mask_inv, b)
    g = cv2.bitwise_and(mask_inv, g)
    r = cv2.bitwise_and(mask_inv, r)
    frame_inv = cv2.merge((b,g,r))

    b = init_frame[:,:,0]
    g = init_frame[:,:,1]
    r = init_frame[:,:,2]
    b = cv2.bitwise_and(b,mask)
    g = cv2.bitwise_and(g,mask)
    r = cv2.bitwise_and(r,mask)
    blanket_area = cv2.merge((b,g,r))
    
    final = cv2.bitwise_or(frame_inv, blanket_area)

    cv2.imshow("Harry's Cloak",final)

    if(cv2.waitKey(3) == ord('q')):
        break;

cv2.destroyAllWindows()
cap.release()
        
    
    
    
    
    
    
    
    
    
    
    
    
    

