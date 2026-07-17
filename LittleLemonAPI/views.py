from rest_framework.permissions import BasePermission
from rest_framework import viewsets
from django.contrib.auth.models import User
from .serializers import UserSerializer

class IsManager(BasePermission):
    def has_permission(self, request, view):
        # breakpoint()  # 🛑 The code will pause right here!
        # print(request.user)
        # print(request.user.is_authenticated)
        # print(request.user.groups.all())
        # print(request.user.groups.filter(name='Manager').exists())
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()

class ManagerGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer