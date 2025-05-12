import os
import signal

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse

from .models import Task
from .jobs import run_task

# Create your views here.
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        return Task.objects.all()
    
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
    def get_object(self):
        return Task.objects.get(id=self.kwargs['pk'])
    
class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'active']
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'create'
        return context
      
    def form_valid(self, form):
        return super().form_valid(form)
    
class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'active']
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'update'
        return context
      
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')
    
    def get_object(self):
        return Task.objects.get(id=self.kwargs['pk'])
    
def start_task(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    try:
        task = Task.objects.get(id=pk)
        # Here you would start the task using Celery or any other method
        # For example:
        # task.start()
        
        # Start the task asynchronously
        # asyncio.run(run_task(task.id))  # This is just an example, adjust as needed
        # If using Celery, you would typically call:
        
        run_task(task.id)
        
        return JsonResponse({'status': 'Task started', 'task_id': task.id})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    
def stop_task(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    try:
        task = Task.objects.get(id=pk)
        if task.pid:
            # Stop the task using its PID
            try:
                os.kill(task.pid, signal.SIGTERM)  # Send SIGTERM to the process
                task.status = 'stopped'
                task.save()
            except OSError as e:
                print("Error stopping task:", e)
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Task not running'}, status=400)
        
        return JsonResponse({'status': 'Task stopped', 'task_id': task.id})
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)