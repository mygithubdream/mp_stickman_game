import cv2
import mediapipe as mp
import math
#import pyautogui

from ctypes import cdll
 
dll_pth="./py_c_call.dll"
dllObj = cdll.LoadLibrary(dll_pth)


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def exceedBorder(pos, threshW, threshH):
    if pos[0]>threshW or pos[0]<0 or pos[1]>threshH or pos[1]<0:
        return True
    return False

def detHands(image, result, l_hand_old):
    #print("detect")
    if result.pose_landmarks == None:
        print("result.pose_landmarks None")
        return
    
    height, width, _ = image.shape
    noseLandMark=result.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]
    nosePos=[noseLandMark.x*width, noseLandMark.y*height]

    l_hand_lmrk = (result.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].x * width,
                        result.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST].y * height)
    
    #print(l_hand_lmrk, width, height)
    if (exceedBorder(l_hand_lmrk, width, height)):
        return
    r_hand_lmrk = (result.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].x * width,
                        result.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST].y * height)
    if (exceedBorder(r_hand_lmrk, width, height)):
        return
    
    l_r_dist = int(math.hypot(l_hand_lmrk[0] - r_hand_lmrk[0],
                              l_hand_lmrk[1] - r_hand_lmrk[1]))
    
    #print(l_hand_lmrk, width)
    if l_r_dist > 20 and l_r_dist<100: #left and right hand distance
        #print("l_r_dist > 50")
        if abs(l_hand_lmrk[0]-l_hand_old[0])>=10:
            l_hand_to_cent_dist=l_hand_lmrk[0]-nosePos[0]
            #print(l_hand_to_cent_dist, nosePos[0])
            if l_hand_to_cent_dist>10:
                #pyautogui.press(keys="right")
                dllObj.key_right();
                print("right-------")
            elif l_hand_to_cent_dist<-10:
                #pyautogui.press(keys="left")
                dllObj.key_left();
                print("-------left")
            else:
                #print("not recg")
                pass
            
        else:
            #print("abs < 20")
            pass
    else:
        #print("l_r_dist > 300")
        pass
        
    l_hand_old[0]=l_hand_lmrk[0]
    #else:
    #    print("not join")
        
cap = cv2.VideoCapture(0)
l_hand_old=[0]
l_pos_old=[0]
with mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        # Draw landmark annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Holistic StickMan Game', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
        detHands(image, results, l_hand_old)
        
cap.release()
