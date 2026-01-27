from django.db import models
from django.contrib.auth.models import User
from issues.models import Issue

# Create your models here.


class AdminActivity(models.Model):
    admin = models.ForeignKey(
        User, on_delete=models.CASCADE, limit_choices_to={"is_staff": True}
    )
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.action} on {self.issue.title}"
