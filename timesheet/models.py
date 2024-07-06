from django.db import models
from users.models import CustomUser

class Activity(models.Model):
    """
    This class creates db tables for the types of actvities
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
    def __str__(self):
        return self.name
    
class FundsSource(models.Model):
    """This class created db tables for the source of funds, which will be selectable from a 
    dropdown list when generating a timesheet
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"
    def __str__(self):
        return self.name
class Timesheet(models.Model):
    """
    This class created db tables for each timesheet, linked to activity model and FundsSource model by ForeinKey relations
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    funds_from = models.CharField(max_length=50)
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    description = models.TextField()
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Timesheet for {self.user.username} - Week of {self.week_start_date}"