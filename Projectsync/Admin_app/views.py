from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Authentication_app.models import CustomUser
from . serializer import *

#* ................... Get All Users For Admin...................
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUsers(request):
    user = CustomUser.objects.filter(is_superuser = False)
    response = UsersSerializer(user, many = True)
    
    return Response (response.data, status=status.HTTP_200_OK)


#* ................... User Block/Unblock ...................

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UserBlockUnblock(request):
    
    id = request.data
    
    if not id :
        return Response("User id required",status=status.HTTP_400_BAD_REQUEST)
    try:
        user = CustomUser.objects.get(id=id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return Response({"message":"User status updated"},status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
    
#* ................... User Permission Management...................
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UserPermission(request):
    
    id = request.data
    if not id :
        return Response("User id required",status=status.HTTP_400_BAD_REQUEST)
    try:
       User = CustomUser.objects.get(id=id)
       if User.is_permission:
           User.is_permission = False
       else:
           User.is_permission = True
       User.save()
       return Response({"message":"User permission updated"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
    