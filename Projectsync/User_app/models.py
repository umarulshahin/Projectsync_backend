from django.db import models
from Authentication_app.models import CustomUser
from django.utils import timezone
# Create your models here.

class Projects(models.Model):
    Choice =[('planned','Planned'),('active','Active'),('Completed','Completed')]
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    created_at = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_by')
    status = models.CharField(choices=Choice,max_length=100,null=False,default='Planned')

    class Meta:
        ordering = ['-id']

class ProjectTeam(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='project')
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employee')
    
    
class ProjectTask(models.Model):
    
    STATUS_CHOICES = [('to-do','To-Do'),('in-progress','In-Progress'),('done','Done')]
    PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),  
    ('high', 'High'),
]
    
    title = models.CharField(max_length=100)
    description = models.TextField(null=False,blank=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_user')
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,blank=False,null=False,default='to-do')
    priority = models.CharField(max_length=50,choices=PRIORITY_CHOICES,default='low',null=False,blank=False)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='assigned_to')
    created_at = models.DateField(default=timezone.now)
    Project = models.ForeignKey(Projects,on_delete=models.CASCADE,related_name='project_by')
    