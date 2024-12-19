from django.db import models
from Authentication_app.models import CustomUser
from django.utils import timezone
# Create your models here.

class Projects(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    created_at = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_by')

    class Meta:
        ordering = ['-id']