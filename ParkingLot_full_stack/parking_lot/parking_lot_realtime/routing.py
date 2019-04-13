from django.urls import path

from . import consumers

websocket_urlpatterns = [  # 路由，指定 websocket 链接对应的 consumer
    # doorNum 是每一个出入口的标识码
    path('ws/indoor/<str:doorNum>/', consumers.IndoorConsumer),
    path('ws/outdoor/<str:doorNum>/', consumers.OutdoorConsumer),
    # 停车场出口管理员
    path('ws/admin/<str:outdoorNum>/', consumers.OutdoorAdminConsumer),
    # 停车场车位信息, 按楼层显示
    path('ws/parkingLotStatus/<str:layerNum>/',
         consumers.ParkingLotStatusConsumer)
]
