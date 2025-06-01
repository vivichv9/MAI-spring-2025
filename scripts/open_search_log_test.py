from datetime import datetime, timezone
from opensearchpy import OpenSearch, RequestsHttpConnection, NotFoundError
import logging
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenSearchLogger:
    def __init__(self, host, port, auth=None, use_ssl=False, verify_certs=True):
        """
        Инициализация клиента OpenSearch
        
        :param host: Хост OpenSearch
        :param port: Порт OpenSearch
        :param auth: Кортеж (username, password) для аутентификации
        :param use_ssl: Использовать SSL
        :param verify_certs: Проверять SSL сертификаты
        """
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=auth,
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            connection_class=RequestsHttpConnection
        )
        
        try:
            if not self.client.ping():
                raise ConnectionError("Не удалось подключиться к OpenSearch")
            logger.info("Успешно подключено к OpenSearch")
        except Exception as e:
            logger.error(f"Ошибка подключения к OpenSearch: {e}")
            raise

    def ensure_index_exists(self, index_name):
        """Проверяет существование индекса и создает его при необходимости"""
        try:
            if not self.client.indices.exists(index=index_name):
                self.client.indices.create(index=index_name)
                logger.info(f"Создан новый индекс: {index_name}")
        except Exception as e:
            logger.error(f"Ошибка при создании индекса: {e}")
            raise

    def log_to_opensearch(self, index_name, log_data):
        """
        Запись лога в OpenSearch
        
        :param index_name: Название индекса
        :param log_data: Данные лога в виде словаря
        """
        try:
            self.ensure_index_exists(index_name)
            
            log_data['@timestamp'] = datetime.now(timezone.utc).isoformat()
            
            response = self.client.index(
                index=index_name,
                body=log_data,
                refresh=True
            )
            
            logger.info(f"Лог успешно записан. ID: {response['_id']}")
            return response
        except NotFoundError:
            logger.error(f"Индекс {index_name} не существует и не может быть создан")
            raise
        except Exception as e:
            logger.error(f"Ошибка при записи лога: {e}")
            raise

if __name__ == "__main__":
    OPENSEARCH_HOST = "localhost"
    OPENSEARCH_PORT = 9203
    OPENSEARCH_AUTH = ("admin", "OlfbVWQ_FvzhKRsYsVBW%bL9N_fi%%_B")
    
    INDEX_NAME = "project_logs"
    
    try:
        os_logger = OpenSearchLogger(
            host=OPENSEARCH_HOST,
            port=OPENSEARCH_PORT,
            auth=OPENSEARCH_AUTH,
            use_ssl=False,
            verify_certs=False
        )
        
        for i in range(1):
            time.sleep(random.random())
            sample_log = {
                "level": "INFO",
                "message": f"Это тестовая запись лога_{i}",
                "service": "example-service",
            }            
            os_logger.log_to_opensearch(INDEX_NAME, sample_log)
        
    except Exception as e:
        logger.error(f"Ошибка в работе логера: {e}")