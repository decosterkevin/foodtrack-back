from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

cart_router = DefaultRouter()
cart_router.register(r'cart', views.CartView, basename="cart")

product_router = DefaultRouter()
product_router.register(r'products', views.ProductView, basename="products")

profile_router = DefaultRouter()
profile_router.register(r'productors', views.ProductorProfileViewSet, basename="productors")
profile_router.register(r'users', views.UserProfileViewSet, basename="users")

productor_router = DefaultRouter()
productor_router.register(r'products', views.ProductorProductView, basename="productor-products")

urlpatterns = [
   path('', include(product_router.urls)),
   path('profile/', include(profile_router.urls)),
   path('', include(cart_router.urls)),
   path('productor/<int:creator_id>/', include(productor_router.urls)),
   # path('exploitations', ExploitationView.as_view()),
   # path('exploitations/<int:pk>', SingleExploitationView.as_view()),
]