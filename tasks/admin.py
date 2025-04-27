from django.contrib import admin
from .models import Progress, Task, Configuration, SystemPrompt

# Register your models here.

from django.contrib import admin
from .models import Progress

admin.site.register(Progress)
admin.site.register(Task)
admin.site.register(Configuration)
admin.site.register(SystemPrompt)

