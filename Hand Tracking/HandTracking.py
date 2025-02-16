## MediaPipe
## OpenCV

import cv2
import mediapipe as mp
import custom_hands
import time

cap = cv2.VideoCapture(0) 

mpHands=mp.solutions.hands
hands = custom_hands.Hands()

pTime=0
cTime=0

while True:
    success, img = cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    mpDraw=mp.solutions.drawing_utils # Drawing the hand points
    
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            for id,lm in enumerate(handLMS.landmark):
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=  int(lm.x*w),int(lm.y*h)
                if id==0:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
                
                
                
            mpDraw.draw_landmarks(img,handLMS,mpHands.HAND_CONNECTIONS )# mpHands.HAND_CONNECTIONS-To draw line between connectiong points
            
    
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
    

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()
