from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserRegistrationSerializer
from drf_yasg import openapi

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

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
