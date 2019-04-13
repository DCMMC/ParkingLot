# HyperLPR 作为 Django 的一个 instance app,
# 该 tasks.py 声明所有的 Celery 定时任务,
# 并且会被 `parking_lot/parking_lot/__init__.py`
# 中的 autodiscover_tasks 自动发现并导入 Celery
from __future__ import absolute_import, unicode_literals
from celery import shared_task
# 必须先用 import 来执行 lpr_provider 的加载 tensorflow 和 keras 的操作
# 因为加载比较慢
import lpr_provider
from camera_provider import camera_provider
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# 为了避免资源消耗, 我们可以基于一辆车至少在一个出入口停留
# 5s 以上(肯定超过 5s) 的先验知识, 在每一次成功识别到车牌信息的
# 的时候, 等待 5s 钟
count_down = 0
# 上一次成功识别的车牌号
# TODO: 突然想起来, 如果出入口有车过来又倒车走了,
# 那么就会出问题了诶, 而且管理员界面应该加一个
# 有权手动修改停车场内车辆信息的功能
last_pstr = ''


# The @shared_task decorator lets you create tasks without
# having any concrete app instance:
@shared_task
def indoorCameraRecognize(indoorNum='1'):
    """
    调用 indoorNum 入口处摄像头并扫描车牌
    一个树莓派 Camera 实例一个识别任务(要么是 indoor 要么是 outdoor)
    """
    image_abspath = camera_provider()
    global count_down
    global last_pstr
    if image_abspath is not None:
        if count_down == 0:
            evl = lpr_provider.recognize_single_image(image_abspath)
            if len(evl) == 0:
                # TODO: 记录日志
                # 也可能是其他非车辆实体触碰
                print('{} 号入口车牌识别未达到精度或出现问题'.format(indoorNum))
            else:
                pstr = evl[0]
                confidence = evl[1]
                print('{} 号入口车牌识别结果: {} 精度 {}'.format(
                    indoorNum, pstr, confidence))
                count_down = 5
                if last_pstr != pstr:
                    last_pstr = pstr
                    # TODO: 数据库更新
                else:
                    # 同一辆车
                    pass
                # TODO: 从数据库中获取该车辆有关信息
                # 不管是不是发现是用一辆车, 都要发一次 ws 数据包,
                # 因为 ws 数据包有可能发送失败
                # TODO: 还可以使用其他健壮性更好地错误处理方案
                # 获取 redis 中存储的 channel layer
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'indoor_{}'.format(indoorNum),
                    {
                        # 这个 type 是 Consumer 中的一个 Listen method
                        # 这个 group_send 就是向该 group 下所有 Consumers
                        # 发送一个以这个字典作为数据的 event 给 consumers
                        # 中 type 指定的 method, 注意: type 中的 `.` 会被
                        # 替换为 `_`
                        'type': 'indoor_discover_license_plate',
                        # 后面的这些字段将会被 wrap 到 event
                        'message': json.dumps({
                            'pstr': pstr,
                            # 其他从数据库中获取的数据
                        })
                    }
                )
        else:
            # 倒计时
            count_down -= 1

    else:
        # print('暂无车辆在停车场出入口')
        # 置零, 防止倒计时还没技术就没有车辆在出入口了
        count_down = 0


@shared_task
def outdoorCameraRecognize(outdoorNum='1'):
    """
    调用 outdoorNum 入口处摄像头并扫描车牌
    """
    image_abspath = camera_provider()
    if image_abspath is not None:
        evl = lpr_provider.recognize_single_image(image_abspath)
        if len(evl) == 0:
            # TODO: 记录日志
            print('{} 号出口车牌识别未达到精度或出现问题'.format(outdoorNum))
        else:
            pstr = evl[0]
            confidence = evl[1]
            print('{} 号出口车牌识别结果: {} 精度 {}'.format(
                outdoorNum, pstr, confidence))
    else:
        # print('暂无车辆在停车场出入口')
        pass
