from django.urls import path

from .views import *

urlpatterns = [
    path('registration', Registration.as_view(), name='registration'),
    path('key-verification', KeyVerification.as_view(), name='key_verification'),
    path('successful_registration', SuccessfulRegistration.as_view(), name='successful_registration'),
    path('authentication', LoginUser.as_view(), name='login')
]
