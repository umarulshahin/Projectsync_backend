from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Authentication_app.models import CustomUser
from . serializer import *
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUsers(request):
    user = CustomUser.objects.filter(is_superuser = False)
    response = UsersSerializer(user, many = True)
    
    return Response (response.data, status=status.HTTP_200_OK)