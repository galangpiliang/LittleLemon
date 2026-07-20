from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('groups-list', request=request, format=format),
        'manager-users': reverse('manager-users-list', request=request, format=format),
        'delivery-crew-users': reverse('delivery-crew-users-list', request=request, format=format),
    })

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ManagerGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = UserSerializer

    def create(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        manager_group, created = Group.objects.get_or_create(name='Manager')
        user.groups.add(manager_group)

        return Response({'message': f'User {username} added to Manager group.'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):       
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            manager_group = Group.objects.get(name='Manager')
        except Group.DoesNotExist:
            return Response({'error': 'Manager group does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.groups.filter(name='Manager').exists():
            return Response({'error': 'User is not in the Manager group.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.groups.remove(manager_group)
        return Response({'message': f'User {user.username} removed from Manager group.'}, status=status.HTTP_200_OK)

class DeliveryCrewGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManager]
    queryset = User.objects.filter(groups__name='Delivery crew')
    serializer_class = UserSerializer

    def create(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        delivery_crew_group, created = Group.objects.get_or_create(name='Delivery crew')
        user.groups.add(delivery_crew_group)

        return Response({'message': f'User {username} added to Delivery crew group.'}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):       
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            delivery_crew_group = Group.objects.get(name='Delivery crew')
        except Group.DoesNotExist:
            return Response({'error': 'Delivery crew group does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.groups.filter(name='Delivery crew').exists():
            return Response({'error': 'User is not in the Delivery crew group.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.groups.remove(delivery_crew_group)
        return Response({'message': f'User {user.username} removed from Delivery crew group.'}, status=status.HTTP_200_OK)