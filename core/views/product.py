from rest_framework import viewsets
from core.serializers import ProductSerializer, FullProductSerializer
from core.models import Product

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import viewsets
from django.contrib.gis.geos import Point, Polygon
from core.permissions import IsCreatorOrReadOnly

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def add_to_favorite(request, pk):
#     user_profile = request.user.user_profile
#     if user_profile:
#         product = Product.objects.get(pk=pk)
#         if not product in user_profile.saved_products.all():
#             user_profile.saved_products.add(product)
#             txt = "Product added from favorites with success"
#         else:
#             txt = "Product already in favorites"
        
#         return Response(txt, status=status.HTTP_200_OK)
#     return Response("this product does not exist", status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def remove_from_favorite(request, pk):
#     user_profile = request.user.user_profile
#     if user_profile:

#         product = Product.objects.get(pk=pk)
#         user_profile.saved_products.remove(product)
#         user_profile.save()
#         return Response("Product removed from favorites with success", status=status.HTTP_200_OK)

#     return Response("this product does not exist", status=status.HTTP_400_BAD_REQUEST)


## Product View
class ProductView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['creator', 'name', 'is_deliverable', "price", "quantity", "is_active", "delivery_time_days"]

    def get_queryset(self):
        box = self.request.query_params.get("box", None)
        if box:
            [xmin, ymin, xmax, ymax] = box.split(',')
            poly = Polygon.from_bbox((xmin, ymin, xmax, ymax))
            return Product.objects.select_related('creator').filter(creator__address__point__within=poly).filter(quantity__gt=0)
        else:
            return Product.objects.filter(quantity__gt=0)

    def get_serializer_class(self):
        with_creator = self.request.query_params.get("with_creator", "False") == "True"
        if with_creator:
            return FullProductSerializer
        else:
            return ProductSerializer

    @action(detail=True, methods=['get'])
    def add_to_favorite(self, request, pk=None):
        user_profile = request.user.user_profile

        product = self.get_object()
        if not product in user_profile.saved_products.all():
            user_profile.saved_products.add(product)
            txt = "Product added from favorites with success"
        else:
            txt = "Product already in favorites"
            
        return Response(txt, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def remove_from_favorite(self, request, pk=None):
        user_profile = request.user.user_profile

        product = self.get_object()
        user_profile.saved_products.remove(product)
            
        return Response("Product remove from favorite with success", status=status.HTTP_200_OK)


class ProductorProductView(ProductView, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsCreatorOrReadOnly)
    def get_queryset(self):
        creator_id = self.kwargs['creator_id']
        return Product.objects.filter(creator_id=creator_id).all()
    
    def create(self, request, creator_id=None):
        if creator_id:
            data = request.data
            data['creator'] = creator_id
            serializer = self.get_serializer_class()(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response("Saved with success", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)