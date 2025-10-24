from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ───────────────────────────────── Base paths & .env
# settings.py در admin_panel/admin_panel/ است → BASE_DIR باید ریشه‌ی app باشد (کنار manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# 1) برای اجرای لوکال (بدون داکر): .env کنار manage.py
load_dotenv(BASE_DIR / ".env")
# 2) برای اجرای داخل داکر: اگر .env کنار docker-compose تزریق شد، نیازی نیست؛
#    ولی اگر خواستی، این خط هم کمکی است (در ایمیج ما مسیر کار /app است):
load_dotenv("/app/.env")

# ───────────────────────────────── Core
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", os.getenv("SECRET_KEY", "dev-change-me"))

_default_hosts = "localhost,127.0.0.1" if DEBUG else ""
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("DJANGO_ALLOWED_HOSTS", os.getenv("ALLOWED_HOSTS", _default_hosts)).split(",")
    if h.strip()
]

# ───────────────────────────────── Installed apps
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Local apps
    "authuser",
    "blog.apps.BlogConfig",
    "roadmap.apps.RoadmapConfig",
    "contact.apps.ContactConfig",
    "character.apps.CharacterConfig",
    "teams.apps.TeamsConfig",
    "faq.apps.FaqConfig",
]

AUTH_USER_MODEL = "authuser.User"

# ───────────────────────────────── Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise باید قبل از Session/CSRF باشد
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "admin_panel.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "admin_panel.wsgi.application"

# ───────────────────────────────── Database
# ترجیح: DATABASE_URL (مثل postgres://user:pass@host:5432/db)
# در غیر این صورت، سوئیچ خودکار به SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}
else:
    # سازگاری با متغیرهای قدیمی در صورت نیاز (MySQL/…)
    ENGINE = os.getenv("DATABASE_ENGINE", "django.db.backends.sqlite3")
    if ENGINE == "django.db.backends.sqlite3":
        DATABASES = {"default": {"ENGINE": ENGINE, "NAME": BASE_DIR / "db.sqlite3"}}
    else:
        DATABASES = {
            "default": {
                "ENGINE": ENGINE,
                "NAME": os.getenv("DB_NAME"),
                "USER": os.getenv("DB_USER"),
                "PASSWORD": os.getenv("DB_PASSWORD"),
                "HOST": os.getenv("DB_HOST", "127.0.0.1"),
                "PORT": os.getenv("DATABASE_PORT", "3306"),
                "ATOMIC_REQUESTS": True,
            }
        }

# ───────────────────────────────── Locale
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

# ───────────────────────────────── Static & Media
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
# در داکر از این مسیرها برای مپ‌کردن ولوم‌ها استفاده می‌کنیم
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise: سرو استاتیک در پشت Nginx یا حتی بدون آن
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ───────────────────────────────── CORS & CSRF
_raw_cors = os.getenv("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOWED_ORIGINS = [o.strip() for o in _raw_cors.split(",") if o.strip()]

# اگر بخواهی همه را در Dev باز کنی:
if os.getenv("CORS_ALLOW_ALL", "0") == "1":
    CORS_ALLOW_ALL_ORIGINS = True  # noqa

_raw_csrf = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _raw_csrf.split(",") if o.strip()]

# ───────────────────────────────── Security (فقط در Prod سفت می‌کنیم)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "0") == "1"  # پشت پروکسی SSL اگر True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

# ───────────────────────────────── DRF & JWT & Schema
REST_FRAMEWORK = {
    # Auth
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Pagination & Filtering
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    # OpenAPI/Schema
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Admin Panel API",
    "DESCRIPTION": "API schema for admin_panel project",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# ───────────────────────────────── Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": True},
    },
}
