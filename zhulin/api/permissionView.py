from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils.auth import MyAuth
from ..utils.permission import MyPermission
from django.http import request
from django.views import View

class permissionView(APIView):
    # 配置认证类(可以用django的session,token)
    authentication_classes = [MyAuth, ]
    # 配置权限类,一般在互联网项目应用较少(在公司内部的项目应用多CRM系统什么的)
    permission_classes = [MyPermission]
    # 接口只能vip访问
    def get(self, request):
        # print(request.user)
        # print(request.auth)
        return Response("权限测试接口")
