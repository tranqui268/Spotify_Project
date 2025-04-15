# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendEmailCodeSerializer, VerifyEmailCodeSerializer

class RequestEmailLoginCodeView(APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        serializer = SendEmailCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Mã xác thực đã được gửi đến email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailLoginCodeView(APIView):
    permission_classes = []  # AllowAny

    def post(self, request):
        serializer = VerifyEmailCodeSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

