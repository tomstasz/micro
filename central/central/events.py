import os
import logging
import time
import requests
from celery import Celery
from datetime import datetime as dt


LINEMAN_URL = os.environ.get("LINEMAN_URL") or "http://localhost:5002/api/v1/barrier"


class Logger:
    def _to_datetime(self, timestamp):
        hour = dt.fromtimestamp(timestamp).strftime("%H:%M:%S")
        return hour if timestamp is not None else None

    def _log_message(self, date, value):
        return f"{date}: {value}"

    def prepare_logger(self, file_name):
        handler = logging.FileHandler(file_name)
        logger = logging.getLogger(file_name)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        return logger

    def incoming_station(self, station, date):
        station_log.info(self._log_message(date, station))
        barrier_status = requests.get(LINEMAN_URL).json()["status"]
        if barrier_status == "closed":
            station_log.info(self._log_message(date, "anomalia - barrier_closed"))
        else:
            requests.post(LINEMAN_URL, data={"status": "closed"})
        time.sleep(10)
        date = dt.now().strftime("%H:%M:%S")
        requests.post(LINEMAN_URL, data={"status": "opened"})
        station_log.info(self._log_message(date, "barrier opened again"))

    def speed_check(self, current_speed, date):
        if 0.0 <= current_speed <= 40.0:
            slow_log.info(self._log_message(date, current_speed))
        elif 40.1 <= current_speed <= 140.0:
            normal_log.info(self._log_message(date, current_speed))
        elif 140.1 <= current_speed <= 180.0:
            fast_log.info(self._log_message(date, current_speed))

    def check_event_result(self, event):
        value = event.split(":")[1].strip()[:-1]
        if "train" in event:
            return value
        else:
            value = float(value)
            return value


class CeleryEventsHandler:
    def __init__(self, celery_app):
        self._app = celery_app
        self._state = celery_app.events.State()
        self._logger = Logger()

    def _event_handler(handler):
        def wrapper(self, event):
            self._state.event(event)
            task = self._state.tasks.get(event["uuid"])
            date = self._logger._to_datetime(task.timestamp)
            res = self._logger.check_event_result(task.result)
            self._logger.speed_check(res, date) if isinstance(
                res, float
            ) else self._logger.incoming_station(res, date)

            handler(self, event)

        return wrapper

    @_event_handler
    def _on_task_succeeded(self, event):
        pass

    def start_listening(self):
        with self._app.connection() as connection:
            recv = self._app.events.Receiver(
                connection, handlers={"task-succeeded": self._on_task_succeeded}
            )
            recv.capture(limit=None)


if __name__ == "__main__":
    app = Celery(broker="redis://localhost:6379")
    station_log = Logger().prepare_logger("info.log")
    slow_log = Logger().prepare_logger("slow.log")
    normal_log = Logger().prepare_logger("normal.log")
    fast_log = Logger().prepare_logger("fast.log")
    events_handler = CeleryEventsHandler(app)
    events_handler.start_listening()
