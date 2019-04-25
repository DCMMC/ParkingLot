import random
import os
import json
# celery 的 work 是多线程的, 所以 provider 必须
# 跨线程共享数据
from multiprocessing.sharedctypes import Value, Array


# int
time_left = Value('i', 0)
last_file = Array('c', bytes(' ' * 50, encoding="utf8"))
BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def camera_provider(local='indoor'):
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
    global last_file
    print('剩余时间: ', time_left.value)
    if time_left.value > 0:
        time_left.value -= 1
        last = str(last_file.value, encoding='utf8')
        return os.path.join(BASE_PATH, 'images_rec',
                            last) if last != '' else None
    elif random.random() > 0.9:
        # 1/50 的概率, i.e., 50s 中有 1s 车来了, 并且将持续
        # 15 ~ 30s
        time_left.value = random.randint(20, 40)
        obj = None
        with open(os.path.join(BASE_PATH, 'cars.json'), 'r') as f:
            obj = json.load(f)
        f_name = ''
        if local == 'indoor':
            if len(obj['out']) > 0:
                keys = list(obj['out'].keys())
                f_idx = keys[random.randint(0, len(keys) - 1)]
                f_name = obj['out'][f_idx]
                obj['in'][f_idx] = f_name
                print('####### 车辆 ' + f_name + ' 进入')
                del obj['out'][f_idx]
        else:
            # local == outdoor
            if len(obj['in']) > 0:
                keys = list(obj['in'].keys())
                f_idx = keys[random.randint(0, len(keys) - 1)]
                f_name = obj['in'][f_idx]
                obj['out'][f_idx] = f_name
                print('####### 车辆 ' + f_name + ' 出去')
                del obj['in'][f_idx]
        with open(os.path.join(BASE_PATH, 'cars.json'), 'w+') as f:
            json.dump(obj, f)
        last_file.value = bytes(f_name, encoding='utf8')
        return os.path.join(BASE_PATH, 'images_rec',
                            f_name) if f_name != '' else None
    return None
