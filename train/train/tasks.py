import random
import celeryconfig
from celery import Celery
from train_data import SPEED_RANGE, STATIONS


BROKER_URL = "redis://localhost:6379"
BACKEND_URL = "redis://localhost:6379"

celery = Celery("train", broker=f"{BROKER_URL}", backend=f"{BACKEND_URL}")
celery.config_from_object(celeryconfig)
celery.conf.task_send_sent_event = True


@celery.task(name="current_speed", serializer="json")
def current_speed():
    speed = random.choice(SPEED_RANGE)
    return {"actual_speed": speed}


@celery.task(name="train_station", serializer="json")
def train_station():
    station = random.choice(STATIONS)
    return {"train_station": station}
