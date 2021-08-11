# from django.contrib.auth.models import User
from .models import CustomUser
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username','first_name','last_name','password','is_active','last_login','is_superuser']

    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data["password"])
    #     return user

class ReadOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','password','is_active','last_login','is_superuser']

class WriteOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','password','is_active']
