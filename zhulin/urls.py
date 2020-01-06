from django.conf.urls import url

from . import views
from rest_framework.routers import DefaultRouter
from zhulin.api import permissionView
# from zhulin.views import BookModelView

# 实例化对象
# router = DefaultRouter()

# 把路由和视图注册进去
# 这里只能生成支持传参的路由
# router.register(r'list', BookModelView)


urlpatterns = [

    url(r"ping", views.ping),
    url(r'register', views.Register.as_view()),
    url(r"user", views.UserResponse.as_view()),
    url(r"permission", permissionView.permissionView.as_view()),
    # url('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

# urlpatterns += router.urls
