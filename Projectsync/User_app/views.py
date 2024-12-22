from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Authentication_app.models import CustomUser
from Admin_app.serializer import UsersSerializer
from .serializer import *


#* ................... Get User Details and related projects  ...................
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_User(request):
    
    id = request.GET.get('id')
    if not id :
        return Response("User id required",status=status.HTTP_400_BAD_REQUEST)  
    try:
        #* getting User dippend on the user
        user = CustomUser.objects.get(id=id)
        serializer = UsersSerializer(user)
        #* getting project dippend on the user 
        
        projects = ProjectTeam.objects.filter(employee=id).select_related('project')
        
        #* Extract the projects only 
        project =[pro.project for pro in projects]
        project_serializer = ProjectsSerializer(project,many=True)
        
        
        data = {
            'user_data':serializer.data,
            'project_data':project_serializer.data,
        }
        
        return Response(data,status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)


#* ................... Get Employees ...................

@api_view(['GET'])
@permission_classes([IsAuthenticated])  
def Get_Employees(request):

    try:
        employees = CustomUser.objects.filter(is_staff = False,is_active = True)
        serializer = EmployeesSerializer(employees,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)    
    
    
#* ................... Create Project ...................
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def Create_Project(request):
    
    user = request.user
    data = request.data.copy()
    
    if  user.is_anonymous:
        return Response("User required",status=status.HTTP_400_BAD_REQUEST)
    elif not data:
        return Response("Project data required",status=status.HTTP_400_BAD_REQUEST)
    
    # userdata = CustomUser.objects.get(id=user.id)
    # data['created_by'] = userdata.id
    team = list(data.get('team[]'))
    print(data,'data')
    if str(user.id) not in team:
        team.append(user.id)
    try:
        
        #* project created here 
        
        serializer = ProjectsSerializer(data=data,context={'request': request})
        if serializer.is_valid():
            projectdata = serializer.save()  #* This returns the model instance, not a dict
            
            #* After creating project we have to store project team in to project team table  
            team_member_list = []   
            
            for member in team:
                employee = CustomUser.objects.get(id=member)
              
                team_member = ProjectTeam(project=projectdata,employee=employee)
                team_member_list.append(team_member)
                
            #* Storing team members in bulk 
            if team_member_list:
               ProjectTeam.objects.bulk_create(team_member_list)
            
            return Response({'Project and team created successfully'},status=status.HTTP_201_CREATED)
           
        else:
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        
        if 'projectdata' in locals():
           projectdata.delete()
        
        return Response({str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
#* ................... Delete Project ...................
@permission_classes([IsAuthenticated])
@api_view(['DELETE']) 
def DeleteProject(request):
    
    id = request.data.get('id')
    print(id,'data')
    if not id:
        return Response("Project id required",status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Projects.objects.get(id=id)
        project.delete()
        return Response("Project deleted successfully",status=status.HTTP_200_OK)
    except Projects.DoesNotExist:
        return Response("Project not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)


#* ................... Project Status Management ...................

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def  ProjectstatusManagement(request):
    
    id = request.data
    
    if not id :
        return Response("Project id required",status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Projects.objects.get(id=id)
        if project.status == 'planned':
            project.status = 'active'
        elif project.status == 'active':
            project.status = 'Completed'
        project.save()
        return Response("Project status updated successfully",status=status.HTTP_200_OK)
        
    except Projects.DoesNotExist:
        return Response("Project not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
        