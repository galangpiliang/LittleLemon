from django.urls import include, path
from .views import ManagerGroupViewSet, DeliveryCrewGroupViewSet, api_root, GroupViewSet, MenuItemViewSet
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', api_root, name='api-root'),

    path(
        'groups/', 
        GroupViewSet.as_view({
            'get': 'list', 
            'post': 'create', 
        }), 
        name='groups-list'
    ),

    # Single dictionary mapping GET, POST, and DELETE
    path(
        'groups/manager/users/', 
        ManagerGroupViewSet.as_view({
            'get': 'list', 
            'post': 'create', 
        }), 
        name='manager-users-list'
    ),
    path(
        'groups/manager/users/<int:pk>/', 
        ManagerGroupViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }), 
        name='manager-users-detail'
    ),
    
    path(
        'groups/delivery-crew/users/', 
        DeliveryCrewGroupViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), 
        name='delivery-crew-users-list'
    ),
    path(
        'groups/delivery-crew/users/<int:pk>/', 
        DeliveryCrewGroupViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }), 
        name='delivery-crew-users-detail'
    ),

    path(
        'menu-items/', 
        MenuItemViewSet.as_view({
            'get': 'list',
            'post': 'create',
        }), 
        name='menu-items-list'
    ),
        path(
        'menu-items/<int:pk>/', 
        MenuItemViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), 
        name='menu-items-detail'
    ),
]