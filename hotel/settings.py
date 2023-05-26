
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
# My Own Apps
    'home',
    'payment',
    'auth_app',
  
#Third Party Apps
    'smart_selects',
    'cities_light',
    

]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hotel.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'hotel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'hotel_db',
    #     'USER': 'railway',
    #     'PASSWORD': '',
    #     'HOST': 'mysql',
    #     'PORT': '3306',
    # }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# STATIC_ROOT = 'staticfiles'

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles','static')

STATICFILES_DIRS = [BASE_DIR / "static"]
# STATICFILES_DIR = {
#     os.path.join(BASE_DIR , "static")
# }

MEDIA_ROOT =  os.path.join(BASE_DIR, 'public/static') 
MEDIA_URL = '/media/'




if DEBUG:
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')


# Uncomment these lines if you have a live keys
# else:
#     STRIPE_PUBLISHABLE_KEY = 'production_publishable_key'
#     STRIPE_SECRET_KEY = 'production_secret_key'




BACKEND_DOMAIN='http://127.0.0.1:8000'
PAYMENT_SUCCESS_URL='http://127.0.0.1:8000/payment/success/'
PAYMENT_CANCEL_URL='http://127.0.0.1:8000/payment/cancel/'

STRIPE_WEBHOOK_SECRET="whsec_2b90b0ec5cd124f7463f570dabffacf456a1c447558faf2b79c4a03fcf3ed3ad"

USE_DJANGO_JQUERY = True
JQUERY_URL = False
MIDDLEWARE_CLASSES = MIDDLEWARE
SMART_SELECTS_USE_DJANGO_ADMIN = True
SMART_SELECTS_ALLOW_ADDITIONAL_RELATIONS = True




AUTH_USER_MODEL='auth_app.User'

SITE_ID = 1


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


LOGIN_REDIRECT_URL = '/login/' 
 

