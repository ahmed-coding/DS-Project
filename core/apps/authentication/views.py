from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView, Request, status
from rest_framework.generics import CreateAPIView, GenericAPIView
from django.contrib.auth import logout, authenticate, login
from rest_framework.permissions import IsAuthenticated

from .register import generit_random_code

from .serializers import ChechEmailValidateSerilzers, User, UserAuthSerializer, VerifySerializer


class CustomAuthToken(CreateAPIView):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ReigsterView(CreateAPIView):
    """
    ReigsterAPI to create user if request.session.has_key('email_code') and request.session.has_key('is_verify') is True
    and he will be replace the another view in User.view for Customer at new
    """
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    model = User
    serializer_class = UserAuthSerializer

    def post(self, request: Request):
        """
        Reigster User View to signup after verify the ``email`` or ``phone number`` (just email for new).
        Returns:
        - in_Success:
            - data: (``string``) -> message from server.
            - user: (``User``) -> data of user after created.
            - status_code : 200 
        - in_Fail:
            - error: (``string``) -> Error Message.
            - status: 401 when come bafore verify the ``email`` or ``phone_number``.
            - status: 400 when data isn't correct or somthing go to by wrong.
        """
        # print(generit_random_code())
        # print(type(generit_random_code()))

        # print(generit_random_code())
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):

    """
    this will be take ``refresh`` token and add it to blackList
    Method :
        >>> [POST]
        dont add more
    """
    # authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # serializer_class =

    def post(self, request: Request):
        """
        >>> LOGIN REQUIRD WITH JWT:
        - Try to get Authentication from User it's self by JWT[refresh].
        - then fo get AUTHORIZATION from request[META],

        Returns:
        - data: login done if the logiut success.
        - status: 200 or 401
        """
        # request.auth
        # d = TokenUser(request.auth)
        # d.delete()

        logout(request=request)
        return Response(data={
            'data': 'Logout done'
        }, status=status.HTTP_200_OK)

#### Email Method ######


class ChechEmailValidateView(GenericAPIView):
    """
    Chech Email View 
    Args:
        ``email`` (string).
    Returns:
        is_valid: Boolen (True or False)
        - if True mean it the Email is unuseable by any user
        - else mean it the Email is alredy exsits.
    """
    serializer_class = ChechEmailValidateSerilzers

    def post(self, request: Request):
        ser = self.serializer_class(
            data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            email = User.objects.get(email=ser.validated_data.get('email'))
            return Response({
                'is_valid': False
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'is_valid': True
            }, status=status.HTTP_200_OK)


class SendVerifyEmailView(GenericAPIView):
    """

    Args:
        GenericAPIView (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = VerifySerializer

    def post(self, request: Request):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid(raise_exception=True):
            code = generit_random_code()
            verify = ser.send_verify_email(code=code)
            if verify.get('is_sand'):
                request.session['email_code'] = code
                request.session['is_verify'] = False
                return Response({
                    'verify': verify,
                    'data': code,

                }, status=status.HTTP_200_OK)
            else:
                return Response(verify, status=status.HTTP_204_NO_CONTENT)

        # if request.data.get('email'):
        #     try:
        #         code = generit_random_code()
        #         print(code)
        #         email = request.data.get('email')
        #         template = loader.get_template('code_design.html').render({
        #             'code': code
        #         })
        #         send = EmailMessage(
        #             "Test OTP Form Django APIs Verify", template,  settings.EMAIL_HOST_USER, [email, ])
        #         # send_mail(
        #         #     f" Welcome Your Code : {code}.", settings.EMAIL_HOST_USER, [email, ], fail_silently=False)
        #         send.content_subtype = 'html'
        #         send.send()
        #         # {
        #         #     "email": "ahmed.128hemzh@gmail.com"
        #         # }
        #         request.session['email_code'] = code
        #         request.session['is_verify'] = False
        #         return Response({
        #             'code': code
        #         }, status=status.HTTP_200_OK)
        #     except Exception as e:
        #         print(e)
        #         return Response(status=status.HTTP_204_NO_CONTENT)

        # else:
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):

    def post(self, request: Request):
        """
        Verify the Email end Check the code that will be sand if from ``Send Verify Email``.
        if you try to sign up before send the code to here it will make error ``with status code 401``.

        Args:
        - code(intager): a given code from email.
        ``- example: {'code': 0000}``.

        Returns:
        - is_valid:Boolen.
        - in_Success:
            - status: 200 .
        - in_Fail:
            - status: 401 when the given code not match with the sending code.
            - status: 400 when data isn't correct or somthing go to by wrong.
        """
        email_code = 0
        code = ''
        # and request.session.has_key('is_verify'): -> لما نكمل بشكل كامل لازم يكون create user من هناء لما يكون False يعني مايقع شي
        if request.session.has_key('email_code') and request.session.has_key('is_verify'):
            email_code = request.session.get('email_code')
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get('code'):
            code = request.data.get('code')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if email_code == code:
            request.session['is_verify'] = True  # هنا

        if code:
            return Response({
                'is_valid': True
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'is_valid': False
            }, status=status.HTTP_200_OK)

#### End Email Method ######
