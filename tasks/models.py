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

    class Meta:
        verbose_name_plural = "Progress"



class Task(models.Model):
    task_id = models.IntegerField(unique=True)
    task_text = models.TextField()
    task_prompt = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Task {self.task_id}: {self.task_text[:30]}..."


class Configuration(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.key

    @staticmethod
    def get_value(key: str, default=None) -> str:
        try:
            config = Configuration.objects.get(key=key)
            return config.value
        except Configuration.DoesNotExist:
            return default


class SystemPrompt(models.Model):
    name = models.CharField(max_length=255, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.name


