from django.urls import path
from .views import UserRegistrationView, CustomTokenObtainPairView, GetAllUserView, GetUserByIdView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/', GetAllUserView.as_view(), name='get_all_user'),
    path('user/<int:pk>', GetUserByIdView.as_view(), name='get_user_by_id')
]