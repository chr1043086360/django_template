#######################################################################################
# Class ：限流
# Function ：
# Description ：{"ip", [time1, time2]}
#######################################################################################
from rest_framework import throttling
import time

# 其实不用自己写,有现成的
class ZhuLinThrottle(throttling.BaseThrottle):

    VisitRecord = {}
    def __init__(self):
        self.history = []
    def allow_request(self, request, view):
        ip = request.META.get("REMOTE_ADDR")
        now = time.time()
        if ip not in self.VisitRecord:
            self.VisitRecord[ip] = [now, ]
            return True
        history = self.VisitRecord[ip]
        history.insert(0, now)
        self.history = history
        while history and history[0] - history[-1] > 60:
            history.pop()
        if len(history) > 3:
            return False
        else:
            return True

    def wait(self):
        # 等待时间
        return self.history[-1] +60 - self.history[0]


# 框架的需要配置SETTINGS
class MyVisit(throttling.SimpleRateThrottle):
    scope = "my_throttle"

    def get_cache_key(self, request, view):
        # 返回值为ip地址
        return self.get_ident(request)

