from celery import Celery
from core.settings import settings


print("Redis URL:", settings.redis_settings.redis_url)
celery_app = Celery(main="shop",
                    broker=settings.redis_settings.redis_url,
                    backend=settings.redis_settings.redis_url,
                    broker_connection_retry_on_startup=True,
                    )

celery_app.autodiscover_tasks(packages=["apps.auth"])