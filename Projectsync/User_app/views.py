from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Authentication_app.models import CustomUser
from Admin_app.serializer import UsersSerializer

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
