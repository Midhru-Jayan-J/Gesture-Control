import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam,hcam=640,488
cTime=0
Ptime=0
vol=0
volBar=0

cap=cv2.VideoCapture(0)
cap.set(3,wcam)
cap.set(4,hcam)

detector=htm.handDetector(detectionCon=0.75)



devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volume_range=volume.GetVolumeRange()

min_vol=volume_range[0]
max_vol=volume_range[1]





while True:
    success,img=cap.read()
    img = detector.findHands(img)
    lmlist=detector.findPosition(img,draw=False)
    
    if len(lmlist) !=0: 
        x1,y1=lmlist[4][1],lmlist[4][2]
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2
        
        
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),8,(255,0,255),cv2.FILLED)
        
        length=math.hypot(x2-x1,y2-y1)
        #print(length)     
        
        # Hand Range -> 50 to 300
        # Volume Range tested -> -96 to 0
        vol=np.interp(length,[50,300],[min_vol,max_vol])
        volBar=np.interp(length,[50,300],[0,max_vol])
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        
        if length <=50:
            cv2.circle(img,(cx,cy),8,(0,255,0),cv2.FILLED)
               
        
        
    
    
    cTime=time.time()
    fps=1/(cTime-Ptime)
    Ptime=cTime
    
    
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    
    cv2.imshow("Img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    