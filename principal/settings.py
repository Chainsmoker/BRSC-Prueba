from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-h5)1hfx3qxizlp53yt-_=04pfhu!vjlo9n98(b4()og*55n@86'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
X_FRAME_OPTIONS = 'ALLOWALL'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    'ckeditor',
    'rest_framework',
    'tinymce',

    'apps.accounts',
    'apps.partidas_planos',
    'apps.centro_costos',
    'apps.control_expediente',
    'apps.hoja_requerimiento',
    'apps.tramites',
    'apps.asistencia',
    'apps.canta_callao',
    'apps.productividad',
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


ROOT_URLCONF = 'principal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'principal.wsgi.application'

MEDIA_URL = '/media/'
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

# PATH FILES
MEDIA_ROOT = BASE_DIR
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # archivo SQLite dentro del proyecto
    }
}




# Password validation
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
LANGUAGE_CODE = 'en'
#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = False

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# USER CUSTOMIZE
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = None

# Email configuration
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'b.r.santaclara@gmail.com'
# EMAIL_HOST_PASSWORD = 'lrwgwnmtkskxfzxm'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'Bienes Raices Santa Clara S.A.C. <b.r.santaclara@gmail.com>'

EMAIL_HOST = 'mail.privateemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@brsantaclara.com'
EMAIL_HOST_PASSWORD = 'Nellylupa2024'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Bienes Raices Santa Clara S.A.C. <info@brsantaclara.com>'


CKEDITOR_CONFIGS = {
    'default': {
        'enterMode': 2,         # CKEDITOR.ENTER_BR
        'shiftEnterMode': 1,    # CKEDITOR.ENTER_P
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline', 'Strike'],
            ['TextColor', 'BGColor'],  # 🎨 Botones de color de texto y fondo
            ['NumberedList', 'BulletedList'],
        ],
        'removePlugins': 'stylescombo',  # puedes dejar esto si no usas el combo de estilos
        #'height': 300,
        'format_tags': 'p;h1;h2;h3',  # deja algunos tags válidos
    }
}


DEFAULT_FILE_STORAGE = "control_expediente.storage.NormalizedFileSystemStorage"




TINYMCE_DEFAULT_CONFIG = {
    'license_key': 'gpl',
    "height": 200,
    "width": "100%",
    "menubar": "",
    "plugins": (
        "lists",  # ← NECESARIO para numlist y bullist
    ),
    "toolbar_mode": "wrap",
    "toolbar": (
        "bold italic underline forecolor backcolor removeformat "
        "numlist bullist "
        "uppercase lowercase"
    ),
    "contextmenu": "link image table",
    "branding": False,
    "promotion": False,
    "setup": """
        function (editor) {
            // Botón MAYÚSCULAS
            editor.ui.registry.addButton('uppercase', {
                text: 'A↑',
                tooltip: 'Convertir en MAYÚSCULAS',
                onAction: function () {
                    const selectedText = editor.selection.getContent({ format: 'text' });
                    editor.selection.setContent(selectedText.toUpperCase());
                }
            });

            // Botón minúsculas
            editor.ui.registry.addButton('lowercase', {
                text: 'a↓',
                tooltip: 'Convertir en minúsculas',
                onAction: function () {
                    const selectedText = editor.selection.getContent({ format: 'text' });
                    editor.selection.setContent(selectedText.toLowerCase());
                }
            });

            // Botón para lista con guiones (estilo cuadrado)
            editor.ui.registry.addButton('dashlist', {
                text: '-•',
                tooltip: 'Lista con guiones',
                onAction: function () {
                    editor.execCommand('InsertUnorderedList', false, {
                        'list-style-type': 'square'
                    });
                }
            });
        }
    """,
}


