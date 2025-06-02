from django.shortcuts import render
from django.views import View

import psutil

class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Get system information
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        disk_info = psutil.disk_usage('/')
        disk_usage = disk_info.percent
        total_disk_space = round(disk_info.total / (1024 ** 3), 2)  # Total disk space in GB
        free_disk_space = round(disk_info.free / (1024 ** 3), 2)  # Total disk space in GB
        # Pass the information to the template
        context = {
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
            'total_disk_space': total_disk_space,
            'free_disk_space': free_disk_space,
        }
        return render(request, 'home.html', context)