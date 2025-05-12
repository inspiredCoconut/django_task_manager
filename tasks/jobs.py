import subprocess

from celery import shared_task
from .models import Task

@shared_task(bind=True)
def run_task(self, task_id):
    """
    Run a task by its ID.
    """
    task = Task.objects.get(id=task_id)
    task.status = 'running'
    task.save()
    try:
        # Example: run a long-running command
        proc = subprocess.Popen(['python3', '-m', "tasks.daemon"])  # Simulated long task
        task.pid = proc.pid
        task.save()

        proc.wait()  # Wait until the process finishes
        task.status = 'done'
        task.result = 'Completed successfully'
    except Exception as e:
        task.status = 'failed'
        task.result = str(e)
        return str(e)