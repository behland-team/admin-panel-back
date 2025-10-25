
# Stage 1: Base build stage
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 
ENV DJANGO_SETTINGS_MODULE=admin_panel.settings.prod

WORKDIR /admin_panel

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the app directory
RUN mkdir /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--settings=admin_panel.settings.prod"]