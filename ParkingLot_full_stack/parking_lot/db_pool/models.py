# models use MongoDB
# from mongoengine import *
from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import ReferenceField
from mongoengine import ListField
from mongoengine import IntField
from mongoengine import MapField
from mongoengine import LazyReferenceField
import datetime


class Vehicle(Document):
    """
    TODO
    车辆信息
    """
    license_plate = StringField(max_length=20, primary_key=True,
                                unique=True, required=True)
    # 备注
    addition_info = StringField(max_length=10000, default='')
    phone_number = StringField(max_length=14, required=True)
    # 车主信息
    owner_name = StringField(max_length=20, required=True)
    # 会员卡, 双向绑定, 并且是可选的, 也就是说, 会员卡可以在不登记在
    # 车辆信息的情况下, 直接使用
    # 如果要新增或删除会员卡, 一定要记得在 MemberCard 里面同时新增或
    # 删除车辆的引用
    # 记住: 对在 Document 里面对引用的更改在该 Document save 的时候不会对其
    # 引用的 Document 进行保存, 除非使用 Cascading Saves
    member_card = ListField(ReferenceField('MemberCard'))


class MemberCard(Document):
    """
    会员卡
    """
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    # 'count'(记数卡), 'top-up'(充值卡)
    card_type = StringField(max_length=20, required=True)
    addition_info = StringField(max_length=10000)
    # 会员卡与车辆双向绑定, 这个是可选的
    bind_vehicles = ListField(ReferenceField(Vehicle))


class MemberCardLog(Document):
    """
    会员卡更新日志
    """
    date_log = DateTimeField(default=datetime.datetime.utcnow)
    # 'create', 'update', 'remove'
    event_type = StringField(max_length=20, required=True)
    # 相关联的会员卡, 如果 event_type 是 'remove'
    card_reference = ReferenceField(MemberCard)
    addition_info = StringField(max_length=10000)
    # 产生该日志的操作员信息
    admin_info = StringField(max_length=50, required=True)


class Parking(Document):
    """
    TODO:
    车位信息
    """
    parking_id = StringField(max_length=20, primary_key=True,
                             unique=True, required=True)
    addition_info = StringField(max_length=10000, default='')
    phone_number = StringField(max_length=14, default='')
    location = StringField(max_length=100, default='')
    # 出入口
    indoors = ListField(ReferenceField('Door'))
    outdoors = ListField(ReferenceField('Door'))


class Floor(Document):
    """
    楼层信息
    """
    name = StringField(max_length=100, required=True)
    id_in_map = StringField(max_length=100, required=True)
    # 几楼?
    floor_num = IntField(required=True)
    # 楼层里面可能有多个分区
    # 使用懒加载, 避免只需要 pk 的时候的性能开销
    # 访问的时候会返回一个 class instance, 所以要手动
    # fetch() 才能解引用
    regions = MapField(field=LazyReferenceField('Region'))


class Region(Document):
    """
    区域信息
    """
    name = StringField(max_length=100, required=True)
    # DCMMC: TODO: 这个在模型的 json 里面暂时还没有...
    id_in_map = StringField(max_length=100, required=True)
    floor = ReferenceField('Floor')
    # 车位
    parkings = MapField(field=LazyReferenceField('Parking'))


class Door(Document):
    """
    出入口
    """
    # 这是在 models.json 这个停车场建模文件中该出入口对应的 id
    # 所有的 id_in_map 必须要跟 models.json 一致!!
    id_in_map = StringField(max_length=100, required=True)
    # 提高可读性, 出入口名称, e.g. 西一门, 最好要跟建模 json 文件对应起来!
    name = StringField(max_length=100, required=True)


class ParkingLot(Document):
    """
    停车场信息
    """
    parking_lot_name = StringField(max_length=50, primary_key=True,
                                   unique=True, required=True)
    addition_info = StringField(max_length=10000, default='')


class Bill(Document):
    """
    账单信息
    Time series
    """
    date_created = DateTimeField(default=datetime.datetime.utcnow)


# class Coach(Document):
# 	"""
# 	教练信息数据库
# 	"""
# 	meta = {
# 		'collection': 'coach_data'
# 	}

# 	# mobile 有时候也被称为 username
# 	mobile = LongField(required=True, primary_key=True)
# 	name = StringField(required=True)
# 	# male/female
# 	sex = StringField(required=True, default="male")
# 	cardId = StringField(required=True, unique=True)
# 	headphoto = StringField(default="default.png")
# 	password = StringField(default="changeme")
#
# class Student(Document):
# 	"""
# 	学员信息数据库
# 	"""
# 	meta = {
# 		'collection': 'sudent_data'
# 	}
# 	name = StringField()
# 	mobile = LongField(required=True, primary_key=True)
# 	sex = StringField(required=True, default="male")
# 	cardId = StringField(required=True, unique=True)
# 	headphoto = StringField(default="default.png")
# 	password = StringField(default="changeme")
# 	height = FloatField(required=True, default=0)
# 	weight = FloatField(required=True, default=0)
# 	f1 = FloatField(required=True, default=0)
# 	x1 = FloatField(required=True, default=0)
# 	f2 = FloatField(required=True, default=0)
# 	x2 = FloatField(required=True, default=0)
# 	x_max = FloatField(required=True, default=0)
# 	x_min = FloatField(required=True, default=0)
# 	f3 = FloatField(required=True, default=0)
# 	x3 = FloatField(required=True, default=0)
# 	f4 = FloatField(required=True, default=0)
# 	x4 = FloatField(required=True, default=0)
