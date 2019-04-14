#!/bin/env python3
"""
对 HyperLPR 车牌识别的封装, 便于后期迁移到其他框架
"""
import time
import os
import HyperLPRLite as pr
import cv2

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

model = None


def init():
    global model
    model = pr.LPR(os.path.join(BASE_PATH, "model/cascade.xml"),
                   os.path.join(BASE_PATH, "model/model12.h5"),
                   os.path.join(BASE_PATH, "model/ocr_plate_all_gru.h5"))


def recognize_single_image(file_full_path, threshold=0.7):
    '''
    判断图片中的车单个车牌号(暂定面积最大的那一张)
    @param file_full_path 图片文件的完整路径
    @param threshold 只考虑置信度 >= 0.7 的结果
    @return 返回判断结果的车牌号的字符串, 并且
            只返回一个车牌号, 包括车牌号, 置信度,
            还有判断矩形的三元组, 如果 文件不存在
            或者其他错误, 返回空 list
    '''
    # test
    # file_full_path = os.path.join(BASE_PATH, "images_rec/1.jpg")
    if not os.path.isfile(file_full_path):
        return []
    area = lambda w, h: h * w # noqa
    start = time.time()
    grr = cv2.imread(file_full_path)
    results = model.SimpleRecognizePlateByE2E(grr)
    interval = time.time() - start
    print('花费: {}s'.format(interval))
    rect_area = 0
    evl = []
    for pstr, confidence, rect in results:
        # rect 是一个四元组: 左上角坐标的 x, y 和 矩形的宽度和高度
        if confidence >= threshold and rect_area < area(rect[2], rect[3]):
            # debug
            print('rect:')
            print(rect)
            print("plate_str:")
            print(pstr)
            print("plate_confidence")
            print(confidence)
            evl = [pstr, confidence, rect]
            rect_area = area(rect[2], rect[3])
    return evl


def recognize_multi_image(files_full_paths):
    """
    TODO:
    同时识别多张照片已提高精度
    """
    pass


if __name__ == '__main__':
    # Test
    print(recognize_single_image(os.path.join(BASE_PATH, "images_rec/1.jpg")))
    print(recognize_single_image(BASE_PATH))
