from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Authentication_app.models import CustomUser
from . serializer import *
from User_app.serializer import *
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied,AuthenticationFailed
from User_app.models import *

#* ................... Admin Permission checking , Custom validation ...................

class AdminPermission(BasePermission):
    
    def has_permission(self, request, view):
        
        try:
            
            auth = JWTAuthentication()
            user,token = auth.authenticate(request)
            role = token.payload.get('role')

            if role :
                print(role,'role')
                return True
            else:
                raise PermissionDenied("You do not have permission to access this resource.")

        except AuthenticationFailed:
            raise PermissionDenied("Invalid token or token missing.")
        except Exception as e:
            raise PermissionDenied(f"Error occurred: {str(e)}")
 
#* ................... Get All Users For Admin...................
@api_view(['GET'])
@permission_classes([IsAuthenticated,AdminPermission])
def GetUsers(request):
    
    user = CustomUser.objects.filter(is_superuser = False)
    response = UsersSerializer(user, many = True)
    
    return Response (response.data, status=status.HTTP_200_OK)


#* ................... User Block/Unblock ...................

@api_view(['POST'])
@permission_classes([IsAuthenticated,AdminPermission])
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
@permission_classes([IsAuthenticated,AdminPermission])
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
    
    
#* ................... Get All Projects For Admin...................

@api_view(['GET'])
@permission_classes([IsAuthenticated,AdminPermission])  
def GetProjects(request):
    
    try:
        project = Projects.objects.all()
        serializer = ProjectsSerializer(project,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
        
