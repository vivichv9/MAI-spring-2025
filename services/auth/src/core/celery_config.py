from core.logger import setup_logging
setup_logging(log_file_path="/tmp/logs/logs.txt", service_name="shop-app")

from celery import Celery
from core.settings import settings


celery_app = Celery(main="shop",
                    broker=settings.redis_settings.redis_url,
                    backend=settings.redis_settings.redis_url,
                    broker_connection_retry_on_startup=True,
                    )

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

celery_app.autodiscover_tasks(packages=["apps.auth"])