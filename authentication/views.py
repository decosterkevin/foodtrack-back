from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.http import HttpResponse

from rest_framework.generics import RetrieveUpdateAPIView,RetrieveAPIView
from rest_framework import routers, serializers, viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, RegistrationSerializer, SocialSerializer
from .models import User
from .renderers import UserJSONRenderer
from .tokens import account_activation_token
from rest_framework_simplejwt.tokens import RefreshToken


# from social_django.utils import psa

from mailing.tasks import send_email
# Create your views here.

# ViewSets define the view behavior.
@permission_classes([AllowAny])
@authentication_classes([])
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.mail_confirmed = True
        user.save()
        login(request, user)
        # return redirect('home')
        return redirect(settings.FRONTEND_URL + '/login')
    else:
        return HttpResponse('Activation link is invalid, contact support')

class UserView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    def get_object(self):
        queryset = self.get_queryset()
        obj = User.objects.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    authentication_classes = ()
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save()
        current_site = settings.DOMAIN
        
        user = User.objects.get(email=request.data['email'])
        message = render_to_string('activation_email.html', {
                'user': user, 
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        send_email.delay("Confirme your identity", message, user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()
    # renderer_classes = (UserJSONRenderer,)

    def post(self, request):

        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        if User.objects.filter(email=email).first() is None:
            raise serializers.ValidationError(
                'User does not exists, please register.'
            )
        
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'Wrong password, please try again'
            )
        

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        if not user.mail_confirmed:
            raise serializers.ValidationError(
                'You did not confirme your email yet. Please check your mailbox.'
            )
        res =  {
            'email': user.email,
            'token': user.token['access']
        }
        return Response(res, status=status.HTTP_200_OK)


                # generated as to why specifically the authentication failed;
                # generated as to why specifically the authentication failed;

# @api_view(http_method_names=['POST'])
# @permission_classes([AllowAny])
# @psa()
# def exchange_token(request, backend):
#     """
#     Exchange an OAuth2 access token for one for this site.
#     This simply defers the entire OAuth2 process to the front end.
#     The front end becomes responsible for handling the entirety of the
#     OAuth2 process; we just step in at the end and use the access token
#     to populate some user identity.
#     The URL at which this view lives must include a backend field, like:
#         url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),
#     Using that example, you could call this endpoint using i.e.
#         POST API_ROOT + 'social/facebook/'
#         POST API_ROOT + 'social/google-oauth2/'
#     Note that those endpoint examples are verbatim according to the
#     PSA backends which we configured in settings.py. If you wish to enable
#     other social authentication backends, they'll get their own endpoints
#     automatically according to PSA.
#     ## Request format
#     Requests must include the following field
#     - `access_token`: The OAuth2 access token provided by the provider
#     """
#     serializer = SocialSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         # set up non-field errors key
#         # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
#         try:
#             nfe = settings.NON_FIELD_ERRORS_KEY
#         except AttributeError:
#             nfe = 'non_field_errors'

#         try:
#             # this line, plus the psa decorator above, are all that's necessary to
#             # get and populate a user object for any properly enabled/configured backend
#             # which python-social-auth can handle.
#             user = request.backend.do_auth(serializer.validated_data['access_token'])
#         except HTTPError as e:
#             # An HTTPError bubbled up from the request to the social auth provider.
#             # This happens, at least in Google's case, every time you send a malformed
#             # or incorrect access key.
#             return Response(
#                 {'errors': {
#                     'token': 'Invalid token',
#                     'detail': str(e),
#                 }},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if user:
#             if user.is_active:
#                 token, _ = Token.objects.get_or_create(user=user)
#                 return Response({'token': token.key})
#             else:
#                 # user is not active; at some point they deleted their account,
#                 # or were banned by a superuser. They can't just log in with their
#                 # normal credentials anymore, so they can't log in with social
#                 # credentials either.
#                 return Response(
#                     {'errors': {nfe: 'This user account is inactive'}},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         else:
#             # Unfortunately, PSA swallows any information the backend provider
#             # generated as to why specifically the authentication failed;
#             # this makes it tough to debug except by examining the server logs.
#             return Response(
#                 {'errors': {nfe: "Authentication Failed"}},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


# Profile View

    # def get(self, request, *args, **kwargs):
    #     user_id = request.query_params.get('user_id')
    #     try:
    #         user = User.objects.get(id=user_id)
    #     except  User.DoesNotExist:
    #         user= request.user
    #     serializer = self.serializer_class(user.user_profile)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


# Create your views here.
