from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=100,min_length=6,write_only=True)
    confirm_password = serializers.CharField(
            max_length=100,min_length=6,write_only=True)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']

    def validate(self,data):
        email = data.get('email','')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                 {'email':('Email is already exists')})
        return super().validate(data)

    def create(self,validated_data):
        if validated_data['password']!=validated_data['confirm_password']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


"""class ChangePasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['password']
"""
