from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView


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

class GetUserByIdView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get profile information of the authenticated user",
        responses={
            200: openapi.Response(description="User profile retrieved successfully"),
            401: openapi.Response(description="Unauthorized"),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve the profile of the authenticated user.
        """
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)