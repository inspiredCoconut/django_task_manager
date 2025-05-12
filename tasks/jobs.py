from celery import shared_task
from .models import Task

@shared_task
def run_task(task_id):
    """
    Run a task by its ID.
    """
    try:
        task = Task.objects.get(id=task_id)
        task.status = 'running'
        task.save()
        
        # Simulate some work being done
        import time
        time.sleep(5)  # Replace with actual task logic
        print(f"Task {task.name} is running with PID {task.pid}")
        
        task.status = 'done'
        task.save()
    except Task.DoesNotExist:
        return f"Task with ID {task_id} does not exist."
    except Exception as e:
        task.status = 'failed'
        task.save()
        return str(e)