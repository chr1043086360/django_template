'''
Author ： CHR_崔贺然
Time ： 2019.12.12
Description ： 跨域中间件,没用第三方组件
               使用第三方组件: https://www.jianshu.com/p/8f43ad5482f4
'''

from django.middleware.security import SecurityMiddleware
from django.utils.deprecation import MiddlewareMixin


class ZhuLinCors(MiddlewareMixin):
    # Django中 的 Aop
    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        return response
