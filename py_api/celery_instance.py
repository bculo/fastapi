import time

from celery import Celery
from kombu import Exchange, Queue

from app_config import get_settings

settings = get_settings()
celery = Celery("tasks", broker=settings.message_broker_url)

DEFAULT_QUEUE = settings.default_queue
DEFAULT_EXCHANGE = settings.default_exchange
DEFAULT_ROUTING_KEY = settings.default_routing_key

celery.conf.task_queues = (
    Queue('test', Exchange('test'), routing_key='test.first'),
    Queue(DEFAULT_QUEUE, Exchange(DEFAULT_EXCHANGE, type='topic'), routing_key=DEFAULT_ROUTING_KEY),
)

celery.conf.task_default_queue = DEFAULT_QUEUE
celery.conf.task_default_exchange_type = DEFAULT_EXCHANGE
celery.conf.task_default_routing_key = DEFAULT_ROUTING_KEY


@celery.task
def send_push_notification(device_token: str):
    time.sleep(5)
    print(device_token)
