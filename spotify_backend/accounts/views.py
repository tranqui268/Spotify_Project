from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    page_size = 10  # Số lượng user mỗi trang
    page_size_query_param = 'page_size'  # Cho phép người dùng tùy chỉnh số lượng trên mỗi trang
    max_page_size = 100  # Giới hạn tối đa số lượng user trên mỗi trang


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema( # type: ignore
        operation_description="Register a new user",
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "message": "User registered successfully",
                        "data": {
                            "id": 1,
                            "username": "testuser",
                            "email": "testuser@example.com",
                            "is_premium": False
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Registration failed",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "Registration failed",
                        "errors": {
                            "username": ["A user with this username already exists."]
                        }
                    }
                }
            )
        }
    )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "status_code": status.HTTP_201_CREATED,
                    "message": "User registered successfully",
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "is_premium": user.is_premium
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "Registration failed",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class GetAllUserView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = UserPagination

class GetUserByIdView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

