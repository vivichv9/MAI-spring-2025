# superset_config.py

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://superset:superset@postgres:5432/superset'

# Настройки безопасности
SECRET_KEY = 'your-secret-key-here'  # Замени на свой ключ
# TALISMAN_ENABLED = True
# CONTENT_SECURITY_POLICY_WARNING = False

# Redis
CACHE_REDIS_HOST = "redis"
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0
CACHE_TYPE = "RedisCache"
FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://redis:6379/1',
}

EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_REDIS_URL': 'redis://redis:6379/2',
}

FLASK_ENV="production"
CELERYD_LOG_LEVEL="INFO"
C_FORCE_ROOT=True
BROKER_CONNECTION_RETRY_ON_STARTUP=True

# Celery
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'