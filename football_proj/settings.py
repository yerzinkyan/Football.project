#  содержит основные настройки проекта Django.
# (конфигурация приложений, шаблоновб middleware ...)

from pathlib import Path
import os
import environ



env = environ.Env()
environ.Env.read_env()

# базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent
print("BASE_DIR:", BASE_DIR)

# секректный ключ для безопасности
SECRET_KEY = env('SECRET_KEY')
print("SECRET_KEY:", SECRET_KEY)

# режим отладки
DEBUG = bool(env('DEBUG'))

ALLOWED_HOSTS_LIST = env('ALLOWED_HOSTS').split(',')
ALLOWED_HOSTS = [s.strip() for s in ALLOWED_HOSTS_LIST]
if DEBUG:
    print(f"ALLOWED_HOSTS : {ALLOWED_HOSTS}")

# список страндартных приложений Django

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


# список сторонних приложений
THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'play',
]





# общий список приложений
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS


# список middleware для обработки запросов  
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# корневой  URL файл проекта
ROOT_URLCONF = 'football_proj.urls'

# конфигурация шаблонов Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'football_proj.wsgi.application'


# конфигурация базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
        'ATOMIC_REQUESTS': True,
     }
}

# валидаторы паролей
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


# настройки интернационализации
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



# настройки статических файлов
STATIC_URL = 'static/'    # URL статики 
STATIC_ROOT = BASE_DIR / 'staticfiles'   # Путь для собранных  файлов статики

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# настройки Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
    },
    "DEFAULT_RENDERER_CLASSES": [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ]
}

# настройки CORS для разработки и продакшена
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:3000',
    ]

#Настройки безопасности
SECURE_BROWSER_XSS_FILTER = True  # Защита от XSS атак
SECURE_CONTENT_TYPE_NOSNIFF = True  # Запрет на MINE типов
X_FRAME_OPTIONS = 'DENY'  # Защита от кликджекинга


# Настройки логирования
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',  # уровень логирования
                'class': 'logging.FileHandler', #логирование в файл
                'filename': BASE_DIR / 'debug.log', # путь к файлу логов
            }, 
        },
        'loggers': {
            'django': {
                'handlers': ['file'], # использукемый обработчик
                'level': 'INFO', # уровень логирования
                'propagate': True, # передача логов в родительские логгерам
            },
        },
    }