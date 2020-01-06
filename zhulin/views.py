from rest_framework import parsers
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.viewsets import ViewSetMixin
import hashlib

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from django.http import Http404, HttpResponse, request
from django.views import View
from .models import User
import json
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from .serializers.serializers import UserSerializer, BookSerializer
from zhulin.models import Book
# Create your views here.

#######################################################################################
# Description ： APIView对View做了封装,对request记性封装,对csrf做了豁免
#                后端给前端传递的数据都是列表套字典
#                通过更改里面的值来做外检关联
#                django是可以实现数据的序列化然后返回的
#######################################################################################

# DRF的API写法

#######################################################################################
# Class ： APIView和View区别
# Function ： request,csrf
# Description ： APIView继承了View,为了实现对View的拓展,封装了request,旧的request是_request
#                request.query_params ==> _request.GET
#                request.data ==> _request.POST _request.FIles
#                豁免了csrf,跨站攻击请求,防止别的钓鱼网站模拟请求提交恶意信息,给了个csrf_token
#                先走类的as_view()方法
#                super(APIView, cls).as_view():代表从哪个类之后往后找
#                从APIView往后找as_view(),不是执行父类的那么简单
#######################################################################################

#######################################################################################
# Class ： restful规范
# Function ： 验证,视图的封装
# Description ： rest风格的架构规范都是restful的,表述性状态转移
#                解决前后端交互的问题,资源   在web中只要有被引用的必要都叫资源
#                统一资源标识符  统一资源接口,遵循HTTP请求方式的语义
#                前后端传输叫资源的表述,前端展示的叫资源的状态,通过超链接的指引
#                告诉用户有哪些资源状态可以进入  尽量用名词,不要使用动词,根据HTTP请求的方式不同对资源进行操作
#                url尽量体现版本   返回值要携带状态码(公司内部规定的,方便前后端进行交互),携带错误信息
#                get返回查看的所有或者单条信息    post返回新增的数据   put返回更新的那条数据
#                delete返回空   分页携带超链接
#######################################################################################

from rest_framework import request, status


class UserResponse(APIView):
    def get(self, request):
        print(request._data)
        query = User.objects.all()
        # 创建出一个序列化器
        res = UserSerializer(query, many=True)

        return Response(res.data)
    #######################################################################################
    # Class ： UserResponse
    # Function ： post
    # Description ： post请求接口用来处理上传的数据
    #######################################################################################

    def post(self, request):
        # 获取请求
        book_obj = request.data
        # 去序列化器进行校验
        ser_obj = BookSerializer(data=book_obj)
        # 是否校验通过
        if ser_obj.is_valid:
            ser_obj.save()
            return Response(ser_obj.data)
        else:
            return Response(ser_obj.errors)

    def delete(self, request, id):
        book_obj = Book.objects.filter(id=id).first()
        if book_obj:
            book_obj.delete()
            return Response("")
        return Response("删除的对象不存在")

# 模板项目


def index(request):
    return render(request, "index.html")

# ping接口用来做生死检查


def ping(request):

    return HttpResponse("pong")

# CBV


class TestView(View):
    def get(self, request):
        pass
    #     queryset = User.objects.values()
    #     queryset_list = list(queryset)
    #     # dumps执行流程:cls----JsonEcoder()  会有一张表,表示Json可以处理的数据
    #     res = json.dumps(queryset_list, ensure_ascii=False)
    #     # return HttpResponse(res)
    #     return JsonResponse(queryset_list, self=False, json_dumps_params={"ensure_ascii": False})

    #     book_query = Book.objects.values(
    #         "id", "title", "pub_time", "publisher")
    #     book_list = list(book_query)
    #     # 申请一个新列表用来存储更新后的数据
    #     ret = []
    #     for book in book_list:
    #         publisher_obj = Publisher.objects.filter(
    #             id=book["publisher"]).first()
    #         book["publisher"] = {
    #             "id": publisher_obj.id,
    #             "title": publisher_obj.title
    #         }
    #         ret.append(book)
    #     return JsonResponse(ret, safe=False, json_dumps_params={"ensure_ascii": False})


#######################################################################################
# Class ： BookModelView
# Function ： ModelViewSet
# Description ： 继承了ModelViewSet
# class ModelViewSet(mixins.CreateModelMixin,
#                    mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.ListModelMixin,
#                    GenericViewSet):
#                    在urls里面就可以通过as_view()传参了
#######################################################################################


# class BookModelView(ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


#######################################################################################
# Class ： 官网示例
# Function ： api_view
# Description ： FBV的写法,有点类似于其他的SpringBoot的框架了
#######################################################################################

# @api_view(['GET', 'POST'])
# def api_view(request):
#     if request.method == 'GET':
#         snippets = Book.objects.all()
#         api_serializer = BookSerializer(snippets, many=True)
#         return Response(api_serializer.data)
#
#     elif request.method == 'POST':
#         api_serializer = BookSerializer(data=request.data)
#         if api_serializer.is_valid():
#             api_serializer.save()
#             return Response(api_serializer.data, status=status.HTTP_201_CREATED)
#         return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     try:
#         snippet = Book.object.get(pk=pk)
#
#     except Book.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         api_serializer = BookSerializer(snippet)
#         return Response(api_serializer.data)
#
#     if request.method == 'PUT':
#         api_serializer = BookSerializer(snippet, data=request.data)
#         if api_serializer.is_valid():
#             api_serializer.save()
#             return Response(api_serializer.data)
#         return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#######################################################################################
# Class ：
# Function ： CBV
# Description ：
#######################################################################################

# class SnippetDetail(APIView):
#
#     def get_object(self, pk):
#         try:
#             return Book.object.get(pk=pk)
#         except Book.DoesNotExit:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         api_serializer = BookSerializer(snippet)
#         return Response(api_serializer.data)
#
#     def put(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         api_serializer = BookSerializer(snippet)
#         if api_serializer.is_valid():
#             api_serializer.save()
#             return Response(api_serializer.data, status=status.HTTP_200_OK)
#         return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# 重写了as_view()方法,两者的返回值一样,做了一个csrf豁免,返回的其实还是一个view


#######################################################################################################
# 第三次封装
# class ModelViewSet(ViewSetMixin, GenericAPIView, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
#     pass
#
# class BookModelView(ModelViewSet):
#     # 如果用人家写好的queryset必须这么写,并且urls参数里面必须带有pk,自动生成了传参的路由(将生成好的路由注册进去)
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


class Register(APIView):
    def post(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        nickName = request.data.get("nickName")
        phoneNum = request.data.get("phoneNum")
        if password:
            md = hashlib.md5()
            md.update(password.encode("utf-8"))
            res_password = md.hexdigest()  # 定长32位
            print(res_password)

            if username and res_password:
                User.objects.create(username=username,
                                    nickName=nickName, phoneNum=phoneNum)
                User.objects.create(password=res_password)
                return Response("注册成功", status=status.HTTP_200_OK)
            return Response("注册失败", status=status.HTTP_400_BAD_REQUEST)


#######################################################################################
# Class ：
# Function ：
# Description ： django不支持post的json数据(支持form),只能通过post.body里面去拿然后还得自己做处理
#                可以配置某个视图只用什么方法做解析
#######################################################################################


class JsonView(APIView):
    # 只能解析json的请求
    parser_classes = [parsers.JSONParser, ]

    def get(self, request):
        # 核心方法,调用data才做解析
        print(request.data)
        pass
