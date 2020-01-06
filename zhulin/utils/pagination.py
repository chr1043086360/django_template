#######################################################################################
# Class ： MyPagination
# Function ：
# Description ： 分页
#######################################################################################
from rest_framework import pagination

#######################################################################################
# Class ： PageNumberPagination
# Function ：
# Description ： 可以显示上一页和下一页
#######################################################################################
# class MyPagination(pagination.PageNumberPagination):
#     page_size = 2
#     page_query_param = 'page'
#     page_size_query_param = "size"
#     max_page_size = 4

#     def paginate_queryset(self, queryset, request, view=None):
#         pass

#######################################################################################
# Class ： LimitOffsetPagination
# Function ：
# Description ： offest:从第几个开始取
#######################################################################################

# class MyPagination(pagination.LimitOffsetPagination):
#     default_limit = 2
#     limit_query_param = 'limit'
#     offset_query_param = 'offset'
#     max_limit = 4


#######################################################################################
# Class ： CursorPagination
# Function ： 
# Description ： ordering:以xx排序,对url还做了个加密的游标,记录最大索引和最小索引,查询速度是最快的
#######################################################################################

class MyPagination(pagination.CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 2
    ordering = '-id'  # 以id为倒叙排序
    page_size_query_param = "size"
    max_page_size = 4
    offset_cutoff = 1000