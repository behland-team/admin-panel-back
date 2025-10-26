FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=admin_panel.settings.prod
ENV DJANGO_DEBUG=0
ENV DJANGO_ALLOWED_HOSTS="localhost,127.0.0.1,0.0.0.0,*"

WORKDIR /admin_panel

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "admin_panel.wsgi:application"]