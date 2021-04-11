import cv2
import math
import numpy as np
from PIL import ImageGrab


def capture_screen():
    pil_img = ImageGrab.grab(bbox=None)
    img = np.array(pil_img)
    print(img.shape)
    return img


def zoom_in_screenshot(img, x, y, size_x, size_y):

    offset_x = 100
    offset_y = 100

    x_finger = x
    y_finger = y

    x = x - offset_x
    y = y - offset_y

    y_min = np.max([1, x])
    y_max = np.min([x+size_x, img.shape[1]])
    x_min = np.max([1, y])
    x_max = np.min([y+size_y, img.shape[0]])

    img_detail = img[x_min:x_max, y_min:y_max]

    img_detail = cv2.resize(img_detail, (img.shape[1], img.shape[0]))
    img_boxed = img.copy()
    img_boxed = cv2.rectangle(img_boxed, (y_min, x_min), (y_max, x_max), (0, 0, 255), 10)
    img_boxed = cv2.circle(img_boxed, (x_finger, y_finger), 15, (0, 0, 255), cv2.FILLED)
    a = 4
    w, h = int(img.shape[1]/a), int(img.shape[0]/a)

    img_boxed = cv2.resize(img_boxed, (w, h))
    print(img.shape[0])
    print(img.shape[1])
    print(img_boxed.shape[0])
    print(img_boxed.shape[1])
    print(img.shape[1] - img_boxed.shape[1])

    print(img_detail[img.shape[0] - img_boxed.shape[0]-1:img.shape[0]-1, img.shape[1] - img_boxed.shape[1]-1:img.shape[1]-1].shape)
    img_detail[img.shape[0] - img_boxed.shape[0] - 1:img.shape[0] - 1, img.shape[1] - img_boxed.shape[1] - 1:img.shape[1] - 1] = img_boxed

    cv2.imshow('detail', img_detail)


def lm_position_list(results, img, handNo=0):
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
        # img = np.zeros_like(img)
        cv2.circle(img, (lmList[idx][0], lmList[idx][1]), 7, (255, 0, 255), cv2.FILLED)
    return img

def zoom(lmList,lastDist,idx2consider4activate_zoom = 8):
    x1, y1 = lmList[4][1], lmList[4][2]
    x2, y2 = lmList[8][1], lmList[8][2]
    currentDist = math.hypot(x2 - x1, y2 - y1)
    if lmList[idx2consider4activate_zoom][2] < -0.2:
        if currentDist - lastDist > 4:
            print("ctrl +")
        elif currentDist - lastDist < -4:
            print("ctrl -")
        else:
            print("active but no zoom")
    else:
        print("Not active ({})".format(lmList[idx2consider4activate_zoom][2]))
    return currentDist