from celery import Celery

app = Celery("coreworker")  # The name should match your Django app name

app.config_from_object("celeryconfig")


@app.task
def testCelery():
    return


app.autodiscover_tasks()
