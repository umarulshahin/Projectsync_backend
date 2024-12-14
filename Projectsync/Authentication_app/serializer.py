from rest_framework import serializers
from .models import *
import re

class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
    
    def validate(self, data):
        
        if not data:
            raise serializers.ValidationError('User data required.')
        
        username_pattern = r'^[A-Za-z][A-Za-z0-9_]{2,}$'
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'
   
            
        if not re.match(username_pattern,data['username']):
            raise serializers.ValidationError({"username":"Username must start with a letter and be at least 3 characters long, containing only letters, numbers, or underscores."})
        
        elif not re.match(email_pattern,data['email']):
            raise serializers.ValidationError({"email":"Enter a valid email address."})
        
        elif not re.match(password_pattern,data['password']):
            raise serializers.ValidationError({"password":"Password must be at least 8 characters long, contain at least one uppercase letter, one digit, and one special character."})
        
        elif CustomUser.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError({'email':'Email already exist.'})
        
        return data
    
    def create(self, validated_data):
        
        user = CustomUser.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        user.save()
        return validated_data