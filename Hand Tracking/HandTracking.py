## MediaPipe
## OpenCV

import cv2
import mediapipe as mp
import custom_hands
import time

cap = cv2.VideoCapture(0) 

hands = custom_hands.Hands()

while True:
    success, img = cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    mpDraw=mp.solutions.drawing_utils # Draing Line between points
    
    #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLMS in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img,handLMS)
            
    
    
    

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
