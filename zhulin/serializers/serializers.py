#######################################################################################
# Author ： CHR_崔贺然
# Time ： 12.13
# Description ： 序列化的流程
# 先声明一个序列化器,拿到序列化器传入从数据库中传入的参数
#######################################################################################

# from rest_framework import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.parsers import JSONParser

from zhulin.models import Book
from rest_framework import views
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets

#######################################################################################
# Class ：
# Function ：
# Description ：
#######################################################################################


class UserSerializer(serializers.Serializer):
    SEX = (
        ('男性', '男性'),
        ('女性', '女性'),
    )
    nickName = serializers.CharField(max_length=32)
    phoneNum = serializers.CharField(max_length=16)
    # get_sex_display:可以拿到里面的值
    sex = serializers.CharField(
        max_length=8, source="get_sex_display", read_only=True)
    birth_year = serializers.IntegerField(default=2000)
    birth_month = serializers.IntegerField(default=1)
    birth_day = serializers.IntegerField(default=1)
    avatar = serializers.CharField(max_length=256)
    location = serializers.CharField(max_length=32)



# def my_validate(value):
#     if value.lower() in "敏感词汇":
#         raise serializers.ValidationError("输入的信息含有敏感词汇")
#     return value

class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=32)
    # title = serializers.CharField(max_length=32, validator=[my_validate, ])
    CHOICES = ((1, "Linux"), (2, "Django"), (3, "Python"))
    # read_only和write_only:分别为正序列化和反序列化
    category = serializers.ChoiceField(
        choices=CHOICES, source="get_category_display", read_only=True)
    post_category = serializers.IntegerField(write_only=True)
    pub_time = serializers.DateField()
    user = UserSerializer(many=True, read_only=True)
    publisher_id = serializers.IntegerField(write_only=True)
    # author_list = serializers.ListSerializer(write_only=True)

    #######################################################################################
    # Class ： BookSerializer
    # Function ： create
    # Description ： 必须要重写create,在数据库中创建create数据,用来写ORM的数据
    #                序列化和反序列化的时候字段不统一的情况:
    #                required=False(在反序列化的时候不做校验)
    #                read_only=True\write_only=True:一正一反
    #######################################################################################

    def create(self, validated_data):
        print(validated_data)
        book_obj = Book.objects.create(
            title=validated_data["title"], pub_time=validated_data["pub_time"],
            category=validated_data["category"], publisher_id=validated_data["publisher_id"])
        book_obj.author.add(*validated_data["author_list"])
        return book_obj

    def update(self, instance, validated_data):
        # instance is 传入的参数:queryset(book_obj)
        instance.title = validated_data.get("title", instance.title)
        instance.pub_time = validated_data.get("pub_time", instance.pub_time)
        instance.category = validated_data.get("category", instance.category)
        instance.publisher = validated_data.get("title", instance.title)
        if validated_data.data.get("author_obj", False):
            # add后面需要加上*,set后面不用加*
            instance.authors.set(validated_data["author_list"])
        instance.save()
        return instance

    #######################################################################################
    # Class ：
    # Function ： validate_title
    # Description ： 单个参数的校验方法名为validate_字段名称(self, value)
    #                如果正确就会return value,如果出现异常raise serializers.ValidationError("自定义错误信息")
    #######################################################################################



    #######################################################################################
    # Class ：
    # Function ：validate
    # Description ： 多字段校验
    #######################################################################################
    # def validate(self, attrs):
    #     pass
#######################################################################################
# Class ：
# Function ： my_validate
# Description ： 校验是否含有敏感词汇,可以自定义校验
#                配置校验给字段加validator=[my_validate,]
#######################################################################################




#######################################################################################
# Class ： 校验规则权重
# Function ：
# Description ： 自定义规则的权重最高,其次是单个字段,最后是全局字段校验
#######################################################################################

# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         # 序列化器
#         fields = ["id", "title", "pub_time"]
#         # fields = "__all__"
#         # exclude = ["author"]  # 排除某些字段
#         # 顺着表的外检关系找几层
#         # depth = 1  # 让所有的外检关系变成read_only=True
#         # extra_kwargs = {
#         #     "字段名称":{"参数"}
#         # }
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(
#         required=False, allow_blank=True, max_length=100)
#     # code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#
#     def create(self, validated_data):
#         return Book.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.save()
#         return instance


#######################################################################################
# Class ：
# Function ：
# Description ：
#######################################################################################
# @csrf_exempt
# def snippet_list(request):
#     if request.method == "GET":
#         snippets = Book.objects.all()
#         serializer_snippet = BookSerializer(snippets, many=True)
#         return JsonResponse(serializer_snippet.data, safe=False)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer_snippet = BookSerializer(data=data)
#         if serializer_snippet.is_valid():
#             serializer_snippet.save()
#             return JsonResponse(serializer_snippet.data, status=201)
#         return JsonResponse(serializer_snippet.data, status=400)
