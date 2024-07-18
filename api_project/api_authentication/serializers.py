from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'patronymic', 'phone_number', 'role')
        
        
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                  'patronymic', 'phone_number')
        
    def update(self, instance, validated_data):
        errors = {}
        
        fields = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'phone_number')
        for field in fields:
            if field not in validated_data:
                errors[field] = 'The wrong format or was not sent.'

        if errors:
            raise serializers.ValidationError(errors)
        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        user = self.context['request'].user
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_new_password = attrs.get('confirm_new_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Invalid password.'})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({'confirm_new_password': 'The new passwords don\'t match.'})

        return attrs

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        else:
            return user
    