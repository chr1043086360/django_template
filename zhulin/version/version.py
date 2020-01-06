from django.http import request
from rest_framework.response import Response
from rest_framework.views import APIView


class DemoView(APIView):
    def get(self, request):
        return Response("版本测试接口")