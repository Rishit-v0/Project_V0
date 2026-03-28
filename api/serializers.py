from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Product

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):

        # Remove password2 from validated_data
        validated_data.pop('password2')

        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'created_at']
        read_only_fields = ['id', 'created_at']



class ProductSerializer(serializers.ModelSerializer):
    created_by = UserProfileSerializer(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']