"""Settings for local env."""

SECRET_KEY = ''

DEBUG = True

ALLOWED_HOSTS = []

SENTRY_DSN = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'white_label',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': 5432
    }
}

FROM_EMAIL_ADDRESS = ''

CONTACT_FORM_EMAIL = FROM_EMAIL_ADDRESS

# Django debug toolbar settings
if DEBUG:
    INTERNAL_IPS = ['127.0.0.1', ]

CORS_ORIGIN_ALLOW_ALL = True

FRONTEND_BASE_URL = ''

CELERY_BROKER_URL = 'redis://localhost:6379'

# Payment processor settings
PAYMENT_PROCESSORS = {
    'stripe': {
        'processor': 'payments.processors.stripe.Stripe',
        'secret_key': '',
        'webhook_secret_key': '',
    }
}
REFUND_REQUEST_DAYS = 0

SKIP_ACTIVATION = False

IS_EMAIL_SENDING_ENABLED = True

INITIAL_AGREEMENT_TYPE_NAMES = []
