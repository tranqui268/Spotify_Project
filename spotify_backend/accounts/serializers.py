from rest_framework import serializers, exceptions
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True, required = True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'profile_picture', 'gender', 'date_of_birth']
        extra_kwargs = {
            'username': {'help_text': 'Unique username for the user'},
            'email': {'help_text': 'Unique email address for the user'},
            'profile_picture': {'required': False, 'help_text': 'Profile picture (optional)'},
            'gender': {'required': False, 'help_text': 'Gender: M (Male), F (Female), O (Other)'},
            'date_of_birth': {'required': False, 'help_text': 'Date of birth in YYYY-MM-DD format'},
        }

    def validate(self, data):
        # Check password
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password do not match"})
        
        # Check user existed
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "A user with this username already exists."})
        
        # Check email existed 
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            profile_picture=validated_data.get('profile_picture', None),
            gender=validated_data.get('gender', None),
            date_of_birth=validated_data.get('date_of_birth', None),
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
            data['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'is_staff': self.user.is_staff,
                'is_superuser': self.user.is_superuser,
                'is_premium': getattr(self.user, 'is_premium', False),
                'profile_picture': getattr(self.user, 'profile_picture', None),
                'gender': getattr(self.user, 'gender', None),
                'date_of_birth': getattr(self.user, 'date_of_birth', None)
            }
            return data
        except exceptions.AuthenticationFailed as e:
            # Tùy chỉnh response lỗi theo định dạng yêu cầu
            error_response = {
                "status_code": 401,  # Unauthorized
                "message": _("Login failed"),
                "errors": {
                    "credentials": [
                        _("The username or password provided is incorrect. Please check your credentials and try again.")
                    ]
                }
            }
            raise exceptions.AuthenticationFailed(error_response)
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'is_superuser',
            'is_premium',
            'profile_picture',
            'gender',
            'date_of_birth',
        ]
        read_only_fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.profile_picture:
            representation['profile_picture'] = instance.profile_picture.url
        return representation