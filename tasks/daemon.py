import sys
from core.utils import get_model_by_name

async def main(task_id):
    # This is a main function example for a daemon task.
    # You can implement your task logic here.
    print("Daemon task is running...")
       
    # Simulate some work being done
    while True:
        print("Working... with task ID:", task_id)
        await asyncio.sleep(5)
    # Update the last_run field in the database
    
    
if __name__ == "__main__":
    import asyncio
    task_id = int(sys.argv[1])
    asyncio.run(main(task_id=task_id))
    # This is where you would typically update the last_run field in the database
    # using an ORM like Django's ORM
    # model = get_model_by_name('tasks', 'Task')
    # Assuming you have a task instance to update
    # Replace with the actual task instance you want to update
    # task = model.objects.get(id=1)  # Replace with the actual task ID
    # task.last_run = time.now()
    #task.save()