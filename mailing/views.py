from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import MailingListSerializer
from .models import MailingList
from django.conf import settings
from django.template.loader import render_to_string
from .tasks import send_email
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def contact(request):
    data = request.data
    print(data)
    from_mail = data['from']
    name = data['name']
    client_msg = data['msg']
    
    current_site = settings.DOMAIN
    message = render_to_string('contact_email.html', {
                'client_name': name, 
                'domain':current_site,
                'client_email': from_mail,
                'message':client_msg
            })
    send_email.delay("new contact message (Foodtrack)", message, settings.CONTACT_EMAIL, from_mail)
    
    return Response({"state":"Message sent to redis"}, status=status.HTTP_200_OK)

class MailingListView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()