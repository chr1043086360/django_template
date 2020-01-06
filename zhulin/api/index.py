#######################################################################################
# Class ：
# Function ：
# Description ： 频率限制,分页器,渲染器,解析器
#                频率限制组件throttle
#######################################################################################
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import request
from django.views import View
from django.shortcuts import render
from ..utils.throttle import ZhuLinThrottle


class Index(APIView):
    throttle_classes = [ZhuLinThrottle, ]

    def get(self, request):
        return render(request, "index.html")
