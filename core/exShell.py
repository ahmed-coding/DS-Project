from apps.notifications.tasks import testTask
from apps.tasks import shardTeskTest
shardTeskTest.delay()
testTask.delay("Teeest")
