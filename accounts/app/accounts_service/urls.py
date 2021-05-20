
from django.urls import path, include
from accounts_service.views import AccountViewSet

urlpatterns = [
    path('accounts', AccountViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('accounts/<int:pk>', AccountViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
    })),
    # path('accounts/<int:pk>/<int:user_id>', AccountViewSet.as_view({
    #     'delete': 'delete',
    # })),
    path('accounts/check-tax-code', AccountViewSet.as_view({
        'get': 'check_tax_code_api',
    })),
    path('accounts/information-company', AccountViewSet.as_view({
        'get': 'get_information_company',
    })),
    path('accounts/list-element', AccountViewSet.as_view({
        'get': 'list_all_element',
    })),
    path('accounts/list-element-address', AccountViewSet.as_view({
        'get': 'list_all_element_address',
    })),
    path('accounts/load-data-first', AccountViewSet.as_view({
        'get': 'load_data_first',
    }))
]
