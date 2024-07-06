from django.db import models
from users.models import CustomUser

class MonthlyReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    activity = models.CharField(max_length=300)
    description = models.TextField()
    timeframe = models.CharField(max_length=300)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    # Add any additional fields you want in your report

    def __str__(self):
        return f"Monthly Report for {self.user.username} - {self.month}"
