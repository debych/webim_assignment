from django.core.exceptions import ObjectDoesNotExist

from .models import RandomNumber
from webim.celery import app
import random


@app.task
def UpdateRandomNumber():
    try:
        n = RandomNumber.objects.get(pk=1)
        n.number = random.randint(0, 10000000)
    except ObjectDoesNotExist:
        n = RandomNumber.objects.create(number=random.randint(0, 10000000))
    n.save()
