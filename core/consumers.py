import json
import asyncio
import psutil
from channels.generic.websocket import AsyncWebsocketConsumer

class StatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        asyncio.create_task(self.send_stats())

    async def disconnect(self, close_code):
        self.running = False

    async def send_stats(self):
        while self.running:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            memory_usage = memory_info.percent
            disk_info = psutil.disk_usage('/')
            disk_usage = disk_info.percent
            total_disk_space = round(disk_info.total / (1024 ** 3), 2)  # Total disk space in GB
            free_disk_space = round(disk_info.free / (1024 ** 3), 2)  # Total disk space in GB
            stats = {
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'total_disk_space': total_disk_space,
                'free_disk_space': free_disk_space,
            }
            await self.send(text_data=json.dumps(stats))
            await asyncio.sleep(2)  # send every 2 seconds

class ProcessListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        asyncio.create_task(self.stream_processes())

    async def disconnect(self, close_code):
        self.running = False

    async def stream_processes(self):
        while self.running:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    info = proc.info
                    processes.append(info)
                except psutil.NoSuchProcess:
                    continue

            # Sort by CPU usage
            processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:10]

            await self.send(text_data=json.dumps(processes))
            await asyncio.sleep(3)  # 