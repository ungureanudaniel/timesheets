from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
    is_approved = models.BooleanField(default=False)

    def __str__(self):
            return self.username
    
    def assign_initial_group(self):
        # Assign user to the "TIMESHEETS INPUT" group upon creation
        group = Group.objects.get(name='TIMESHEETS LIMITED')
        self.groups.add(group)
        
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.user.username

    
