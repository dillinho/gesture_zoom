import cv2
import numpy as np
import mediapipe as mp

from functions import *


def run():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    screen_not_captured = True
    window_name = "Screenshot"

    # For webcam input:
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        # max_num_hands=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
    ) as hands:
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

            if results.multi_hand_landmarks:  # min one hand in image detected

                # draw found hand-landmarks and the connections in the image from the cam
                mp_drawing.draw_landmarks(image, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)

                if screen_not_captured:
                    cv2.waitKey(5)
                    img = capture_screen()
                    cv2.waitKey(5)
                    screen_not_captured = False
                    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                zoom_in_screenshot(img, results, mp_hands, mp_drawing, 1000, 500, window_name)

            else:  # no hand in image detected
                screen_not_captured = True
                cv2.destroyWindow(window_name)

            # show image from cam in separate window
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow("MediaPipe Hands", image)

            # shutdown when pressing esc
            if cv2.waitKey(50) & 0xFF == 27:
                break

    cap.release()


if __name__ == "__main__":
    run()
