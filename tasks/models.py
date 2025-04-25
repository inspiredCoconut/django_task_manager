from django.db import models
from .daemon import main as daemon_main_function

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255)
    pid = models.IntegerField()
    description = models.TextField()
    cron_schedule = models.CharField(max_length=255)
    cron_job = models.CharField(max_length=255)
    cron_job_id = models.CharField(max_length=255)
    cron_job_name = models.CharField(max_length=255)
    cron_job_description = models.TextField()
    cron_job_args = models.TextField()
    cron_job_kwargs = models.TextField()
    cron_job_user = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_run = models.DateTimeField(null=True, blank=True)
    
    daemon_main_function = staticmethod(daemon_main_function)

    def __str__(self):
        return self.name