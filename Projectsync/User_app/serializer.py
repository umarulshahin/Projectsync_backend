from rest_framework import serializers
from .models import *
import re
from datetime import date

   
class EmployeesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id','username']
        

class ProjectTeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProjectTeam
        fields = ['project','employee']
class ProjectsSerializer(serializers.ModelSerializer):
    
    team = ProjectTeamSerializer(read_only=True,many=True)
    created_by =EmployeesSerializer(read_only=True)
    class Meta:
        model = Projects
        fields = ['id','title','description','start_date','end_date','created_at','created_by','status','team']
        
    def validate(self, attrs):

        basic_pattern = r'^(?!\s*$).+'

        if not attrs['title'] or not attrs['description'] or not attrs['start_date'] or not attrs['end_date'] :
            raise serializers.ValidationError('All fields are required.')
        elif not re.match(basic_pattern,attrs['title']):
            raise serializers.ValidationError({"error":"Title must start with a letter and be at least 3 characters long, containing only letters, numbers, or underscores."})
        elif not re.match(basic_pattern,attrs['description']):
            raise serializers.ValidationError({"error":"Input cannot be empty or contain only spaces. It must include at least one letter, number, or symbol."})
        elif date.today() > attrs['start_date']:
            raise serializers.ValidationError({'error': "Start date cannot be in the past."})
        elif attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError({'error': "Start date cannot be greater than end date."})
        return attrs
    
    def create(self, validated_data):
        
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError("User is required")
            
            
        project = Projects.objects.create(
            title = validated_data['title'],
            description = validated_data['description'],
            start_date = validated_data['start_date'],
            end_date = validated_data['end_date'],
            created_by = request.user
        )
        project.save()
        return project
 
