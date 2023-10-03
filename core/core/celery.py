from celery import Celery
import os
import sys
# sys.path.append('/usr/src/app/ds-project/ds-core')  # Adjust the path as needed

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery("core")  # The name should match your Django app name

app.config_from_object("django.conf:settings", namespace="CELERY")


@app.task
def testCelery():
    return


app.autodiscover_tasks()
