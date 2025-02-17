import cv2
import HandTrackingModule as htm
import numpy as np 
import time
import math
import pyautogui

wcam=640
hcam=488
cTime=0
pTime=0
screenWidth, screenHeight = pyautogui.size()# Returns two integers, the width and height of the screen. (The primary monitor, in multi-monitor setups.)
#print(screenWidth, screenHeight)
x,y = pyautogui.position() # Returns two integers, the x and y of the mouse cursor's current position.

# pyautogui.moveTo(100, 150) # Move the mouse to the x, y coordinates 100, 150.
# pyautogui.click() # Click the mouse at its current location.
# pyautogui.click(200, 220) # Click the mouse at the x, y coordinates 200, 220.
# pyautogui.move(None, 10)  # Move mouse 10 pixels down, that is, move the mouse relative to its current position.
# pyautogui.doubleClick() # Double click the mouse at the
# pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # Use tweening/easing function to move mouse over 2 seconds.
# pyautogui.write('Hello world!', interval=0.25)  # Type with quarter-second pause in between each key.
# pyautogui.press('esc') # Simulate pressing the Escape key.
# pyautogui.keyDown('shift')
# pyautogui.write(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.hotkey('ctrl', 'c')

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

detector=htm.handDetector(detectionCon=0.8)  # Increased confidence to reduce false positives

prev_pinky_thumb = None
scroll_smooth = 0
right_click_active = False

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img)
    
    if len(lmlist)!=0:
        #index finger
        x11,y11=lmlist[8][1],lmlist[8][2]
        x12,y12=lmlist[7][1],lmlist[7][2]
        
        #middle finger
        x21,y21=lmlist[12][1],lmlist[12][2]
        x22,y22=lmlist[11][1],lmlist[11][2]
        
        #ring finger
        x31,y31=lmlist[16][1],lmlist[16][2]
        x32,y32=lmlist[15][1],lmlist[15][2]
        
        #thumb finger
        x4,y4=lmlist[4][1],lmlist[4][2]
        
        #pinky finger
        x5,y5=lmlist[20][1],lmlist[20][2]
        
        #Lengths
        index_middle1=math.hypot(x21-x11,y21-y11)
        index_middle2=math.hypot(x22-x12,y22-y12)
        
        middle_ring1=math.hypot(x31-x21,y31-y31)
        middle_ring2=math.hypot(x32-x22,y32-y22)
        
        index_thumb=math.hypot(x4-x11,y4-y11)
        pinky_thumb=math.hypot(x5-x4,y5-y4)  # Distance between pinky and thumb
        
        #print(index_middle1,index_middle2,middle_ring1,middle_ring2,index_thumb)
        #print(x11,y11)  
        
        #Pixel Position wrt to screen
        x=np.interp(x11,[0,640],[1920,0])
        y=np.interp(y11,[0,488],[0,1080])
        
        # Mouse Movement
        if middle_ring1<50 and middle_ring2<50 and index_thumb>100:
            pyautogui.moveTo(x, y)

        # Left Click (Debounced for Stability)
        if index_middle1<50 and index_middle2<50:
            pyautogui.click()
            time.sleep(0.1)  # Prevents multiple unwanted clicks
        
        # Right Click (Debounced)
        if index_middle1<50 and middle_ring1<50 and middle_ring2<50:
            if not right_click_active:
                pyautogui.rightClick()
                right_click_active = True
        else:
            right_click_active = False  # Reset when fingers are apart
        
        # Smooth Scrolling Using Pinky & Thumb Finger Distance
        if prev_pinky_thumb is not None:
            scroll_movement = pinky_thumb - prev_pinky_thumb

            # Apply smoothing for better control
            scroll_smooth = 0.8 * scroll_smooth + 0.2 * scroll_movement
            
            # Scroll logic: Move pinky closer for up, move away for down
            if abs(scroll_smooth) > 5:
                pyautogui.scroll(50 if scroll_smooth > 0 else -50)
        
        prev_pinky_thumb = pinky_thumb

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
