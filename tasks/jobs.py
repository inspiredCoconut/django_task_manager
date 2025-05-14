import subprocess
import threading

from celery import shared_task
from .models import Task
import psutil

def stream_output(stream, prefix):
    for line in iter(stream.readline, b''):
        print(f"[{prefix}] {line.decode().rstrip()}")

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
        if task.pid != 0:
            try:
                existing_process = psutil.Process(task.pid)
                if existing_process.is_running() and task.status == 'running':
                    print(f"Process with PID {task.pid} is already running.")
                    return f"Task with PID {task.pid} is already running."
            except psutil.NoSuchProcess:
                print(f"Process with PID {task.pid} does not exist.")
                pass  # Process does not exist, continue
        proc = subprocess.Popen(['python3', '-m', "tasks.daemon", str(task_id)], 
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Started process with PID: {proc.pid}")
        # Simulated long task
        task.pid = proc.pid
        task.save()
        
        threading.Thread(target=stream_output, args=(proc.stdout, 'OUT')).start()
        threading.Thread(target=stream_output, args=(proc.stderr, 'ERR')).start()
        
        #proc.wait()  # Wait until the process finishes
        #task.status = 'done'
        #task.result = 'Completed successfully'
    except Exception as e:
        task.status = 'failed, finished'
        task.pid = 0
        task.result = str(e)
        task.save()
        return str(e)