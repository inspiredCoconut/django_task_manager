from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render

from .models import Task

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
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'tasks/task_form.html'
    fields = ['name', 'description', 'active']
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        return super().form_valid(form)
    
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')
    
    def get_object(self):
        return Task.objects.get(id=self.kwargs['pk'])