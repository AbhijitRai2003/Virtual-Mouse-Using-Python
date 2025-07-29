import random
import cv2
import mediapipe as mps
import util
import pyautogui
from pynput.mouse import Button, Controller
mouse=Controller()
screen_width,screen_height = pyautogui.size()
mpsHand = mps.solutions.hands
hands=mpsHand.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1   
)

def find_finger_tip(p_output):
    if p_output.multi_hand_landmarks:
        hand_landmarks=p_output.multi_hand_landmarks[0]
        return hand_landmarks.landmark[mpsHand.HandLandmark.INDEX_FINGER_TIP]
    
    return None

def left_click(landmark_list,thumb_index_dist):
    return (util.cal_angle(landmark_list[5],landmark_list[6],landmark_list[8])<50 and util.cal_angle(landmark_list[9],landmark_list[10],landmark_list[12])>90  and thumb_index_dist > 50)

def right_click(landmark_list,thumb_index_dist):
    return (util.cal_angle(landmark_list[9],landmark_list[10],landmark_list[12])<50 and util.cal_angle(landmark_list[5],landmark_list[6],landmark_list[8])>90  and thumb_index_dist > 50)

def double_click(landmark_list,thumb_index_dist):
    return (util.cal_angle(landmark_list[5],landmark_list[6],landmark_list[8])<50 and util.cal_angle(landmark_list[9],landmark_list[10],landmark_list[12])<50  and thumb_index_dist > 50)

def is_fist_closed(landmark_list):
    # Check if landmarks are detected
    if not landmark_list or len(landmark_list) != 21:
        return False

    # Thumb: tip is index 4, check against index 2 (knuckle)
    thumb_tip = landmark_list[4][0]
    thumb_knuckle = landmark_list[2][0]

    # Fingers: tip index > pip joint index means finger is down (for y-coordinate)
    finger_states = []
    finger_tips = [8, 12, 16, 20]  # index, middle, ring, pinky
    finger_pips = [6, 10, 14, 18]  # corresponding PIP joints

    for tip, pip in zip(finger_tips, finger_pips):
        if landmark_list[tip][1] > landmark_list[pip][1]:  # y increases downward
            finger_states.append(True)
        else:
            finger_states.append(False)

    # For thumb, compare x (horizontal direction for right hand)
    thumb_closed = thumb_tip < thumb_knuckle

    # Return True if all fingers + thumb are closed
    return all(finger_states) and thumb_closed

def screenshot(landmark_list,thumb_index_dist):
    return (util.cal_angle(landmark_list[5],landmark_list[6],landmark_list[8])<50 and util.cal_angle(landmark_list[9],landmark_list[10],landmark_list[12])<50  and thumb_index_dist < 50)

def detect_gestures(frame, landmark_list,p_output):
    if len(landmark_list)>=21:
        
        index_finger_tip= find_finger_tip(p_output)
        thumb_index_distance= util.cal_distance([landmark_list[4], landmark_list[5]])
        
        if thumb_index_distance < 50 and util.cal_angle(landmark_list[5],landmark_list[6],landmark_list[8]) >90:
            move_mouse(index_finger_tip)
        
        #For Left Click
        elif left_click(landmark_list,thumb_index_distance):
            mouse.press(Button.left)
            mouse.release(Button.left)
            cv2.putText(frame,"Left Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        #Right Click
        elif right_click(landmark_list,thumb_index_distance):
            mouse.press(Button.right)
            mouse.release(Button.right)
            cv2.putText(frame,"Right Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        #Double Click
        elif double_click(landmark_list,thumb_index_distance):
            pyautogui.doubleClick()
            cv2.putText(frame,"Double Click", (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)
        #Screenshot
        elif screenshot(landmark_list,thumb_index_distance):
            im1 = pyautogui.screenshot()
            label = random.randint(1,1000)
            im1.save(f'Screenshot_{label}.png')
            cv2.putText(frame,"Screenshot_Snapped", (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2)
def move_mouse(index_finger_tip):
    if index_finger_tip is not None:
        x = int(index_finger_tip.x * screen_width)
        y = int(index_finger_tip.y * screen_height)
        pyautogui.moveTo(x,y)
 
def main():
    caps= cv2.VideoCapture(0)
    draw= mps.solutions.drawing_utils
    
    try:
        while caps.isOpened():
            ret, frame = caps.read()
            
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            frameRGB= cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            
            p_output= hands.process(frameRGB)
            
            landmark_list=[]
            
            if p_output.multi_hand_landmarks:
                hand_landmarks=p_output.multi_hand_landmarks[0]
                draw.draw_landmarks(frame,hand_landmarks,mpsHand.HAND_CONNECTIONS)
                
                for lm in hand_landmarks.landmark:
                    landmark_list.append((lm.x, lm.y))
            
            detect_gestures(frame, landmark_list,p_output)
                    
            print(landmark_list)
            
            cv2.imshow('Frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    finally: 
        caps.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    main()
