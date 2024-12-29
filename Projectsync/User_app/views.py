from django.shortcuts import render
from rest_framework.decorators import api_view,APIView,permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from Authentication_app.models import CustomUser
from Admin_app.serializer import UsersSerializer
from .serializer import *
from django.db.models import Q

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
 
    team = list(data.get('team[]'))
    
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
        
#* ......................... Edit project details .......................
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def EditProject(request):
    
    data = request.data
    if not data:
        return Response("Project data required",status=status.HTTP_400_BAD_REQUEST)
    try:
        project = Projects.objects.get(id=data['id'])
        serializer = ProjectsSerializer(project,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Project updated successfully",status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Projects.DoesNotExist:
        return Response("Project not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
    
#* .................... Get project related users (project team) ..................
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProjectTeam(request):
    
    id = request.GET.get('id')
    if not id:
        return Response('Project id required',status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        
        users = ProjectTeam.objects.filter(project=id).prefetch_related('employee')
      
        serializer = ProjectTeamSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    except ProjectTeam.DoesNotExist:
        return Response("Project id  not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#*........................ Remove Project Team member ...................

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def RemoveTeamMember(reques):
    
    id = reques.data
    if not id :
        return Response("Project id required",status=status.HTTP_400_BAD_REQUEST)
    
    try:
        
        ProjectTeam.objects.filter(id=id).delete()
        return Response("Team Member Removed successfully",status=status.HTTP_200_OK)

    except ProjectTeam.DoesNotExist:
        return Response("Project team membet  not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#* ........................... Add New Team Member ........................

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AddNewMemeber(request):
    
    data = request.data
    if not data:
        return Response("data required",status=status.HTTP_400_BAD_REQUEST)

    members = data.get('members')
    project_id = data.get('project_id')
  
    
    try:
        
        project = Projects.objects.get(id=project_id)
        
        Team_list=[]
        for member in members:
            
            employee = CustomUser.objects.get(id = member['value'])
            team = ProjectTeam(project=project,employee=employee)
            Team_list.append(team)
            
        if Team_list:
            ProjectTeam.objects.bulk_create(Team_list)
            
            return Response("Team Members updated successfully",status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response("User not find",status=status.HTTP_400_BAD_REQUEST)
    except ProjectTeam.DoesNotExist:
        return Response("Project not find",status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    
#* .......................... Add New Task .........................
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def AddNewTask(request):
    
    data = request.data

    if not data:
        return Response("data required",status=status.HTTP_400_BAD_REQUEST)
    try:
        
        user = request.user
        project_id = data.get('project_id')
        assign_to = data.get('assignedTo')
        
        if  user.is_anonymous:
            return Response("User required",status=status.HTTP_400_BAD_REQUEST)       
        elif not project_id or not assign_to:
            return Response("Project id and assign to required",status=status.HTTP_400_BAD_REQUEST) 
        else:
            
            try:
                
               project = Projects.objects.get(id=project_id)
            except Projects.DoesNotExist:
                return Response('project not found',status=status.HTTP_404_NOT_FOUND)
            
            try:
                created_by = CustomUser.objects.get(Q(id=user.id) & (Q(is_permission=True) | Q (is_staff=True))) #* here checking user have permission or user is admin 

            except CustomUser.DoesNotExist:
                 return Response('Created_by or assign to not found',status=status.HTTP_400_BAD_REQUEST)
            try:
                
               assign = CustomUser.objects.get(id=assign_to)
            except CustomUser.DoesNotExist:
                 return Response(' assign to not found',status=status.HTTP_400_BAD_REQUEST)
            
            task ={
                'title' : data.get('title'),
                'description' : data.get('description'),
                'priority' : data.get('priority'),
                'assigned_to' : assign.id,
                'Project' : project.id
                
            }
            
            serializer = TaskSerializer(data=task,context={'request': request,'assigned_to':assign,'project':project})
            if serializer.is_valid():
                serializer.save()
                return Response("Task Added successfully",status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)

#*............................ Get Tasks ........................

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Get_Tasks(request):
    
    id = request.GET.get('id')
 
    if not id :
         return Response("Project id required",status=status.HTTP_400_BAD_REQUEST)
   
    try:
        tasks = ProjectTask.objects.filter(Project=id)
        serializer = TaskSerializer(tasks,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    except ProjectTask.DoesNotExist:
        return Response("Task not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    

#* ............................ Delete Task ........................

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def Delete_Task(request):
    
    id = request.data.get('id')
    if not id:
        return Response ('Task id required',status=status.HTTP_400_BAD_REQUEST)
    try:
        
        task = ProjectTask.objects.get(id=id)
        task.delete()
        return Response("Task deleted successfully",status=status.HTTP_200_OK)
    except ProjectTask.DoesNotExist:
        return Response("Task not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#* ............................ Update Task ........................

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def Update_Task(request):
    
    data = request.data
    id = request.data.get('task_id')
    assigned_to = request.data.get('assignedTo')
   
    if not data:
        return Response("data required",status=status.HTTP_400_BAD_REQUEST)
    elif not id:
        return Response("Task id required",status=status.HTTP_400_BAD_REQUEST)
    try:
       if assigned_to:
           assigned = CustomUser.objects.get(id=assigned_to)
           
       task = ProjectTask.objects.get(id=id)
       serializer = TaskSerializer(task,data=data,context={'assigned_to':assigned},partial=True)
       if serializer.is_valid():
           serializer.save()
           return Response("Task updated successfully",status=status.HTTP_200_OK)
       else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)       
    except ProjectTask.DoesNotExist:
        return Response("Task not found",status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({str(e)},status=status.HTTP_400_BAD_REQUEST)
    