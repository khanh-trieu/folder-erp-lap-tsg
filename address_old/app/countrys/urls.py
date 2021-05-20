from django.urls import path

from countrys.views import CountsViewSet

urlpatterns = [
    path('countrys', CountsViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('countrys/<int:pk>', CountsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete',
    }))
]
