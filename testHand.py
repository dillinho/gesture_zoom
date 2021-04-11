import cv2
import mediapipe as mp
import math
from pynput.keyboard import Key, Controller
keyboard = Controller()


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def lmPositionList(results,img,handNo=0):
    lmList = []
    if results.multi_hand_landmarks:
        myHand = results.multi_hand_landmarks[handNo]
        for id, lm in enumerate(myHand.landmark):
            # print(id, lm)
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print(id, cx, cy)
            lmList.append([cx, cy, lm.z])
            # if draw:
            #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

    return lmList

def draw_lmList(img,lmList,idx2draw):
    for idx in idx2draw:
        cv2.circle(img, (lmList[idx][0], lmList[idx][1]), 7, (255, 0, 255), cv2.FILLED)
        # print(lmList[idx][2])

def zoom(lmList,lastDist,idx2consider4activate_zoom = 8):
    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
    currentDist = math.hypot(x2 - x1, y2 - y1)
    if lmList[idx2consider4activate_zoom][2] < -0.2:
        if currentDist - lastDist > 4:
            with keyboard.pressed(Key.ctrl):
                keyboard.press('+')
                print("ctrl +")
        elif currentDist - lastDist < -4:
            with keyboard.pressed(Key.ctrl):
                keyboard.press('-')
                print("ctrl -")
        else:
            print("active but no zoom")
    else:
        print("Not active ({})".format(lmList[idx2consider4activate_zoom][2]))
    return currentDist


# For webcam input:
cap = cv2.VideoCapture(0)
lastDist = 0
with mp_hands.Hands(
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
      for hand_landmarks in results.multi_hand_landmarks:

        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        lmList = lmPositionList(results,image)
        draw_lmList(image, lmList, [4,8])

        lastDist = zoom(lmList, lastDist)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()