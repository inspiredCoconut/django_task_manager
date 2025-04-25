import time

from .models import Task

async def main():
    # This is a main function example for a daemon task.
    # You can implement your task logic here.
    print("Daemon task is running...")
    # Simulate some work being done
    await asyncio.sleep(5)
    print("Daemon task completed.")
    # Update the last_run field in the database
    
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    # This is where you would typically update the last_run field in the database
    # using an ORM like Django's ORM
    task = Task.objects.get(id=1)  # Replace with the actual task ID
    task.last_run = time.now()
    task.save()