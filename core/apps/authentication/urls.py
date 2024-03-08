from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.CustomAuthToken.as_view()),
    path('sginup/', views.ReigsterView.as_view()),
    path('check-email/', views.ChechEmailValidateView.as_view(),
         name='check_email_velidate'),
    path('verify-email/', views. VerifyEmailView.as_view(), name='verify_email'),
    path('send-verify-email/', views.SendVerifyEmailView.as_view(),
         name='send_verify_email'),
    # path('logout/',)
]
