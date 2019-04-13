# models use MongoDB
# from mongoengine import *
from mongoengine import Document


class Vehicle(Document):
    """
    TODO
    车辆信息
    """
    pass


class Parking(Document):
    """
    TODO:
    车位信息
    """
    pass


class ParkingLot(Document):
    """
    停车场信息
    """
    pass


class Bill(Document):
    """
    账单信息
    Time series
    """
    pass


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
