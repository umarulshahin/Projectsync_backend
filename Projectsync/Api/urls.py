
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
    
    #* ................ User apis ...................
    
    path('get_user/',Get_User,name='get_user'),
    path('createproject/',Create_Project,name='createproject'),
    path('getemployee/',Get_Employees,name='getemployee'),
    path('deleteproject/',DeleteProject,name='deleteproject'),
    path('projectstatus/',ProjectstatusManagement,name='projectstatus')
    
    
]
