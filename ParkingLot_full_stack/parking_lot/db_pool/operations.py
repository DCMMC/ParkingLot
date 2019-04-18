# 一堆对 models 的数据库操作的封装
import json
import os
import .models as db # noqa
from mongoengine import Q


def load_model_create_db(file_abspath, addition_info=''):
    """
    从停车场建模的 json 文件中导入停车场数据并且创建对应的数据库
    @param file_abspath 模型文件的绝对路径
    """
    if not os.path.isfile(file_abspath):
        # TODO
        return 'ERROR: 文件 {} 不存在!'.format(os.path.basename(file_abspath))
    with open(file_abspath, 'r') as f:
        data = json.load(f)
        parking_lot = db.ParkingLot(parking_lot_name=data['data']['building'][
            'Name'])
        parking_lot.phone_number = data['data']['building'][
            'Tel']
        floors = {}
        indoors = {}
        outdoors = {}
        for floor in data['data']['Floors']:
            floor_doc = db.Floor()
            floor_doc.name = floor['Name']
            floor_doc.id_in_map = floor['_id']
            # DCMMC: TODO: 楼层现在暂时用 Brief 代替!!
            try:
                floor_doc.floor_num = int(floor['Brief'])
            except: # noqa
                try:
                    floor_doc.floor_num = int(floor['_id'])
                except: # noqa
                    print('ERROR: floor_num 有误!!!')
            # DCMMC: TODO: 为 models.json 添加区域!
            region_doc = db.Region()
            region_doc.name = '一区'
            region_doc.floor = floor_doc
            parkings = {}
            for entry in floor['FuncAreas']:
                if entry['SortType'] == 1:
                    parking_doc = db.Parking()
                    parking_doc.parking_id = parking_lot.parking_lot_name + \
                        entry['ParkingNo']
                    parking_doc.floor = floor_doc
                    parking_doc.region = region_doc
                    parking_doc.addition_info = entry['Name']
                    parking_doc.used = (entry['AreaStatus'] == 1)
                    parkings[parking_doc.parking_id] = parking_doc
                    parking_doc.save()
                elif entry['SortType'] == 3 or entry['SortType'] == 4:
                    door_doc = db.Door()
                    door_doc.id_in_map = entry['_id']
                    door_doc.name = entry['Name']
                    door_doc.status = 'working'
                    if entry['SortType'] == 3:
                        door_doc.door_type = 'indoor'
                        door_doc.save()
                        indoors[entry['_id']] = door_doc
                    else:
                        door_doc.door_type = 'outdoor'
                        door_doc.save()
                        outdoors[entry['_id']] = door_doc
                else:
                    # TODO: warning if type is 0 (unsorted)
                    pass
            region_doc.parkings = parkings
            region_doc.save()
            floor_doc.regions = region_doc
            floor_doc.save()
            floors[floor_doc.id_in_map] = floor_doc
        parking_lot.floors = floors
        parking_lot.indoor = indoors
        parking_lot.outdoors = outdoors
        parking_lot.addition_info = addition_info
        parking_lot.save()
    return None


def updateFloor():
    pass


def updateRegion():
    pass


def updateParking():
    pass


def updateParkingLot():
    pass


def addMemberCard():
    pass


def updateMemberCard():
    pass


def removeMemberCard():
    pass


def vehicle_enter():
    pass


def vehicle_leave():
    pass


def updateDoor():
    pass


def getBillsByDateRangeCheckin(start_date, end_date):
    logs = db.BillLog(Q(date_in__gte=start_date) & Q(date_in__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getBillsByDateRangeCheckout(start_date, end_date):
    logs = db.BillLog(Q(date_out__gte=start_date) & Q(date_out__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getBillsByLicense(license):
    logs = db.BillLog(vehicle__id)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.addition_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getBillsByAdmin():
    pass


def getBillsByType():
    pass


def getMemberCardLogsByDateRange(start_date, end_date):
    logs = db.MemberCardLog(Q(date_log__gte=start_date) &
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
    logs = db.MemberCardLog(id=cardId)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardsLogsByLicense(license):
    cards = db.Vehicle(license_plate=license).get().member_card
    logs = db.MemberCardLog(card_reference__in=cards)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardLogsByAdmin(admin_info):
    logs = db.MemberCardLog(admin_info=admin_info)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getMemberCardLogsByType(event_type):
    logs = db.MemberCardLog(event_type=event_type)
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
        logs_dict['card_id'] = str(l.card_reference.id)
    return logs_dict


def getLicensesByPhone(phone):
    vehicles = db.Vehicle(phone_number=phone).all()
    licenses = []
    for v in vehicles:
        licenses.append(v.license_plate)
    return licenses


def getLiensesByOwnName(name):
    vehicles = db.Vehicle(owner_name=name).all()
    licenses = []
    for v in vehicles:
        licenses.append(v.license_plate)
    return licenses


def getParkingLogsByDateRange(start_date, end_date):
    """
    从指定时间段获得日志
    """
    logs = db.ParkingLotLog(Q(date_created__gte=start_date) &
                            Q(date_created__lte=end_date))
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['event_info'] = l.event_info
        logs_dict['admin_info'] = l.admin_info
    return logs_dict


def getParkingLotLogsByType(event_type):
    logs = db.ParkingLotLog(event_type=event_type).all()
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
    logs = db.ParkingLotLog(admin_info=admin_info).all()
    logs_dict = {}
    for l in logs:
        logs_dict['date'] = l.date_created.strftime("%Y/%m/%d, %H:%M:%S")
        logs_dict['event_type'] = l.event_type
        logs_dict['admin_info'] = admin_info
        logs_dict['event_info'] = l.event_info
    return logs_dict
