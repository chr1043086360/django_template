from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models

# Create your models here.
# __all__ = ["User", "Profile"]


class User(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=60)
    SEX = (
        ('1', '男性'),
        ('2', '女性'),
    )
    nickName = models.CharField(max_length=32)
    phoneNum = models.CharField(max_length=16)
    sex = models.CharField(max_length=8, choices=SEX)
    birth_year = models.IntegerField(default=2000, verbose_name="出生年")
    birth_month = models.IntegerField(default=1, verbose_name="出生月")
    birth_day = models.IntegerField(default=1, verbose_name="出生日")
    avatar = models.CharField(max_length=256, verbose_name="个人形象")
    location = models.CharField(max_length=32, verbose_name="长居地")
    CHOICES = ((1, "vip"), (2, "svip"), (3, "vvip"))
    type = models.IntegerField(choices=CHOICES, default=1)
    token = models.CharField(max_length=60, default="666")


class Profile(models.Model):
    SEX = (
        ('1', '男性'),
        ('2', '女性'),
    )
    location = models.CharField(max_length=32, verbose_name="目标城市")

    min_distance = models.IntegerField(default=1, verbose_name="最小查找范围")
    max_distance = models.IntegerField(default=10, verbose_name="最大查找范围")

    min_dating_age = models.IntegerField(default=18, verbose_name="最小交友年龄")
    max_dating_age = models.IntegerField(default=50, verbose_name="最大交友年龄")

    dating_sex = models.CharField(
        max_length=8,  choices=SEX, verbose_name="匹配性别")
    vibration = models.BooleanField(default=True, verbose_name="是否要开启震动")
    only_match = models.BooleanField(default=True, verbose_name="不让为匹配的人看我的相册")
    auto_play = models.BooleanField(default=True, verbose_name="是否自动播放视频")


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    # author = models.CharField(max=32)
    title = models.CharField(max_length=32)
    CHOICES = ((1, "Linux"), (2, "Django"), (3, "Python"))
    # chapter = models.ChoiceField(choices=CHOICES)
    pub_time = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


#######################################################################################
# Class ：PricePolicy  DegreeCourse  Course
# Function ：
# Description ：价格策略表,优惠券表和不同的课程去关联,因为不可能在价格策略表中每一个都加一门课程的FK
#               所以需要加上课程表的id,通过id去django默认的ContentType表中取表名
#######################################################################################
class DegreeCourse(models.Model):
    name = models.CharField(max_length=32)


class Course(models.Model):
    name = models.CharField(max_length=32)

    policy_list = GenericRelation("PricePolicy")


class PricePolicy(models.Model):
    content_type = models.ForeignKey(
        to=ContentType, on_delete=False, related_name=None)
    object_id = models.PositiveIntegerField()
    content_obj = GenericForeignKey('content_type', 'object_id')

    period = models.CharField(max_length=32)
    price = models.FloatField()


# Django在背后都默认给你做了
# course_obj = Course.objects.get(id=1)
# PricePolicy.objects.create(period='10', price='9.9', content_obj=course_obj)
# policy_list = course_obj.policy_list.all()
# for policy in policy_list:
#     print(policy)


#######################################################################################
# Class ：
# Function ：
# Description ： 一对一关系可以用来做简介和详情
#######################################################################################
