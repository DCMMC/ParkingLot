import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class IndoorConsumer(AsyncJsonWebsocketConsumer):
    """
    入口处信息的 ws server
    主要是车牌信息
    发出信息来自于 HyperLPR 的 Celery tasks 中(可能处于其他的机器中, 分布式环境)
    下同
    """
    async def connect(self):
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.doorNum = self.scope['url_route']['kwargs']['doorNum']
            self.group_name = 'indoor_{}'.format(self.doorNum)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        print('IndoorConsumer 不需要接受信息, 丢弃: {}'.format(json.dumps(
            content)))

    async def indoor_discover_license_plate(self, event):
        """
        监听来自于 HyperLPR 的 Celery Tasks 的事件
        """
        await self.send_json(
            {
                # TODO: 到时候可以添加 status code 之类的信息
                'message': json.loads(event['message'])
            }
        )


class OutdoorConsumer(AsyncJsonWebsocketConsumer):
    """
    主要是车牌信息和收费信息
    """
    async def connect(self):
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.doorNum = self.scope['url_route']['kwargs']['doorNum']
            self.group_name = 'outdoor_{}'.format(self.doorNum)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('OutdoorConsumer 不需要接受信息, 丢弃: {}'.format(json.dumps(
            text_data_json)))


class OutdoorAdminConsumer(AsyncJsonWebsocketConsumer):
    """
    主要是收费信息
    """
    async def connect(self):
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.doorNum = self.scope['url_route']['kwargs']['outdoorNum']
            self.group_name = 'outdoor_admin_{}'.format(self.doorNum)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        print('OutdoorAdminConsumer 不需要接受信息, 丢弃: {}'.format(json.dumps(
            content)))


class ParkingLotStatusConsumer(AsyncJsonWebsocketConsumer):
    """
    停车场内停车位的占用信息更新
    """
    async def connect(self):
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.doorNum = self.scope['url_route']['kwargs']['layerNum']
            self.group_name = 'status_{}'.format(self.doorNum)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        print('ParkingLotStatusConsumer 不需要接受信息, 丢弃: {}'.format(json.dumps(
            content)))
