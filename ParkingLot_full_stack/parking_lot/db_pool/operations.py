# 一堆对 models 的数据库操作的封装
import json
import os
import traceback
import db_pool.models as db
import math
from mongoengine import Q
from mongoengine import DoesNotExist
from random import sample
import datetime


time_format = "%Y/%m/%d, %H:%M:%S"


def load_model_create_db(file_abspath, addition_info=''):
    """
    从停车场建模的 json 文件中导入停车场数据并且创建对应的数据库
    @param file_abspath 模型文件的绝对路径
    """
    if not os.path.isfile(file_abspath):
        # TODO
        return 'ERROR: 文件 {} 不存在!'.format(os.path.basename(file_abspath))
    print('从文件 {} 中创建数据库...'.format(file_abspath))
    if len(db.ParkingLot.objects()):
        db.ParkingLot.objects().delete()
    if len(db.Floor.objects()):
        db.Floor.objects().delete()
    if len(db.Region.objects()):
        db.Region.objects().delete()
    if len(db.Parking.objects()):
        db.Parking.objects().delete()
    if len(db.Door.objects()):
        db.Door.objects().delete()
    with open(file_abspath, 'r') as f:
        data = json.load(f)
        parking_lot = db.ParkingLot(parking_lot_name=data[
            'data']['building'][
            'Name'])
        parking_lot.phone_number = data['data']['building'][
            'Tel']
        floors = {}
        indoors = {}
        outdoors = {}
        for floor in data['data']['Floors']:
            floor_doc = db.Floor()
            floor_doc.name = floor['Name']
            floor_doc.id_in_map = str(floor['_id'])
            floor_doc.floor_num = int(floor['_id'])
            floor_doc.save()
            # DCMMC: TODO: 楼层现在暂时用 Brief 代替!!
            try:
                floor_doc.floor_num = int(floor['Brief'])
            except: # noqa
                try:
                    floor_doc.floor_num = int(floor['_id'])
                except: # noqa
                    print('ERROR: floor_num 有误!!!')
            # DCMMC: TODO: 为 models.json 添加区域!
            regions = {}
            region_doc = db.Region()
            region_doc.name = '一区'
            region_doc.floor = floor_doc
            region_doc.id_in_map = '1'
            region_doc.save()
            regions[region_doc.id_in_map] = region_doc
            parkings = {}
            for entry in floor['FuncAreas']:
                if entry['SortType'] == 1:
                    parking_doc = db.Parking()
                    parking_doc.parking_id = entry['ParkingNo']
                    parking_doc.floor = floor_doc
                    parking_doc.region = region_doc
                    parking_doc.addition_info = entry['Name']
                    parking_doc.used = (entry['AreaStatus'] == 1)
                    parkings[parking_doc.parking_id] = parking_doc
                    parking_doc.save()
                elif entry['SortType'] == 3 or entry['SortType'] == 4:
                    door_doc = db.Door()
                    door_doc.id_in_map = str(entry['_id'])
                    door_doc.name = entry['Name']
                    door_doc.status = 'working'
                    if entry['SortType'] == 3:
                        door_doc.door_type = 'indoor'
                        door_doc.save()
                        indoors[str(entry['_id'])] = door_doc
                    else:
                        door_doc.door_type = 'outdoor'
                        door_doc.save()
                        outdoors[str(entry['_id'])] = door_doc
                else:
                    # TODO: warning if type is 0 (unsorted)
                    pass
            # region_doc.parkings = parkings
            region_doc.update(set__parkings=parkings)
            # floor_doc.regions = regions
            floor_doc.update(set__regions=regions)
            floors[floor_doc.id_in_map] = floor_doc
        parking_lot.floors = floors
        parking_lot.indoors = indoors
        parking_lot.outdoors = outdoors
        parking_lot.addition_info = addition_info
        parking_lot.save()
    return None


def updateFloor():
    pass


def updateRegion():
    pass


def updateParking(parking_id, used=None,
                  status=None,
                  addition_info=None):
    """
    @param used bool 类型
    """
    # lot_id = db.ParkingLot.objects().first()
    try:
        p = db.Parking.objects(parking_id=parking_id).get()
    except DoesNotExist:
        return {'code': 'error', 'info': '车位 {} 未找到!'.format(
            str(parking_id))}
    try:
        to_update = {}
        if used:
            to_update['set__used'] = used
        if status:
            if status not in ['normal', 'unavailable', 'obligated']:
                return {'code': 'error', 'info': 'status 值错误'}
            to_update['set__status'] = status
        if addition_info:
            to_update['set__addition_info'] = addition_info
        p.update(**to_update)
        return {'code': 'success'}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def addMemberCard(phone, card_type, value, admin, bind_license=[],
                  info=''):
    try:
        c = db.MemberCard(phone_number=phone, card_type=card_type, value=value,
                          addition_info=info)
        for i in range(len(bind_license)):
            try:
                bind_license[i] = db.Vehicle.objects(
                    license=bind_license[i]).get()
            except DoesNotExist:
                return {'code': 'error', 'info': '车牌 {} 不存在!'.format(
                    bind_license[i]
                )}
        c.bind_vehicles = bind_license
        c.save()
        log = db.MemberCardLog()
        log.card_reference = c
        log.event_type = 'create'
        log.addition_info = '创建会员卡, 卡号={}, 值={}'.format(c.id, value)
        log.admin_info = admin
        log.save()
        return {'code': 'success', 'info': '会员卡号: {}'.format(
            str(c.id))}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def addVehicle(license, **kwargs):
    """
    车牌, 以及其他可选信息
    """
    if len(db.Vehicle.objects(license_plate=license)) == 0:
        v = db.Vehicle(license_plate=license)
        for k, value in kwargs.items():
            try:
                v.__setattr__(k, value)
            except: # noqa
                # TODO, 不存在
                pass
        v.save()
        return {'code': 'success', 'info': ''}
    else:
        return {'code': 'error', 'info': '车牌 {} 已经存在'.format(license)}


def updateVehicle(license, **kwargs):
    try:
        v = db.Vehicle.objects(license_plate=license).get()
        up = {}
        for k, value in kwargs.items():
            up['set__' + k] = value
        v.update(**up)
        return {'code': 'success'}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def getVehiclesFilter(**kwargs):
    try:
        vs = db.Vehicle.objects().all()
        if 'phone_number' in kwargs:
            vs = vs.filter(phone_number=kwargs['phone_number'])
        if 'license_plate' in kwargs:
            vs = vs.filter(license_plate=kwargs['license_plate'])
        if 'used' in kwargs:
            vs = vs.filter(used=kwargs['used'])
        cnt = vs.count()
        if 'offset' in kwargs:
            vs = vs.skip(kwargs['offset'])
        if 'limit' in kwargs:
            vs = vs.limit(kwargs['limit'])
        vs = [{
            'owner_name': v.owner_name,
            'phone_number': v.phone_number,
            'license_plate': v.license_plate,
            'addition_info': v.addition_info,
            'cards': [
                {
                    'id': c.id,
                    'card_type': c.card_type,
                    'value': str(c.value)
                } for c in v.member_card
            ]
        } for v in vs]
        return {'code': 'success', 'data': {
            'count': cnt,
            'vehicles': vs
        }}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def rmVehicle(license, **kwargs):
    try:
        db.Vehicle.objects(license_plate=license).first().delete()
        return {'code': 'success'}
    except Exception as e:
        traceback.print_exc(e)
        return {'code': 'error', 'info': str(e)}


def updateMemberCard(cardId, new_val, admin, info='',
                     bind_license='',
                     phone_number=''):
    try:
        try:
            c = db.MemberCard.objects(id=cardId).get()
        except DoesNotExist:
            return {'code': 'error', 'info': '会员卡("{}") 未找到!'.format(
                cardId
            )}
        old = c.value
        c.update(set__value=new_val)
        if phone_number and phone_number != '':
            c.update(set__phone_number=phone_number)
        if bind_license and bind_license != '':
            arr = c.bind_vehicles
            arr.append(db.Vehicle.objects(license_plate=bind_license).get())
            c.update(set__bind_vehicles=arr)
        log = db.MemberCardLog()
        log.admin_info = admin
        log.card_reference = c
        log.addition_info = info + '. old_value={}, new_value={}'.format(
            old, new_val
        )
        log.event_type = 'update'
        log.save()
        return {'code': 'success', 'info': ''}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def removeMemberCard(card_id=None, admin=''):
    try:
        if card_id:
            c = db.MemberCard.objects(id=card_id).get()
            c.delete()
            log = db.MemberCardLog()
            log.admin_info = admin
            log.addition_info = '删除会员卡: ' + str(card_id)
            log.event_type = 'remove'
            log.save()
        return {'code': 'success'}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def vehicle_enter(license, date_in, indoorId):
    """
    @param license 车牌, str
    @param date_in datetime.datetime, 入场时间
    @param indoorId 入口号, str, 这个是跟 id_in_map 对应的
    """
    try:
        vehicle = db.Vehicle.objects(license_plate=license)
    except Exception:
        vehicle = []
    print('数据库, 车辆进入!')
    if len(vehicle) == 0:
        vehicle = addVehicle(license)
    vehicle = db.Vehicle.objects(license_plate=license).get()
    if not vehicle:
        # TODO error
        return {'code': 'error'}
    vehicle.update(set__date_in=datetime.datetime.utcnow,
                   set__indoor_id=indoorId)
    # TODO: 入场 ws
    return {'code': 'success'}


def get_fee_and_cards(license, date_out):
    try:
        vehicle = db.Vehicle.objects(license_plate=license).get()
        # TODO: 复杂计费系统
        diff = date_out - vehicle.date_in
        print('耗时: ', diff)
        days, seconds = diff.days, diff.seconds
        hours = math.ceil(days * 24 + seconds / 3600)
        # TODO: 多停车场情况
        fee = db.ParkingLot.objects().get().fee_per_hr * hours
        print('############## debug fee:', fee)
        cards = []
        for i in vehicle.member_card:
            cards.append({'id': i.id, 'card_type': i.card_type,
                          'value': i.value})
        return {
            'fee': fee, 'cards': cards,
            'date_in': vehicle.date_in.strftime(
                    "%Y/%m/%d, %H:%M:%S"
                ),
            'date_out': date_out.strftime("%Y/%m/%d, %H:%M:%S"),
            'indoorNum': vehicle.indoor_id,
            'indoorName': getDoorNameById(vehicle.indoor_id)
        }
    except Exception as e:
        import traceback # noqa
        traceback.print_exc(e)
        return


def vehicle_leave(license, outdoorId, date_out, admin, fee,
                  card_id=''):
    """
    在前端中选择是否使用会员卡, 或者直接输入一个会员卡号
    date_out 是 datetime.datetime 类型
    """
    try:
        vehicle = db.Vehicle.objects(license_plate=license)
        if len(vehicle) == 0:
            # TODO: error
            return {'code': 'error', 'info': 'vehicle 不存在'}
        vehicle = vehicle.get()
        log = db.BillLog()
        log.date_in = vehicle.date_in
        log.date_out = date_out
        log.admin_info = admin
        log.vehicle = vehicle
        # 必须合法的 id!
        try:
            card = db.MemberCard.objects(id=card_id).get() if \
                (card_id and card_id != '') else None
        except DoesNotExist:
            return {'code': 'error', 'info': 'card_id="{}" 不存在, 请检查'.format(
                card_id)}
        # TODO: 多停车场情况
        if card:
            log.member_card = card
            if card.card_type == 'count':
                log.addition_info = \
                        '剩余次数: {}'.format(int(card.value))
                card_value = card.value - 1
                up_res = updateMemberCard(card_id, card_value, admin,
                                          info='车牌号 {} 在 {} 使用'.format(
                                              license, str(date_out)))
                if up_res['code'] != 'success':
                    raise Exception(up_res['info'])
            elif card.card_type == 'top-up':
                log.addition_info = \
                    '余额: {:.3f}'.format(float(card.value))
                log.fee = fee
                card_value = card.value - fee
                up_res = updateMemberCard(card_id, card_value, admin,
                                          info='车牌号 {} 在 {} 使用'.format(
                                              license, str(date_out)
                                          ))
                if up_res['code'] != 'success':
                    raise Exception(up_res['info'])
                card.save()
        else:
            log.fee = fee
        vehicle.update(set__date_in=None, set__indoor_id=None)
        vehicle.save()
        log.save()
        return {'code': 'success', 'info': ''}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def updateDoor():
    pass


def getBillsByDateRangeCheckin(start_date, end_date):
    logs = db.BillLog.objects(Q(date_in__gte=start_date) &
                              Q(date_in__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        card = l.member_card.fetch() if l.member_card else None
        fee_type = '非会员'
        if card:
            if card.card_type == 'count':
                fee_type = '记次卡'
                logs_dict['addition_info'] = \
                    '剩余次数: {}'.format(int(card.value))
            elif card.card_type == 'top-up':
                fee_type = '储值卡'
                logs_dict['addition_info'] = \
                    '余额: {:.3f}'.format(float(card.value))
            logs_dict['card_id'] = str(card.id)
        logs_dict['fee_type'] = fee_type
        logs_dict['fee'] = str(l.fee) if l.fee else '记次卡消费'
        logs_dict['indoor'] = l.indoor.fetch().name
        logs_dict['outdoor'] = l.outdoor.fetch().name
        logs_dict['license'] = l.vehicle.id
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getBillLogsFilter(**kwargs):
    try:
        logs = db.BillLog.objects()
        if 'license_plate' in kwargs:
            logs = logs.filter(license__id=kwargs['license_plate'])
        if 'date_in_start' in kwargs:
            s = datetime.datetime.strptime(kwargs['date_in_start'],
                                           time_format)
            logs = logs.filter(date_in__gte=s)
        if 'date_in_end' in kwargs:
            e = datetime.datetime.strptime(kwargs['date_in_end'],
                                           time_format)
            logs = logs.filter(date_in__lte=e)
        cnt = logs.count()
        if 'offset' in kwargs:
            logs = logs.skip(kwargs['offset'])
        if 'limit' in kwargs:
            logs = logs.limit(kwargs['limit'])
        logs = [
            {
                'license_plate': l.vehicle.id,
                'date_in': l.date_in.strftime(time_format),
                'date_out': l.date_out.strftime(time_format),
                'fee': str(l.fee),
                'indoor': l.indoor.fetch().id_in_map if l.indoor else '',
                'outdoor': l.outdoor.fetch().id_in_map if l.outdoor else '',
                'addition_info': l.addition_info,
                'card_id': l.member_card.id if l.member_card else None,
                'card_type': l.member_card.card_type if l.member_card
                else None,
            } for l in logs
        ]
        return {'code': 'success', 'data': {
            'count': cnt,
            'logs': logs,
        }}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def getParkingLogsFilter(**kwargs):
    try:
        logs = db.ParkingLotLog.objects()
        # DCMMC: TODO: 凉了, 我发现判断 kwargs 存在之后还要再判断是否为空的...
        # 所有的类似逻辑都要这样..
        if 'event_type' in kwargs and kwargs['event_type'] != '':
            logs = logs.filter(event_type=kwargs['event_type'])
        if 'date_start' in kwargs and kwargs['date_start'] != '':
            s = datetime.datetime.strptime(kwargs['date_start'],
                                           time_format)
            logs = logs.filter(date_created__gte=s)
        if 'date_end' in kwargs and kwargs['date_end'] != '':
            e = datetime.datetime.strptime(kwargs['date_end'],
                                           time_format)
            logs = logs.filter(date_created__lte=e)
        cnt = logs.count()
        if 'offset' in kwargs:
            logs = logs.skip(kwargs['offset'])
        if 'limit' in kwargs:
            logs = logs.limit(kwargs['limit'])
        logs = [
            {
                'date_created': l.date_log.strftime(time_format),
                'event_type': l.indoor.event_type,
                'card_reference': l.card_reference.id,
                'addition_info': l.addition_info,
                'admin_info': l.admin_info,
            } for l in logs
        ]
        return {'code': 'success', 'data': {
            'count': cnt,
            'logs': logs,
        }}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


def getCardLogsFilter(**kwargs):
    try:
        logs = db.MemberCardLog.objects()
        if 'card_id' in kwargs and kwargs['card_id'] != '':
            c = db.MemberCard.objects(id=kwargs['card_id']).get()
            logs = logs.filter(card_reference=c)
        if 'date_start' in kwargs and kwargs['date_start'] and \
                kwargs['date_start'] != '':
            s = datetime.datetime.strptime(kwargs['date_start'],
                                           time_format)
            logs = logs.filter(date_log__gte=s)
        if 'date_end' in kwargs and kwargs['date_end'] and \
                kwargs['date_end'] != '':
            e = datetime.datetime.strptime(kwargs['date_end'],
                                           time_format)
            logs = logs.filter(date_log__lte=e)
        cnt = logs.count()
        if 'offset' in kwargs:
            logs = logs.skip(kwargs['offset'])
        if 'limit' in kwargs:
            logs = logs.limit(kwargs['limit'])

        def check_rm(l, e):
            # workaround
            import re # noqa
            try:
                return str(l.card_reference.id) if l.card_reference else ''
            except Exception as ex:
                print(ex)
                r = re.search(".*ObjectId\\('([\\.0-9a-zA-Z]*)'.*", str(ex))
                print(r)
                return r.group(1)

        logs = [
            {
                'date_log': l.date_log.strftime(time_format),
                'event_type': l.event_type,
                'card_reference': check_rm(l, l.event_type), # noqa
                'addition_info': l.addition_info,
                'admin_info': l.admin_info,
            } for l in logs
        ]
        return {'code': 'success', 'data': {
            'count': cnt,
            'logs': logs,
        }}
    except Exception as e:
        print(e)
        return {'code': 'error', 'info': str(e)}


def getBillsByDateRangeCheckout(start_date, end_date):
    logs = db.BillLog.objects(Q(date_out__gte=start_date) &
                              Q(date_out__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        card = l.member_card.fetch() if l.member_card else None
        fee_type = '非会员'
        if card:
            logs_dict['card_id'] = str(card.id)
        logs_dict['fee_type'] = fee_type
        logs_dict['fee'] = str(l.fee) if l.fee else '记次卡消费'
        logs_dict['indoor'] = l.indoor.fetch().name
        logs_dict['outdoor'] = l.outdoor.fetch().name
        logs_dict['license'] = l.vehicle.id
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getBillsByLicense(license):
    logs = db.BillLog.objects(vehicle__id=license)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        card = l.member_card.fetch() if l.member_card else None
        fee_type = '非会员'
        if card:
            logs_dict['card_id'] = str(card.id)
        logs_dict['fee_type'] = fee_type
        logs_dict['fee'] = str(l.fee) if l.fee else '记次卡消费'
        logs_dict['indoor'] = l.indoor.fetch().name
        logs_dict['outdoor'] = l.outdoor.fetch().name
        logs_dict['license'] = l.vehicle.id
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getBillsByAdmin(admin):
    logs = db.BillLog.objects(admin_info=admin)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        card = l.member_card.fetch() if l.member_card else None
        fee_type = '非会员'
        if card:
            logs_dict['card_id'] = str(card.id)
        logs_dict['fee_type'] = fee_type
        logs_dict['fee'] = str(l.fee) if l.fee else '记次卡消费'
        logs_dict['indoor'] = l.indoor.fetch().name
        logs_dict['outdoor'] = l.outdoor.fetch().name
        logs_dict['license'] = l.vehicle.id
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getBillsByType(member, card_type=''):
    """
    @param member 如果为 False, 查找非会员, 如果为 True, 查找会员
    @param card_type 会员卡类型 top-up/count
    """
    if member:
        cards = db.MemberCard.objects(card_type=card_type)
        logs = db.BillLog.objects(member_card__in=cards)
    else:
        logs = db.BillLog.objects(member_card=None)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        card = l.member_card.fetch() if l.member_card else None
        fee_type = '非会员'
        if card:
            logs_dict['card_id'] = str(card.id)
        logs_dict['fee_type'] = fee_type
        logs_dict['fee'] = str(l.fee) if l.fee else '记次卡消费'
        logs_dict['indoor'] = l.indoor.fetch().name
        logs_dict['outdoor'] = l.outdoor.fetch().name
        logs_dict['license'] = l.vehicle.id
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getMemberCardLogsByDateRange(start_date, end_date):
    logs = db.MemberCardLog.objects(Q(date_log__gte=start_date) &
                                    Q(date_log__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardLogByCardId(cardId):
    logs = db.MemberCardLog.objects(id=cardId)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardsLogsByLicense(license):
    cards = db.Vehicle.objects(license_plate=license).get().member_card
    logs = db.MemberCardLog.objects(card_reference__in=cards)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardLogsByAdmin(admin_info):
    logs = db.MemberCardLog.objects(admin_info=admin_info)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardLogsByType(event_type):
    logs = db.MemberCardLog.objects(event_type=event_type)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getLicensesByPhone(phone):
    vehicles = db.Vehicle.objects(phone_number=phone).all()
    licenses = []
    for v in vehicles:
        licenses.append(v.license_plate)
    return licenses


def getLiensesByOwnName(name):
    vehicles = db.Vehicle.objects(owner_name=name).all()
    licenses = []
    for v in vehicles:
        licenses.append(v.license_plate)
    return licenses


def arrange_parkings_by_floor(parkings_dict):
    """
    @param parkings_dict [{'parking_id': 'id', 'used': True, ...}, ...]
    """
    # TODO 异常处理
    keys = []
    for i in parkings_dict:
        keys.append(i['parking_id'])
    ps = db.Parking.objects(parking_id__in=keys)
    lot = db.ParkingLot.objects().get()
    res = {}
    for i, f in lot.floors.items():
        al = ps.filter(floor=f).all()
        al = [al_p.parking_id for al_p in al]
        res[i] = {}
        for parking in parkings_dict:
            if parking['parking_id'] in al:
                res[i][parking['parking_id']] = parking
    return res


def getParkingLogsByDateRange(start_date, end_date):
    """
    从指定时间段获得日志
    """
    logs = db.ParkingLotLog.objects(Q(date_created__gte=start_date) &
                                    Q(date_created__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getParkingLotLogsByType(event_type):
    logs = db.ParkingLotLog.objects(event_type=event_type).all()
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getParkingLotLogsByAdmin(admin_info):
    """
    通过 admin 信息获得日志
    """
    logs = db.ParkingLotLog.objects(admin_info=admin_info).all()
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['admin_info'] = admin_info
        logs_dict['event_info'] = l.event_info
    return logs_dict


def getUsedParkings(floor_id=[], region_id=[]):
    """
    获取正在使用的停车位
    """
    # TODO: 多停车场
    parkings = db.Parking.objects(used=True).all()
    parkings_filter = []
    for p in parkings:
        if len(floor_id) > 0:
            p = None if p.floor.id_in_map not in floor_id else p
        if len(region_id) > 0:
            p = None if p.region.id_in_map not in region_id else p
        if p:
            parkings_filter.append(p.parking_id)
    return {'code': 'success', 'data': parkings_filter}


def getAvailableParkings(floor_id=[], region_id=[]):
    """
    获取空停车位
    """
    # TODO: 多停车场
    parkings = db.Parking.objects(used=False).all()
    parkings_filter = []
    for p in parkings:
        if len(floor_id) > 0:
            p = None if p.floor.id_in_map not in floor_id else p
        if len(region_id) > 0:
            p = None if p.region.id_in_map not in region_id else p
        if p:
            parkings_filter.append(p.parking_id)
    return {'code': 'success', 'data': parkings_filter}


def getRecommParkings(indoor_id):
    """
    通过入口给出推荐停车位
    TODO
    """
    # 暂时随机...
    try:
        ps = list(db.Parking.objects(used=False).all())
    except DoesNotExist:
        print('停车场数据库为空')
        return {'code': 'error', 'info': '停车场数据库为空!'}
    cnt = 5 if len(ps) >= 5 else len(ps)
    ps = sample(ps, cnt)
    return {'code': 'success', 'data': [p.parking_id for p in ps]}


def getAllParkingStatus():
    # TODO 多停车场
    try:
        parkings = db.Parking.objects().all() # noqa
    except DoesNotExist:
        return {'code': 'error', 'info': '停车场数据库为空!!'}
    lot = db.ParkingLot.objects().get()
    floors = lot.floors
    res = {}
    for k, v in floors.items():
        res[k] = {}
        regions = v.regions
        for k_r, v_r in regions.items():
            res[k][k_r] = {}
            # 原来这 MapField(LazyReferenceField()) 就是 dict{'xx': 'Field 的 pk'}
            # 所以还要用这个 value 作为 ObjectId(primary key) 查询一次
            v_r = db.Region.objects.get(id=v_r)
            # v_r = v_r.fetch()
            for k_p, r_p in v_r.parkings.items():
                # i = r_p.fetch() # noqa
                i = db.Parking.objects.get(parking_id=r_p)
                res[k][k_r][k_p] = (('used' if i.used else 'unused') if
                                    i.status == 'normal' else i.status)
    return {'code': 'success', 'data': res}


def getAllDoorIds(door_type):
    try:
        doors = db.Door.objects(door_type='indoor').all()
    except DoesNotExist:
        return {'code': 'error', 'info': ''}
    return {'code': 'success', 'data': [i.id_in_map for i in doors]}


def getDoorNameById(id_in_map):
    try:
        door = db.Door(id_in_map=id_in_map)
        return {'code': 'success', 'data': door.name}
    except DoesNotExist:
        pass
    return {'code': 'error', 'info': 'todo'}


def getParkingsFilter(offset=0, limit=20, floor_id='', region_id='',
                      parking_id=''):
    """
    @offset 分页的第一条的偏移量
    @param limit int, 分页大小, 记得在第2页及以后都要带上 gt_oid
    @param floor_id 检索floor 的 id_in_map, 为空表示不限制楼层, region_id 同理
    @param parking_id 指定 parking_id, 那么就只返回一个或者空了
    """
    try:
        if parking_id and parking_id != '':
            res = db.Parking.objects(parking_id=parking_id)
        else:
            res = db.Parking.objects()
            if floor_id and floor_id != '':
                res = res.filter(floor=db.Floor.objects(
                    id_in_map=floor_id).get())
            if region_id and region_id != '':
                res = res.filter(region=db.Region.objects(
                    id_in_map=region_id
                ).get())
            # if gt_oid and gt_oid != '':
            #     res = res.filter(__raw__={
            #         '_id': {
            #             '$gt': gt_oid
            #         }
            #     })
            res = res.order_by('parking_id')
        count = len(res)
        res = res.skip(offset).limit(limit)
        res = [
            {
                'addition_info': p.addition_info,
                'parking_id': p.parking_id,
                'floor_id': p.floor.id_in_map,
                'region_id': p.region.id_in_map,
                'status': p.status,
                'used': p.used,
            } for p in list(res)
        ]
        res = {'parkings': res}
        res['count'] = count
        return {'code': 'success', 'data': res}
    except Exception as e: # noqa
        # traceback.print_exc(e)
        return {'code': 'error', 'info': str(e)}


def getMemberCardsFilter(**kwargs):
    try:
        vs = db.MemberCard.objects().all()
        cnt = vs.count()
        if 'card_id' in kwargs:
            vs = vs.filter(id=kwargs['card_id'])
            cnt = len(list(vs))
            if 'offset' in kwargs:
                vs = vs.skip(kwargs['offset'])
            if 'limit' in kwargs:
                vs = vs.limit(kwargs['limit'])
        elif 'license_plate' in kwargs and kwargs['license_plate'] != '':
            vs = db.Vehicle.objects(
                license_plate=kwargs['kwargs']).get().member_card()
            cnt = len(vs)
        vs = [{
            'date_created': v.date_created,
            'phone_number': v.phone_number,
            'addition_info': v.addition_info,
            'value': str(v.value),
            'card_type': v.card_type,
            'card_id': str(v.id),
            'bind_vehicles': [
                {
                    'license_plate': p.license_plate,
                } for p in v.bind_vehicles
            ]
        } for v in vs]
        return {'code': 'success', 'data': {
            'count': cnt,
            'cards': vs
        }}
    except Exception as e:
        return {'code': 'error', 'info': str(e)}


