from django.db import models
#from .daemon import main as daemon_main_function

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    pid = models.IntegerField(default=0)
    description = models.TextField(default='', blank=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., pending, running, done, failed
    active = models.BooleanField(default=True)
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_run = models.DateTimeField(null=True, blank=True)
    
#    daemon_main_function = staticmethod(daemon_main_function)

    def __str__(self):
        return self.name