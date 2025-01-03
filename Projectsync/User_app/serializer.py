from rest_framework import serializers
from .models import *
import re
from datetime import date

   
class EmployeesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ['id','username']
        

class ProjectTeamSerializer(serializers.ModelSerializer):
    employee = EmployeesSerializer()
    class Meta:
        model = ProjectTeam
        fields = ['id','project','employee']
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
            raise serializers.ValidationError({"error":"Title must start with a letter and be at least 3 characters long, "})
        elif not re.match(basic_pattern,attrs['description']):
            raise serializers.ValidationError({"error":"description cannot be empty or contain only spaces. It must include at least one letter, number, or symbol."})
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
 

class TaskSerializer(serializers.ModelSerializer):
    
    created_by = EmployeesSerializer(read_only=True)
    assigned_to = EmployeesSerializer(read_only=True)
    Project = ProjectsSerializer(read_only=True)
    
    class Meta:
         
        model = ProjectTask
        fields = ['id','title','description','created_by','status','priority','assigned_to','created_at','Project']
        
    def validate(self,attrs):
        print(attrs,'attrs')
        base_pattern = r'^(?!\s*$).+'
        
        if not attrs['title'] or not attrs['description'] or not attrs['priority']: 
            raise serializers.ValidationError('all fields are required,')
        
        elif not re.match(base_pattern,attrs['title']):
            raise serializers.ValidationError({'error':'Title must start with a letter and be at least 3 characters long.'})
        elif not re.match(base_pattern,attrs['description']):
            raise serializers.ValidationError({'error':'description cannot be empty or contain only spaces. It must include at least one letter, number, or symbol.'})
         
        return attrs
    def create(self, validated_data):
          
        request = self.context.get('request')
        project = self.context.get('project')
        assigned_to = self.context.get('assigned_to')
        
        if not request or not request.user:
            raise serializers.ValidationError("User is required")
            
        task = ProjectTask.objects.create(created_by=request.user,
                                          title = validated_data['title'],
                                          description = validated_data['description'],
                                          priority = validated_data['priority'],
                                          assigned_to = assigned_to,
                                          Project =project)
        return task
    def update(self, instance, validated_data):
        
        assigned_to = self.context.get('assigned_to')
        if assigned_to:
            instance.assigned_to = assigned_to
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance