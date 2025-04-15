from rest_framework import serializers
from .models import CustomUser
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
            raise serializers.ValidationError({"Email": "A user with this email already exists."})
        
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
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'is_staff': self.user.is_staff,
            'is_superuser': self.user.is_superuser,
            'is_premium': self.user.is_premium,
            'profile_picture': self.user.profile_picture,
            'gender': self.user.gender,
            'date_of_birth': self.user.date_of_birth
        }
        return data