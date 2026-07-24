from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework.permissions import BasePermission, AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .models import MenuItem, Cart, Order, OrderItem
from django.db import IntegrityError
from django.utils import timezone

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'groups': reverse('groups-list', request=request, format=format),
        'manager-users': reverse('manager-users-list', request=request, format=format),
        'delivery-crew-users': reverse('delivery-crew-users-list', request=request, format=format),
        'menu-items': reverse('menu-items-list', request=request, format=format),
        'cart': reverse('cart-list', request=request, format=format),
        'orders': reverse('orders-list', request=request, format=format),
    })

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
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

        return Response({'message': f'User {username} added to Manager group.'}, status=status.HTTP_201_CREATED)

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
        return Response({'message': f'User {user.username} removed from Manager group.'}, status=status.HTTP_200_SUCCESS)

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

        return Response({'message': f'User {username} added to Delivery crew group.'}, status=status.HTTP_201_CREATED)

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
        return Response({'message': f'User {user.username} removed from Delivery crew group.'}, status=status.HTTP_200_SUCCESS)

class MenuItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsManagerOrReadOnly]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def list(self, request):
        cart_items = self.get_queryset()
        serializer = self.serializer_class(cart_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        menuitem_id = request.data.get('menuitem_id')
        quantity = request.data.get('quantity')

        if not menuitem_id or not quantity:
            return Response({'error': 'Menu item ID and quantity are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            menuitem = MenuItem.objects.get(id=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Menu item does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        try:
            quantity = int(quantity)
        except ValueError:
            return Response({'error': 'Quantity must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        unit_price = menuitem.price
        total_price = unit_price * quantity

        try:
            cart_item = Cart.objects.create(
                user=request.user,
                menuitem=menuitem,
                quantity=quantity,
                unit_price=unit_price,
                price=total_price
            )
        except IntegrityError:
            return Response({'error': 'This menu item is already in the cart. Please update the quantity instead.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': f'Menu item {menuitem.title} added to cart.'}, status=status.HTTP_201_CREATED)

    def destroy_all(self, request):
        Cart.objects.filter(user=request.user).delete()
        return Response({'message': 'All items removed from cart.'}, status=status.HTTP_204_NO_CONTENT)

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
        else:
            return Order.objects.filter(user=user)

    def list(self, request):
        orders = self.get_queryset()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            order = self.get_queryset().get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        order_items = OrderItem.objects.filter(order=order)

        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data)

    def create(self, request):
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty. Cannot create order.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.price for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total=total_price,
            date=timezone.now().date(),
        )

        order_items = [
            OrderItem(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            ) for item in cart_items
        ]
        OrderItem.objects.bulk_create(order_items)

        serializer = self.serializer_class(order)
        cart_items.delete()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            order = self.get_queryset().filter(pk=pk).first()
            if not order:
                return Response({'error': 'Order does not exist.'}, status=status.HTTP_404_NOT_FOUND)
            
            order.delete()
            return Response({'message': 'Order deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'You do not have permission to delete this order.'}, status=status.HTTP_403_FORBIDDEN)