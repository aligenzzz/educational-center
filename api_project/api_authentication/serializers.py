from rest_framework import serializers, status
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.urls import reverse
import requests
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                  'patronymic', 'phone_number', 'role')
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 
                  'patronymic', 'phone_number')
        
    def update(self, instance, validated_data):        
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)
    refresh = serializers.CharField(required=True)
    
    def validate(self, data):
        user = self.context['request'].user
        old_password = data['old_password']
        new_password = data['new_password']
        confirm_new_password = data['confirm_new_password']

        if not user.check_password(old_password):
            raise serializers.ValidationError({'old_password': 'Invalid password.'})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({'confirm_new_password': 'The new passwords don\'t match.'})

        return data
    
    def save(self):
        request = self.context['request']
        user = request.user
        
        refresh_token = self.validated_data['refresh']
        access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        
        try:
            new_password = self.validated_data['new_password']
            user.set_password(new_password)            
            
            blacklist_url = request.build_absolute_uri(reverse('token-blacklist'))       
            blacklist_data = {'refresh': refresh_token}
            blacklist_headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(blacklist_url, data=blacklist_data, headers=blacklist_headers)
            
            if response.status_code == status.HTTP_200_OK:
                # save + reset session inside api
                user.save()
            else:
                raise Exception('Failed to blacklist token')
        except Exception as e:
            raise Exception(str(e))


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    
    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        return user
        
    def save(self):
        request = self.context['request']    
        username = request.data['username']
        password = request.data['password']
        user = self.validated_data 
        
        if user:
            token_url = request.build_absolute_uri(reverse('token-obtain-pair'))
            token_data = {
                'username': username,
                'password': password,
            }
            response = requests.post(token_url, data=token_data)
            
            if response.status_code == status.HTTP_200_OK:
                # authorization inside api
                login(request, user)
                
                return response.json()
            else:
                raise Exception('Failed to obtain tokens')
        else:
            raise Exception('Invalid credentials')
        

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)
    
    def save(self):
        request = self.context['request']
        refresh_token = request.data['refresh']
        access_token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        
        try:
            blacklist_url = request.build_absolute_uri(reverse('token-blacklist'))       
            blacklist_data = {'refresh': refresh_token}
            blacklist_headers = {'Authorization': f'Bearer {access_token}'}
            response = requests.post(blacklist_url, data=blacklist_data, headers=blacklist_headers)
            
            if response.status_code == status.HTTP_200_OK:
                # logout inside api
                logout(request)
            else:
                raise Exception('Failed to blacklist token')
        except Exception as e:
            raise Exception(str(e))
    