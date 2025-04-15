import random
from rest_framework import serializers
from .models import EmailLoginCode
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta

class SendEmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email chưa được đăng ký.")
        return value

    def create(self, validated_data):
        code = f"{random.randint(100000, 999999)}"
        email = validated_data['email']

        # Lưu mã vào DB
        EmailLoginCode.objects.create(email=email, code=code)

        # Gửi email (tùy cấu hình EMAIL_BACKEND)
        send_mail(
            subject="Mã đăng nhập của bạn",
            message=f"Mã xác nhận đăng nhập của bạn là: {code}",
            from_email="noreply@yourdomain.com",
            recipient_list=[email],
        )
        return {"message": "Mã xác thực đã được gửi đến email."}
    
class VerifyEmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data['email']
        code = data['code']

        try:
            record = EmailLoginCode.objects.filter(email=email, code=code, is_used=False).latest('created_at')
        except EmailLoginCode.DoesNotExist:
            raise serializers.ValidationError("Mã xác nhận không hợp lệ.")

        # Kiểm tra thời gian hết hạn (5 phút)
        if timezone.now() - record.created_at > timedelta(minutes=3):
            raise serializers.ValidationError("Mã đã hết hạn.")

        # Đánh dấu là đã dùng
        record.is_used = True
        record.save()

        return data

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.get(email=validated_data['email'])

        # Tạo JWT token
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_premium': user.is_premium
            }
        }
