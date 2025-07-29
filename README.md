# Virtual-Mouse-Using-Python
🖱️ Virtual Mouse Using Hand Gestures
Control your computer mouse with your hands — no hardware needed beyond a webcam!
This project uses OpenCV, MediaPipe, and PyAutoGUI to turn your webcam into a gesture-based mouse controller.

🔍 Project Description
The Virtual Mouse lets you:

🖐️ Move the mouse cursor using your index finger.

👆 Left-click with a specific hand gesture.

🤚 Right-click with another gesture.

✌️ Double-click with a combined gesture.

✊ Take a screenshot by closing your fist.

This is a fun and intuitive way to interact with your computer using just your hands and your webcam.

🛠️ Features
Gesture	Action
Move index finger	Move mouse
Index + Middle finger pinch	Left-click
Thumb + Middle finger pinch	Right-click
Index + Middle finger pinch + close	Double-click
Closed Fist	Screenshot

(Gesture detection is based on hand landmark angles and distances using MediaPipe.)

🧰 Technologies Used
Python

OpenCV

MediaPipe

PyAutoGUI

pynput

🖥️ How It Works
Uses your webcam feed to detect hand landmarks (via MediaPipe).

Calculates angles and distances between fingers to interpret gestures.

Maps finger tip coordinates to screen dimensions to move the cursor.

Executes system-level mouse actions with pyautogui and pynput.

🚀 How to Run
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/AbhijitRai2003/virtual-mouse.git
cd virtual-mouse
2. Install Dependencies
bash
Copy
Edit
pip install opencv-python mediapipe pynput pyautogui numpy
3. Run the Application
bash
Copy
Edit
python app.py
📌 Press Q to quit the application.

📁 Project Structure
bash
Copy
Edit
virtual-mouse/
│
├── app.py        # Main script with gesture recognition and actions
├── util.py       # Utility functions for angle and distance calculations
└── README.md     # Project overview

🙌 Credits
Developed by [Abhijit Rai]
Inspired by gesture-controlled interfaces using computer vision.

