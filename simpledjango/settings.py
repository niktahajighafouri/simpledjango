# simpledjango / settings.py
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&$$ud%*i$7*q_31m(nlnn1wc^t6=lep^(s42z3o5+(flk*94^4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io']

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Required for GraphiQL
    'accounts.apps.AccountsConfig',
    # 'accounts',
    'home',
    'tasks.apps.TasksConfig',
    'django.contrib.admin',
    'graphene_django',
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
]

# # 'django_admin_interface',
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simpledjango.urls'

# # 'DIRS': [os.path.join(BASE_DIR, 'templates')],  # <<< این خط مهم است
# 'DIRS': [
#     # [os.path.join(BASE_DIR, 'templates')],
#     # BASE_DIR / "templates",  # مسیر پیش‌فرض
#     # BASE_DIR / "templates/public",  # اضافه کردن پوشه public
# ],

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simpledjango.wsgi.application'

LOGIN_REDIRECT_URL = "/"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'  # مسیر عمومی برای دسترسی به فایل‌های استاتیک
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # مسیر ذخیره فایل‌های استاتیک جمع‌آوری شده

STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_DIRS = [BASE_DIR / 'static', ]

STATICFILES_DIRS = [
    BASE_DIR / "static",
    # os.path.join(BASE_DIR, 'static')
]
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

GRAPHENE = {
    # 'SCHEMA': 'home.schema.schema',
    'SCHEMA': 'simpledjango.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ]
}

GRAPHQL_JWT = {
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=10),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
}
# GRAPHQL_JWT = {
#     "JWT_ALLOW_ANY_CLASSES": [],
#     "JWT_VERIFY_EXPIRATION": True,
#     "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
#     "JWT_AUTH_HEADER_PREFIX": "Bearer",
#     "JWT_REFRESH_EXPIRED_HANDLER": "graphql_jwt.refresh_token.shortcuts.default_refresh_expired_handler",
#     "JWT_BLACKLIST_AFTER_ROTATION": True,
#     "JWT_TOKEN_CLASSES": {
#         'access': 'graphql_jwt.tokens.AccessToken',
#         'refresh': 'graphql_jwt.tokens.RefreshToken',
#     },
# }

AUTH_USER_MODEL = 'accounts.CustomUser'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# ADMIN_INTERFACE_DEFAULT_THEME = 'purple'

# DJANGO_ADMIN_INTERFACE = {
#     "theme": "purple",
# }
X_FRAME_OPTIONS = 'SAMEORIGIN'
SILENCED_SYSTEM_CHECKS = ['security.W019']
