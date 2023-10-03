from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery("coreCelery")

app.config_from_object("coreapis.conf:settings", namespace="CELERY")


@app.task
def testCelery():
    return


app.autodiscover_tasks()
