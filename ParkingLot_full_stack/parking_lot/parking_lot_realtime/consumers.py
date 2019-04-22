import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from db_pool import operations
import datetime


class IndoorConsumer(AsyncJsonWebsocketConsumer):
    group_name = None

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
            res = operations.getRecommParkings(indoor_id=self.doorNum)
            if res['code'] == 'success':
                res['code'] = 'recommand_parkings'
                await self.send_json(res)
            status = operations.getAllParkingStatus()
            if status['code'] == 'success':
                status['code'] = 'all_parkings_status'
                # status 有 used, unsed, unavailable,obligated
                await self.send_json(status)
            else:
                # TODO: 炒鸡严重的错误
                pass

    async def disconnect(self, close_code):
        if self.group_name is not None:
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
                'code': 'discover_license',
                # TODO: 到时候可以添加 status code 之类的信息
                'data': json.loads(event['message'])
            }
        )

    async def send_recommand(self, event):
        res = operations.getRecommParkings(indoor_id=self.doorNum)
        if res['code'] == 'success':
            res['code'] = 'recommand_parkings'
            await self.send_json(res)


class OutdoorConsumer(AsyncJsonWebsocketConsumer):
    group_name = None

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

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print('OutdoorConsumer 不需要接受信息, 丢弃: {}'.format(json.dumps(
            text_data_json)))

    async def outdoor_discover_license_plate(self, event):
        """
        监听来自于 HyperLPR 的 Celery Tasks 的事件
        """
        await self.send_json(
            {
                'code': 'discover_license',
                # TODO: 到时候可以添加 status code 之类的信息
                'data': json.loads(event['message'])
            }
        )

    async def send_fee_cards(self, event):
        fee_cards_dict = json.loads(event['message'])
        await self.send_json({
            'code': 'fee_cards',
            'data': fee_cards_dict
        })

    async def send_fee_success(self, event):
        """
        收费成功
        """
        await self.send_json({
            'code': 'confirm_fee',
            'data': json.loads(event['message'])
        })


class OutdoorAdminConsumer(AsyncJsonWebsocketConsumer):
    group_name = None

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

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        if content['type'] == 'confirm_fee':
            # 管理员确认支付
            fee = content['data'].get('fee_selected', 0)
            card_id = content['data'].get('card_id', '')
            doorNum = content['data']['doorNum']
            license = content['data']['license_plate']
            admin_info = str(self.scope['user'])
            date_out = datetime.datetime.strptime(content['data']['date_out'],
                                                  operations.time_format)
            operations.vehicle_leave(license, doorNum, date_out, admin_info,
                                     fee, card_id)
            channel_layer = get_channel_layer()
            await channel_layer.group_send('outdoor_'.format(doorNum), {
                'type': 'confirm_fee',
                'message': {
                    'admin_info': admin_info,
                    'card_id': card_id,
                    'fee': fee,
                    'license_plate': license
                }
            })

    async def send_fee_cards(self, event):
        fee_cards_dict = json.loads(event['message'])
        await self.send_json({
            'code': 'fee_cards',
            'data': fee_cards_dict
        })


class ParkingLotStatusConsumer(AsyncJsonWebsocketConsumer):
    group_name = None

    """
    停车场内停车位的占用信息更新
    """
    async def connect(self):
        # Are they logged in?
        if self.scope["user"].is_anonymous:
            # Reject the connection
            await self.close()
        else:
            self.layerNum = self.scope['url_route']['kwargs']['layerNum']
            self.group_name = 'status_{}'.format(self.layerNum)
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            res = operations.getAllParkingStatus()
            if res['code'] == 'success':
                res['code'] = 'updateParking'
                await self.send_json(res)

    async def disconnect(self, close_code):
        if self.group_name is not None:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        print('ParkingLotStatusConsumer 不需要接受信息, 丢弃: {}'.format(json.dumps(
            content)))

    async def update_parking(self, event):
        await self.send_json(
            json.loads(event['message'])
        )
