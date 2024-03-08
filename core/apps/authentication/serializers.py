from django.conf import settings
from django.template import loader
from django.core.mail import send_mail, EmailMessage
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from ..models import User
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer


class UserAuthSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(use_url=True)
    password = serializers.CharField(write_only=True)
    user_auth = serializers.SerializerMethodField(read_only=True)

    def get_user_auth(self, obj) -> dict:
        # request = self.context.get('request' or None)
        # serializer = AuthTokenSerializer(data=request.data,
        #                                  context=self.context)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=obj)
        return {
            'token': token.key,
            'user_id': obj.pk,
            'email': obj.email
        }

    class Meta:
        model = User
        fields = ['id', 'email', 'phone_number',
                  'username', 'password',  'name', 'image', 'user_auth']

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instence = self.Meta.model(**validated_data)
        if instence is not None:

            instence.set_password(password)
        instence.save()
        return instence


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email) -> any:
        return super().validate(email)

    def send_verify_email(self, code) -> dict:
        """
        To send Code verfcation to the user and add the code to session.
        Is very requeird bafore the signub  

        Args:
            ``code`` (int): random intager from ``generit_random_code()`` method
        Returns:
            dict: {
                'is_send': Boolen,
                # 'code': Intager -> not allowd
            }
        """
        try:
            print(code)
            email = self.validated_data.get('email') or self.email
            template = loader.get_template('code_design.html').render({
                'code': code
            })
            send = EmailMessage(
                "Test OTP Form Django APIs Verify", template,  settings.EMAIL_HOST_USER, [email, ])
            # send_mail(
            #     f" Welcome Your Code : {code}.", settings.EMAIL_HOST_USER, [email, ], fail_silently=False)
            send.content_subtype = 'html'
            send.send()
            # {
            #     "email": "ahmed.128hemzh@gmail.com"
            # }
            # refresh
            return {
                'is_send': True,
                'code': code
            }
        except Exception as e:
            print(e)
            return {
                'is_send': False,
                'code': None
            }


class ChechEmailValidateSerilzers(serializers.Serializer):
    """
    Serializer for Chack if The Email is used by another user or not

    Args:
        email (``Email``): take email from request
    """
    email = serializers.EmailField()
