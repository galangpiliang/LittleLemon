from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    menuitem = serializers.StringRelatedField(read_only=True)

    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(), 
        write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

        read_only_fields = ['unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    delivery_crew = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    menuitem = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price'] 
