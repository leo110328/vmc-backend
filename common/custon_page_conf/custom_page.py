from django.core.paginator import InvalidPage
from rest_framework.pagination import PageNumberPagination


class CustomPagePagination(PageNumberPagination):
    # 每页数目
    page_size = 10
    # 前端最多能设置的每页数量
    max_page_size = 100
    page_size_query_param = 'size'
    # 前端最多能设置的每页数量
    page_query_param = 'page'

    def __init__(self):
        self.page = None
        self.request = None

    def paginate_queryset(self, queryset, request, view=None):
        empty = True

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            empty = False
            pass

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request

        if not empty:
            self.page = []

        return list(self.page)
