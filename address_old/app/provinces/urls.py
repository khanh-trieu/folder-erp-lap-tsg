
from django.urls import path

from provinces.views import *

urlpatterns = [
    path('provinces', ProvincesViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('provinces/<int:pk>', ProvincesViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete',
    })),
    path('districts', DistrictViewSet.as_view({
        'get': 'list',
    })),
    path('wards', WardsViewSet.as_view({
        'get': 'list',
    })),
    path('districts/<int:pk>', DistrictViewSet.as_view({
        'get': 'retrieve',
    })),
    path('wards/<int:pk>', WardsViewSet.as_view({
        'get': 'retrieve',
    })),
]