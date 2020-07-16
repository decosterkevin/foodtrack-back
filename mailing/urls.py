from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MailingListView, contact

# router = DefaultRouter()
# router.register(r'products', ProductView)
# router.register(r'products/<int:pk>', SingleProductView)

urlpatterns = [
   path('subscribe', MailingListView.as_view()),
   path('contact', contact)
]