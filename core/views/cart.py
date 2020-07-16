from core.serializers import CartItemSerializer, CartSerializer
from core.models import Cart, CartItem, Product

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes,  action
from django.contrib.gis.geos import Point, Polygon
from core.permissions import IsCreatorOrReadOnly

## Product View
class CartView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsCreatorOrReadOnly)
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'creator', 'checked_out']
    
    def create(self, request):
        user = self.request.user
        data = request.data
        data['creator'] = user.user_profile.id
        serializer = self.get_serializer_class()(data=data)
        if serializer.is_valid():
            if Cart.objects.filter(checked_out=False).count() < 1:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response("Cart not checked out already exist", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        user_profile = request.user.user_profile
        data = request.data.copy()
        print(data)
        cart = self.get_object()
        product_id = data['product_id']
        quantity = int(data['quantity'])
        product = Product.objects.get(pk=product_id)
        if product and product.quantity >= quantity:
            cartItem = cart.items.filter(product = product).first()
            if cartItem:
                #cappend quantity
                cartItem.quantity += quantity
                cartItem.save()
                product.quantity = product.quantity - quantity
                product.save()
                return Response("CartItem modified with success", status=status.HTTP_200_OK)
            else:
                cart_item_data = {
                    'product': product,
                    'quantity': quantity,
                    'unit_price': product.price,
                    'cart' : cart
                }
                cart = CartItem(**cart_item_data)
                cart.save()
                serializer = CartItemSerializer(cart)
                product.quantity = product.quantity - quantity
                product.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response("Not enough quantity", status=status.HTTP_400_BAD_REQUEST)

        

    @action(detail=True, methods=['post'])   
    def remove_from_cart(self, request, pk=None):
        user_profile = request.user.user_profile
        data = request.data.copy()
        cart = self.get_object()
        print(data)
        product_id = data['product_id']
        quantity = int(data['quantity'])
        product = Product.objects.get(pk=product_id)
        product.quantity = product.quantity + quantity
        product.save()

        cartItem = cart.items.filter(product = product).first()
        if cartItem.quantity == quantity:
            cartItem.delete()
            cart.save()

            product.quantity = product.quantity + quantity
            product.save()
            return Response("CartItem removed with success", status=status.HTTP_200_OK)
        else:
            cartItem.quantity = cartItem.quantity - quantity
            cartItem.save()

            product.quantity = product.quantity + quantity
            product.save()
            return Response("CartItem quantity modified with success", status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])   
    def empty_cart(self, request, pk=None):
        user_profile = request.user.user_profile
        cart = self.get_object()
        for cart_item in cart.items.all():
            product = cart_item.product
            cart_item.delete()
            product.quantity += cart_item.quantity
            product.save()
        
        return Response("Cart emptied with success", status=status.HTTP_200_OK)

        
