import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Track last action time and click state
last_action_time = time.time()
click_state = {"left": False, "right": False}

# Function to check if enough time has passed since the last action
def can_perform_action(cooldown=1.0):  # 1 second cooldown
    global last_action_time
    if time.time() - last_action_time > cooldown:
        last_action_time = time.time()
        return True
    return False

# Function to detect gestures and perform actions
def recognize_gesture(hand_landmarks, prev_gesture):
    global click_state
    finger_tips = [8, 12, 16, 20]  # Using correct indices from the image
    thumb_tip = 4

    landmarks = hand_landmarks.landmark
    fingers = []

    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # Check if finger is up
            fingers.append(1)
        else:
            fingers.append(0)

    # Move Mouse Cursor (Index Finger)
    index_finger = landmarks[8]  # Index finger tip
    cursor_x = int(index_finger.x * screen_width)  # Scale X to screen width
    cursor_y = int(index_finger.y * screen_height)  # Scale Y to screen height
    pyautogui.moveTo(cursor_x, cursor_y, duration=0.1)  # Move smoothly

    # Screenshot (All fingers up) with cooldown
    if fingers == [1, 1, 1, 1] and prev_gesture != "screenshot" and can_perform_action(2):
        pyautogui.screenshot("screenshot.png")
        print("Screenshot taken!")
        return "screenshot"

    # Left-click (Only index finger up)
    elif fingers == [0, 1, 0, 0]:
        if not click_state["left"]:  # Ensure it only clicks once
            pyautogui.click()
            print("Left Click")
            click_state["left"] = True
        return "left_click"

    # Right-click (Index and middle fingers up)
    elif fingers == [0, 1, 1, 0]:
        if not click_state["right"]:  # Ensure it only clicks once
            pyautogui.rightClick()
            print("Right Click")
            click_state["right"] = True
        return "right_click"

    # Reset click state when fingers are not in click position
    if fingers != [0, 1, 0, 0]:
        click_state["left"] = False
    if fingers != [0, 1, 1, 0]:
        click_state["right"] = False

    # Zoom in (Thumb tip closer to index finger tip)
    if abs(landmarks[thumb_tip].x - landmarks[8].x) < 0.05 and prev_gesture != "zoom_in" and can_perform_action(2):
        pyautogui.hotkey('ctrl', '+')
        print("Zooming In")
        return "zoom_in"

    # Zoom out (Thumb tip far from index finger tip)
    if abs(landmarks[thumb_tip].x - landmarks[8].x) > 0.2 and prev_gesture != "zoom_out" and can_perform_action(2):
        pyautogui.hotkey('ctrl', '-')
        print("Zooming Out")
        return "zoom_out"

    return prev_gesture  # Keep the previous gesture if no new one is detected

# Main loop for capturing webcam feed
previous_gesture = None  # Stores the last detected gesture

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Detect hands
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Recognize gesture and perform action
            previous_gesture = recognize_gesture(hand_landmarks, previous_gesture)

    # Display frame
    cv2.imshow("Gesture Control", frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()