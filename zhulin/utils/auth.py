from rest_framework import authentication, status

from ..models import User
from rest_framework.exceptions import AuthenticationFailed

class MyAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        # 获取前端携带的token比对是否合法
        token = request.query_params.get("token", "")
        if not token:
            raise AuthenticationFailed("没有携带token")
        try:
            user_obj = User.objects.filter(token=token).first()

        except AttributeError:
            raise AuthenticationFailed("token不合法")

        finally:
            return (user_obj, token)