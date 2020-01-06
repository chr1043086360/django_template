"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from zhulin import views
from zhulin.version import version
from zhulin.api import index
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('zhulin/api/v1', include(("zhulin.urls", "zhulin"), namespace="zhulin")),
    # path('', views.index),
    path('', index.Index.as_view()),
    path('version', version.DemoView.as_view()),
    path('test', views.TestView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


