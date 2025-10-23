#!/usr/bin/env bash
set -e

echo "Migrate..."
python manage.py migrate --noinput

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Start gunicorn..."
exec gunicorn admin_panel.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
