from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Progress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} – Level {self.current_level}"

