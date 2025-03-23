def recognize_gesture(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Tips of the fingers
    thumb_tip = 4
    landmarks = hand_landmarks.landmark
    fingers = []

    for tip in finger_tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # Check if finger is up
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [0, 1, 0, 0]:  # Example: If only index finger is up
        return "Scrolling up..."
    
    return None  # No recognized gesture