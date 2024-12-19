from rest_framework.serializers import ModelSerializer
from Authentication_app.models import CustomUser


class UsersSerializer(ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id','email','username','is_active','date_joined','is_permission']
        