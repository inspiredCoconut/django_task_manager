import asyncio

from django.apps import AppConfig

from core.utils import get_model_by_name

class ManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'manager'
    
    
    def ready(self):
        model = get_model_by_name('tasks', 'Task')
        # Check if there are any active tasks in the database
        if model.objects.filter(active=True).exists():
            # This is where you would typically start the daemon tasks
            # For example, you could use a task queue or a separate thread
            # to run the daemon tasks in the background.
            # Here, we are just simulating the daemon task with asyncio
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.start_daemon_tasks())
            
    async def start_daemon_tasks(self):
        model = get_model_by_name('tasks', 'Task')
        # Get all active tasks from database
        active_tasks = model.objects.filter(active=True)
        for task in active_tasks:
            # Here you would start the daemon task
            # For example, you could use asyncio.create_task() to run the task
            # in the background.
            print(f"Starting daemon task: {task.name}")
            await task.daemon_main_function()