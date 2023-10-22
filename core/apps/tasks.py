from celery import shared_task
# Create your views here.


@shared_task
def shardTeskTest():
    return {"Key": 5555}
