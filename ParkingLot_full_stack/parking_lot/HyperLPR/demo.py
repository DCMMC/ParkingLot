#!/bin/env python3
import time
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import HyperLPRLite as pr
import cv2
import numpy as np

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def SpeedTest(image_path):
    grr = cv2.imread(image_path)
    model = pr.LPR(os.path.join(BASE_PATH, "model/cascade.xml"),
                   os.path.join(BASE_PATH, "model/model12.h5"),
                   os.path.join(BASE_PATH, "model/ocr_plate_all_gru.h5"))
    model.SimpleRecognizePlateByE2E(grr)
    t0 = time.time()
    for x in range(20):
        model.SimpleRecognizePlateByE2E(grr)
    t = (time.time() - t0)/20.0
    print("Image size :" + str(grr.shape[1]) +
          "x"+str(grr.shape[0]) + " need " +
          str(round(t*1000, 2))+"ms")


fontC = ImageFont.truetype(os.path.join(BASE_PATH,
                                        "Font/platech.ttf"), 14, 0)


def drawRectBox(image, rect, addText):
    cv2.rectangle(image, (int(rect[0]),
                          int(rect[1])), (int(rect[0] + rect[2]),
                                          int(rect[1] + rect[3])),
                  (0, 0, 255), 2, cv2.LINE_AA)
    cv2.rectangle(image, (int(rect[0]-1), int(rect[1])-16),
                  (int(rect[0] + 115), int(rect[1])), (0, 0, 255), -1,
                  cv2.LINE_AA)
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.text((int(rect[0]+1), int(rect[1]-16)), addText, (255, 255, 255),
              font=fontC)
    imagex = np.array(img)
    return imagex


model = pr.LPR(os.path.join(BASE_PATH, "model/cascade.xml"),
               os.path.join(BASE_PATH, "model/model12.h5"),
               os.path.join(BASE_PATH, "model/ocr_plate_all_gru.h5"))

# SpeedTest("images_rec/2.jpg")


def demo():
    grr = cv2.imread(os.path.join(BASE_PATH, "images_rec/1.jpg"))
    for pstr, confidence, rect in model.SimpleRecognizePlateByE2E(grr):
        if confidence > 0.7:
            # image = drawRectBox(grr, rect, pstr+" " +
            #                     str(round(confidence, 3)))
            print("plate_str:")
            print(pstr)
            print("plate_confidence")
            print(confidence)
            # cv2.imshow("image", image)
            # 按任意键继续
            # cv2.waitKey(0)

    grr = cv2.imread(os.path.join(BASE_PATH, "images_rec/2.jpg"))
    for pstr, confidence, rect in model.SimpleRecognizePlateByE2E(grr):
        if confidence > 0.7:
            # image = drawRectBox(grr, rect, pstr+" " +
            #                     str(round(confidence, 3)))
            print("plate_str:")
            print(pstr)
            print("plate_confidence")
            print(confidence)
            # cv2.imshow("image", image)
            # 按任意键继续
            # cv2.waitKey(0)
