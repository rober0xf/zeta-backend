from rest_framework.pagination import PageNumberPagination


class SmallPagination(PageNumberPagination):
    page_query_param = "p"
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 3


class MediumPagination(PageNumberPagination):
    page_query_param = "p"
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 6


class LargePagination(PageNumberPagination):
    page_query_param = "p"
    page_size = 9
    page_size_query_param = "page_size"
    max_page_size = 9
