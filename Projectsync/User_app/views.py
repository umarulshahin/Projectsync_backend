from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Authentication_app.models import CustomUser
from Admin_app.serializer import UsersSerializer
from .serializer import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_User(request):
    
    id = request.GET.get('id')
    if not id :
        return Response("User id required",status=status.HTTP_400_BAD_REQUEST)  
    try:
        user = CustomUser.objects.get(id=id)
        serializer = UsersSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Create_Project(request):
    
    user = request.user
    data = request.data.copy()
    print(data,'data')
    
    if  user.is_anonymous:
        return Response("User required",status=status.HTTP_400_BAD_REQUEST)
    elif not data:
        return Response("Project data required",status=status.HTTP_400_BAD_REQUEST)
    
    data['created_by'] = user.id
    try:
        serializer = ProjectsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Project created successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        
       return Response({str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)