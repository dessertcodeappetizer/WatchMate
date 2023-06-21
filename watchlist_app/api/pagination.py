from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 3                                       #number of pages
    page_query_param = "P"                              #it will rename the "page" in the url
    page_size_query_param = "size"                      #http://127.0.0.1:8000/watch/list2/?size=5 we can set the size of the page
    max_page_size = 5                                   #Even if we set the above size to 6 we will get 5 entity
    last_page_strings = "last_page"
    
class LimitOffsetPaginationLO(LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'limit'
    offset_query_param = 'start'
    max_limit = 5                                       #maxm limit a user can set
    
class CurserPagination(CursorPagination):
    page_size = 3
    ordering = "created"
    cursor_query_param = "cursor"