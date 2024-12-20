from django.db import models
from Authentication_app.models import CustomUser
from django.utils import timezone
# Create your models here.

class Projects(models.Model):
    Choice =[('planned','planned'),('active','active'),('Completed','Completed')]
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    created_at = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_by')
    status = models.CharField(choices=Choice,max_length=100,null=False,default='planned')

    class Meta:
        ordering = ['-id']

class ProjectTeam(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='project')
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employee')