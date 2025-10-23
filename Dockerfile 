FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

# اگر requirements.txt داخل admin_panel است، همین مسیر را نگه‌دار
COPY admin_panel/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt \
    && pip install --no-cache-dir gunicorn whitenoise

# کد برنامه
COPY admin_panel /app

# اسکریپت شروع (Prod)
COPY deploy/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000
# Dev: runserver   | Prod: از docker-compose تنظیم می‌کنیم
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
