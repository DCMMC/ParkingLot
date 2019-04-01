## 1. 主要功能

* 设置背景图作为绘制蓝本
* 可以鼠标左键拖拽移动 building, room 等
* 空格+鼠标左键移动画布
* 导出 json

## 2. 编译

### 2.1 依赖

* `Qt5`
* `CMake`
* `make`

```bash
$ cmake . && make -j5 && ./ParkingLotEditor
```

## 3. TODOs

* 字体问题
* 修复鼠标右键设为xxx
* 精简无用功能
* room 类型: 墙体, 车位, etc.