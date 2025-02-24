import numpy as np
import cv2 

def same(x):
    pass  # No need for print statements

# Open webcam
cap = cv2.VideoCapture(0)

# Create trackbars for HSV threshold tuning
cv2.namedWindow("bars")
cv2.createTrackbar("upper_hue", "bars", 130, 180, same)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, same)
cv2.createTrackbar("upper_value", "bars", 255, 255, same)
cv2.createTrackbar("lower_hue", "bars", 90, 180, same)
cv2.createTrackbar("lower_saturation", "bars", 50, 255, same)
cv2.createTrackbar("lower_value", "bars", 50, 255, same)

# Capture initial background frame
while True:
    cv2.waitKey(2000)
    ret, init_frame = cap.read()
    if ret:
        init_frame = cv2.GaussianBlur(init_frame, (5, 5), 0)  # Smooth the initial frame
        break

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get HSV values from trackbars
    upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
    upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
    upper_value = cv2.getTrackbarPos("upper_value", "bars")
    lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
    lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")
    lower_value = cv2.getTrackbarPos("lower_value", "bars")

    # Define upper and lower HSV range for blue detection
    lower_hsv = np.array([lower_hue, lower_saturation, lower_value])
    upper_hsv = np.array([upper_hue, upper_saturation, upper_value])

    # Create mask to detect blue color
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Apply Gaussian blur to reduce noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Apply morphological operations to remove noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)  # Remove noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel, iterations=1)  # Expand mask slightly

    # Create inverse mask
    mask_inv = cv2.bitwise_not(mask)

    # Convert masks to 3 channels for bitwise operations
    mask_3ch = cv2.merge([mask, mask, mask])
    mask_inv_3ch = cv2.merge([mask_inv, mask_inv, mask_inv])

    # Use bitwise operations to blend frames
    frame_inv = cv2.bitwise_and(frame, mask_inv_3ch)
    cloak_area = cv2.bitwise_and(init_frame, mask_3ch)
    final = cv2.addWeighted(frame_inv, 1, cloak_area, 1, 0)  # Blend images properly

    # Display result
    cv2.imshow("Harry's Cloak", final)

    if cv2.waitKey(3) == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
