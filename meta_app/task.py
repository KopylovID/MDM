from celery import shared_task
import logging
logger = logging.getLogger(__name__)

@shared_task
def info_test(message: str):
    logger.info(message)
