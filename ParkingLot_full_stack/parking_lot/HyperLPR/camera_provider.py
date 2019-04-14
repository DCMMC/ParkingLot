import random
import os
# celery 的 work 是多线程的, 所以 provider 必须
# 跨线程共享数据
from multiprocessing.sharedctypes import Value


# int
time_left = Value('i', 0)
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def camera_provider():
    """
    TODO:
    摄像头的抽象封装
    因为 *cameraRecognize() 是定时任务,
    然而每一次 tf 识别图像, 都需要 0.3 ~ 0.9s,
    所以如果可以的话, 可以额外加一个压感测试,
    如果没有车过来就不拍照了, 直接返回一个 None
    @return 返回图像所在的路径(绝对路径), 如果压感测试
            不通过(可选), 则返回 None
    """
    # 模拟
    global time_left
    print('剩余时间: ', time_left.value)
    if time_left.value > 0:
        time_left.value -= 1
        return os.path.join(BASE_PATH, 'images_rec',
                            str(random.randint(1, 2)) + '.jpg')
    elif random.random() > 0.98:
        print('车辆进入!')
        # 1/50 的概率, i.e., 50s 中有 1s 车来了, 并且将持续
        # 15 ~ 30s
        time_left.value = random.randint(15, 30)
    return None
