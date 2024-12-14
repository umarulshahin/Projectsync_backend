from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

#* ................... User Register ....................

@api_view(['POST'])
def SignUp(request):
    
    data = request.data
    if not data:
        return Response("User data required",status=status.HTTP_400_BAD_REQUEST) 
    serializer = SignupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'success':serializer.data},status=status.HTTP_201_CREATED)
    else: 
       return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
   

#* ................. Login and JWT token generating....................
   
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token["role"]=user.is_superuser
        
        return token

class MyTokenobtainedPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer
    
    