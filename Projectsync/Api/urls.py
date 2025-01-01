
from django.urls import path
from Authentication_app.views import *
from Admin_app.views import *
from User_app.views import *

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    
    path('signin/',MyTokenobtainedPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/',SignUp,name='signup'),
    
    #* ............... Admin apis ...................
    
    path('getusers/',GetUsers,name='getusers'),
    path('userblockunblock/',UserBlockUnblock,name='userblockunblock'),
    path('userpermission/',UserPermission,name='userpermission'),
    path('getprojects/',GetProjects,name='getprojects'),
    path('bulk_delete/',Bulk_Delete,name='bulk_delete'),
    
    #* ................ User apis ...................
    
    path('get_user/',Get_User,name='get_user'),
    path('createproject/',Create_Project,name='createproject'),
    path('getemployee/',Get_Employees,name='getemployee'),
    path('deleteproject/',DeleteProject,name='deleteproject'),
    path('projectstatus/',ProjectstatusManagement,name='projectstatus'),
    path('editproject/',EditProject,name='editproject'),
    path('getprojectteam/',GetProjectTeam,name='getprojectteam'),
    path('removeteammember/',RemoveTeamMember,name='removeteammember'),
    path('addnewmember/',AddNewMemeber,name='addnewmember'),
    path('addnewtask/',AddNewTask,name='addnewtask'),
    path('Get_Tasks/',Get_Tasks,name='get_tasks'),
    path('delete_task/',Delete_Task,name='delete_task'),
    path('update_task/',Update_Task,name='update_task'),
    
    
]
