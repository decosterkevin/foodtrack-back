
from core.serializers import ExploitationSerializer
from core.models import Exploitation
from core.permissions import IsCreatorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import  ListAPIView, RetrieveUpdateDestroyAPIView

## Exploitation View
class ExploitationView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExploitationSerializer
    queryset = Exploitation.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['creator', 'address']
    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(creator=user)

class SingleExploitationView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsCreatorOrReadOnly)
    queryset = Exploitation.objects.all()
    serializer_class = ExploitationSerializer