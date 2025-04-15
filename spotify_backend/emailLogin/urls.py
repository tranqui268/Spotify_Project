# urls.py
from django.urls import path
from .views import RequestEmailLoginCodeView, VerifyEmailLoginCodeView

urlpatterns = [
    path('login/email/', RequestEmailLoginCodeView.as_view(), name='request_email_code'),
    path('login/email/verify/', VerifyEmailLoginCodeView.as_view(), name='verify_email_code'),
]
