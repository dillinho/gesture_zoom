import cv2
import mediapipe as mp
import math
import numpy as np

from functions import *

def run():

    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    screen_not_captured = True
    # For webcam input:
    cap = cv2.VideoCapture(0)
    lastDist = 0
    with mp_hands.Hands(
            #max_num_hands=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            if results.multi_hand_landmarks:
                #for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
                lmList = lm_position_list(results, image)
                image = draw_lmList(image, lmList, [4, 8])

                if screen_not_captured:
                    img = capture_screen()
                    screen_not_captured = False

                x, y = lmList[8][0], lmList[8][1]
                img_z = zoom_in_screenshot(img, x, y, 1000, 500)

                #show_screenshot(img_z)


            # lastDist = zoom(lmList, lastDist)

            else:
                screen_not_captured = True
                cv2.destroyWindow("detail")
                #cv2.destroyWindow("screen")
                #cv2.destroyWindow("boxed")


            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow('MediaPipe Hands', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
            # if capture_gesture_detected():




if __name__ == "__main__":
    run()


