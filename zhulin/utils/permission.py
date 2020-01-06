from rest_framework import permissions

class MyPermission(permissions.BasePermission):
    message = "权限不足"
    # 如果没有这个方法会拒绝访问
    def has_permission(self, request, view):
        # 判断用户是否有权限
        if request.user.type in [1,3]:
            return True
        return False
