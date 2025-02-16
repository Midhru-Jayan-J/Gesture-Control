import cv2
import HandTrackingModule as htm
import numpy as np
import time
import math
import pyautogui
import threading

# Camera Dimensions (Lowered for Better Performance)
wcam, hcam = 320, 240
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)

# Hand Detector
detector = htm.handDetector(detectionCon=0.8)

# Screen Dimensions
screenWidth, screenHeight = pyautogui.size()

# Cursor Position & Smoothening
smoothening = 5
prev_x, prev_y = 0, 0

# Click & Scroll Control Variables
left_click_active = False
right_click_active = False
last_click_time = 0
click_delay = 0.3
scroll_speed = 2
prev_index_thumb = None

# FPS Calculation Variables
cTime = 0
pTime = 0
frame_skip = 2  # Process every 2nd frame
frame_count = 0

def move_cursor(x, y):
    """ Move cursor smoothly using EMA """
    global prev_x, prev_y
    x = prev_x + (x - prev_x) / smoothening
    y = prev_y + (y - prev_y) / smoothening
    pyautogui.moveTo(x, y, duration=0.05)
    prev_x, prev_y = x, y

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)

    if frame_count % frame_skip == 0 and len(lmlist) != 0:
        # Index Finger
        x11, y11 = lmlist[8][1], lmlist[8][2]
        x12, y12 = lmlist[7][1], lmlist[7][2]

        # Middle Finger
        x21, y21 = lmlist[12][1], lmlist[12][2]
        x22, y22 = lmlist[11][1], lmlist[11][2]

        # Ring Finger
        x31, y31 = lmlist[16][1], lmlist[16][2]
        x32, y32 = lmlist[15][1], lmlist[15][2]

        # Thumb
        x4, y4 = lmlist[4][1], lmlist[4][2]

        # Length Calculations
        index_middle1 = math.hypot(x21 - x11, y21 - y11)
        index_middle2 = math.hypot(x22 - x12, y22 - y12)

        middle_ring1 = math.hypot(x31 - x21, y31 - y21)
        middle_ring2 = math.hypot(x32 - x22, y32 - y22)

        index_thumb = math.hypot(x4 - x11, y4 - y11)

        # Convert Coordinates to Screen Mapping
        x = np.interp(x11, [0, wcam], [0, screenWidth])
        y = np.interp(y11, [0, hcam], [0, screenHeight])

        # 1️⃣ Mouse Movement (Smoothened)
        if middle_ring1 > 50 and middle_ring2 > 50:
            threading.Thread(target=move_cursor, args=(x, y)).start()

        # 2️⃣ Left Click (Prevent False Positives)
        if index_middle1 < 40 and index_middle2 < 40:
            if not left_click_active and time.time() - last_click_time > click_delay:
                pyautogui.click()
                left_click_active = True
                last_click_time = time.time()
        else:
            left_click_active = False

        # 3️⃣ Right Click (Adaptive Threshold)
        if abs(index_middle1 - middle_ring1) < 40:
            if not right_click_active and time.time() - last_click_time > click_delay:
                pyautogui.rightClick()
                right_click_active = True
                last_click_time = time.time()
        else:
            right_click_active = False

        # 4️⃣ Scrolling (Smooth Velocity-Based)
        if index_thumb < 80:
            if prev_index_thumb is not None:
                scroll_movement = (index_thumb - prev_index_thumb) * scroll_speed

                if abs(scroll_movement) > 5:
                    pyautogui.scroll(int(scroll_movement))

            prev_index_thumb = index_thumb

    frame_count += 1  # Frame skipping for efficiency

    # FPS Calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'{int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 2)

    # Show Image
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
