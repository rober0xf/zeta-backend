from django_prose_editor.fields import ProseEditorField
from pathlib import Path
import environ
import os

BASE_DIR_BACKEND = Path(__file__).resolve().parent.parent
BASE_DIR_FRONTED = BASE_DIR_BACKEND.parent / "zeta-frontend"

env = environ.Env()
environ.Env.read_env(BASE_DIR_BACKEND / ".env")

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS_DEV")

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# here we add our created apps
PROJECT_APPS = ["apps.blog", "apps.categories"]

THIRD_PARTY_APPS = ["corsheaders", "rest_framework", "django_prose_editor"]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

content = ProseEditorField(
    extensions={"Bold": True, "Italic": True, "BulletList": True, "Link": True},
    sanitize=True,
)

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR_FRONTED, "build")],
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

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR_BACKEND / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR_BACKEND, "staticfiles")
STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR_BACKEND, "media")
MEDIA_URL = "media/"

STATICFILES_DIRS = [os.path.join(BASE_DIR_FRONTED, "build/static")]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# configure the django rest framework options
REST_FRAMEWORK = {"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticatedOrReadOnly"]}

# configure cors
CORS_ORIGIN_WHITELIST_DEV = env.list("CORS_ORIGIN_WHITELIST_DEV")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS_DEV")

# show in console like a log, (development)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if not DEBUG:
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS_DEPLOY")
    CORS_ORIGIN_WHITELIST_DEPLOY = env.list("CORS_ORIGIN_WHITELIST_DEPLOY")
    CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS_DEPLOY")

    DATABASES = {"default": env.db("DATABASE_URL")}

    # avoid duplicated requests
    DATABASES["default"]["ATOMIC_REQUESTS"] = True
