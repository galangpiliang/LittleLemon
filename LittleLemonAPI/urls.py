from django.urls import include, path
from .views import ManagerGroupViewSet
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('manager/users/', ManagerGroupViewSet.as_view({'get': 'list'}), name='manager-users-list'),
] + debug_toolbar_urls()