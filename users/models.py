from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from log_config import logger

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
            return self.username
    
    def assign_initial_group(self):
        try:
            group = Group.objects.get(name='TIMESHEETS LIMITED')
            self.groups.add(group)
            logger.debug(f"Assigned {self.username} to group 'TIMESHEETS LIMITED'.")
        except Group.DoesNotExist:
            logger.error("Group 'TIMESHEETS LIMITED' does not exist.")

        
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    bio = models.TextField(blank=True)
    resume = models.FileField(upload_to='cv/', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username

    
