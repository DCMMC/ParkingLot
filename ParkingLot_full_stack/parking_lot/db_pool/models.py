
# models use MongoDB
# from mongoengine import *
from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import FloatField
from mongoengine import ReferenceField
from mongoengine import ListField
from mongoengine import DecimalField
from mongoengine import IntField
from mongoengine import MapField
from mongoengine import LazyReferenceField
from mongoengine import BooleanField
import datetime


class Vehicle(Document):
    """
    车辆信息
    """
    # 车牌为主键
    # pk 不能同时设置为 unique
    license_plate = StringField(max_length=20, primary_key=True,
                                required=True)
    # 备注
    addition_info = StringField(max_length=10000, default='')
    phone_number = StringField(max_length=14)
    # 车主信息
    owner_name = StringField(max_length=20)
    # 会员卡, 双向绑定, 并且是可选的, 也就是说, 会员卡可以在不登记在
    # 车辆信息的情况下, 直接使用
    # 如果要新增或删除会员卡, 一定要记得在 MemberCard 里面同时新增或
    # 删除车辆的引用
    # 记住: 对在 Document 里面对引用的更改在该 Document save 的时候不会对其
    # 引用的 Document 进行保存, 除非使用 Cascading Saves
    member_card = ListField(ReferenceField('MemberCard'))
    # TODO: 暂停
    date_in = DateTimeField()
    indoor_id = StringField(max_length=20)


class MemberCard(Document):
    """
    会员卡
    """
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    # 持卡人信息
    phone_number = StringField(max_length=20, require=True)
    # 'count'(记数卡), 'top-up'(充值卡)
    card_type = StringField(max_length=20, required=True)
    # 记次/储值
    value = DecimalField(min_value=0., require=True)
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
    # 相关联的会员卡, 如果 event_type 是 'remove', 则为空
    # 为了保证安全, 删除操作必须前端重点提醒, 并且将 memberCard 当中的
    # 信息存在日志的 addition_info 里面
    card_reference = ReferenceField(MemberCard)
    addition_info = StringField(max_length=10000, require=True)
    # 产生该日志的操作员信息
    admin_info = StringField(max_length=50, required=True)


class Parking(Document):
    """
    车位信息
    """
    # 车位 id 推荐用停车场 pk + 车位号(在 models.json 里面的) 的结合
    parking_id = StringField(max_length=100, primary_key=True,
                             required=True)
    addition_info = StringField(max_length=10000, default='')
    floor = ReferenceField('Floor', require=True)
    region = ReferenceField('Region', require=True)
    # 'normal'(正常使用), 'unavailable'(不可用, e.g., 正在维修),
    # 'obligated'(特殊情况预留, e.g., 已预约)
    status = StringField(max_length=20, default='normal')
    # 是否有车在停车位上
    used = BooleanField(default=False)


class Floor(Document):
    """
    楼层信息
    """
    name = StringField(max_length=100, required=True)
    # 不作为 pk, 因为如果存在多个停车场, 就看会冲突
    id_in_map = StringField(max_length=100, required=True, unique=True)
    # 几楼?
    floor_num = IntField(required=True)
    # 楼层里面可能有多个分区
    # 使用懒加载, 避免只需要 pk 的时候的性能开销
    # 访问的时候会返回一个 class instance, 所以要手动
    # fetch() 才能解引用
    # {id_in_map: LazyRefField} 的字典
    regions = MapField(field=LazyReferenceField('Region'))
    addition_info = StringField(max_length=10000, default='')


class Region(Document):
    """
    区域信息
    """
    name = StringField(max_length=100, required=True)
    # DCMMC: TODO: 这个在模型的 json 里面暂时还没有...
    id_in_map = StringField(max_length=100, required=True,
                            unique=True)
    floor = ReferenceField('Floor', require=True)
    # 车位
    # {parkingNo: LazyRefField} 的字典
    parkings = MapField(field=LazyReferenceField('Parking'))
    addition_info = StringField(max_length=10000, default='')


class Door(Document):
    """
    出入口
    """
    # 这是在 models.json 这个停车场建模文件中该出入口对应的 id
    # 所有的 id_in_map 必须要跟 models.json 一致!!
    id_in_map = StringField(max_length=100, required=True)
    # 提高可读性, 出入口名称, e.g. 西一门, 最好要跟建模 json 文件对应起来!
    name = StringField(max_length=100, required=True)
    addition_info = StringField(max_length=10000, default='')
    # 'indoor', 'outdoor'
    door_type = StringField(max_length=20, require=True)
    # 'working', 'closed'
    status = StringField(max_length=20, require=True)


class ParkingLot(Document):
    """
    停车场信息
    """
    # 停车场名称必须唯一
    parking_lot_name = StringField(max_length=50, required=True,
                                   primary_key=True, uniqu=True)
    addition_info = StringField(max_length=10000, default='')
    # 联系电话
    phone_number = StringField(max_length=14, default='')
    location = StringField(max_length=100, default='')
    # 出入口
    # 这三个 map 都是 {id_in_map: RefField}
    indoors = MapField(ReferenceField('Door'))
    outdoors = MapField(ReferenceField('Door'))
    floors = MapField(ReferenceField(Floor))
    # 每小时费用
    # TODO: 暂定 10
    fee_per_hr = FloatField(default=10)


class ParkingLotLog(Document):
    """
    停车场信息维护
    主要是更新, 创建和删除一般不推荐做
    以为创建和删除之后最好还是要跟 models.json 里面的信息
    保持一致.
    Floor, Rigon, Parking, ParkingLot 这些数据的创建
    都是靠直接从 models.json 导入
    """
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    admin_info = StringField(max_length=50, required=True)
    event_type = StringField(max_length=100, required=True)
    # 具体操作信息用 String 来记录
    event_info = StringField(max_length=10000, required=True)


class BillLog(Document):
    """
    账单信息
    Time series
    """
    date_in = DateTimeField(required=True)
    date_out = DateTimeField(required=True)
    addition_info = StringField(max_length=10000, default='')
    # 暂时没法直到具体车位, 所以暂时设置为 optional
    parking_info = ReferenceField(Parking)
    # 懒加载, 到时候我们要根据 pk 搜索日志, 所以必须要用这个为了效率
    vehicle = LazyReferenceField(Vehicle, required=True)
    # 非会员用户或者储值卡(top-up)用户
    fee = DecimalField(min_value=0., precision=3)
    # 如果使用了(储值卡/记次卡)才需要用到 member_card
    member_card = ReferenceField(MemberCard)
    indoor = LazyReferenceField(Door, require=True)
    outdoor = LazyReferenceField(Door, require=True)
    admin_info = StringField(max_length=50, required=True)


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
