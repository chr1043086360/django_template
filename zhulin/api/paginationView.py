from rest_framework.response import Response
from django.http import request
from rest_framework.views import APIView

from zhulin.models import Book
from ..utils.pagination import MyPagination
from ..serializers.serializers import BookSerializer
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

# 可以不自己写
class PaginationView(APIView):
    def get(self, request):
        # 从数据库中取Book
        queryset = Book.objects.all()
        # 创建一个分页器
        zhulin_page = MyPagination()
        # 返回分页后的数据
        ret_page = zhulin_page.paginate_queryset(queryset, request)
        # 将分页后的数据传入BookSerializer
        ret_serializer = BookSerializer(ret_page, many=True)
        # 如果有返回值return 200
        if ret_serializer:
            # return Response(ret_serializer.data, status=status.HTTP_200_OK)
            return MyPagination.get_paginated_response(ret_serializer.data)
        # 否则返回400
        return Response("序列化错误", status=status.HTTP_400_BAD_REQUEST)


# 使用封装,内部自动进行分页
class PaginationModelView(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = MyPagination  # 这里只能配置一个

    def get(self,request):
        return self.list(request)
