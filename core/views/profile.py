from core.serializers import ProductorProfileSerializer,SimpleProductorProfileSerializer, UserProfileSerializer#, ProductorProfileFullSerializer
from core.models import ProductorProfile, UserProfile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import  RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets

class ProductorProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductorProfileSerializer
    filter_backends = [DjangoFilterBackend]
    queryset = ProductorProfile.objects.all()
    def prefetch_related(cls, queryset, request):
        queryset = queryset.select_related("creator")
        return queryset
    def get_queryset(self):
        box = self.request.query_params.get("box", None)
        if box:
            [xmin, ymin, xmax, ymax] = box.split(',')
            poly = Polygon.from_bbox((xmin, ymin, xmax, ymax))
            return ProductorProfile.objects.filter(address__point__within=poly)
        else:
            return ProductorProfile.objects.all()

    def get_serializer_class(self):
        with_products = self.request.query_params.get("with_products", "False") == "True"
        if with_products:
            return ProductorProfileSerializer
        else:
            return SimpleProductorProfileSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend]
