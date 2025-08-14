python3 manage.py makemigrations --noinput

python manage.py migrate --noinput
python3 manage.py collectstatic --noinput

echo "Creando superusuario..."
python manage.py createsuperuser --noinput || echo "Superusuario ya existe, continuando..."

# Production
gunicorn django_task_manager.asgi:application --bind 0.0.0.0:7000 --workers 5 --threads 21 --worker-class uvicorn.workers.UvicornWorker --timeout 120 --log-level debug --access-logfile - --error-logfile -