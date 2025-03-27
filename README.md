Hand Gesture Recognition Using AI - Virtual Mouse

Introduction
 This project enables gesture-based control of a computer using a webcam. 

It leverages OpenCV, MediaPipe, and PyAutoGUI to detect hand gestures and perform actions like
 mouse movement, clicks, zooming, and screenshots.
 Features- Move the cursor using the index finger.- Left-click with the index finger extended.- Right-click with the index and middle fingers extended.- Take a screenshot when all fingers are extended.- Zoom in and out using thumb and index finger distance.

 Installation
 1. Install Python (>=3.7).
 2. Install required libraries using:
   ```
   pip install opencv-python mediapipe pyautogui numpy
   ```
 3. Run the script:
   ```
   python gesture_control.py
   ```
 Usage- Ensure the webcam is connected and running.- Perform gestures to control the cursor and execute actions.- Press 'q' to exit the program.
 Hand Landmarks
 
 The program uses the following hand landmarks (from MediaPipe) for gesture recognition:- Index Finger Tip (8)
- Middle Finger Tip (12)- Ring Finger Tip (16)- Pinky Finger Tip (20)- Thumb Tip (4)

 How It Works
 1. The webcam captures hand movements.
 2. MediaPipe detects hand landmarks and tracks fingers.
 3. Specific gestures trigger actions like clicks, zoom, and screenshots.
 4. PyAutoGUI translates gestures into system commands.
 
 Troubleshooting- Ensure all dependencies are installed correctly.- Run the script in a well-lit environment for better gesture detection.- If cursor movement is slow, adjust webcam resolution.
 Conclusion
 
 This project demonstrates how computer vision and AI can enable touchless interaction with
 computers.
 Future improvements could include more gesture controls and support for multiple users.
