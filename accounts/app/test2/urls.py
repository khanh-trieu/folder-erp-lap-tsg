
from django.urls import path
from accounts_service.views import AccountViewSet
from test2.views import TestViewSet

urlpatterns = [
    path('tests', TestViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('tests/<int:pk>', TestViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
    # path('accounts/<int:pk>/<int:user_id>', AccountViewSet.as_view({
    #     'delete': 'delete',
    # })),

    path('tests/filed', TestViewSet.as_view({
        'get': 'crawl_filed',
    })),
    path('tests/update-code-address', TestViewSet.as_view({
        'get': 'update_code_address',
    })),
]