from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """Пагинация страниц."""
    page_size_query_param = 'limit'
