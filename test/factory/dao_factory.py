import datetime

from dataengine.common.util import random_str, current_time_sec
from dataengine.model.dao.event import Event
from dataengine.model.dao.metric import Metric
from dataengine.model.dao.user_metric import UserMetric


def make_event(time, user_id, body, activity=None, duration=None, feel=None):
    event = Event()
    event.time = time
    event.user_id = user_id
    event.body = body
    event.activity = activity
    event.duration = duration
    event.feel = feel

    return event


def make_user_metric(
        user_id: str = random_str(),
        name: str = random_str(),
        description: str = random_str(),
        created_at: int = current_time_sec(),
):
    user_metric = UserMetric()
    user_metric.id = random_str()
    user_metric.user_id = user_id
    user_metric.name = name
    user_metric.description = description
    user_metric.created_at = created_at

    return user_metric


def make_metric(
    user_id: str = random_str(),
    user_metric_id: str = random_str(),
    name: str = random_str(),
    value: str = 1,
    event: str = random_str(),
    time: str = datetime.datetime.today(),
):
    metric = Metric()
    metric.user_id = user_id
    metric.user_metric_id = user_metric_id
    metric.name = name
    metric.value = value
    metric.event = event
    metric.time = time

    return metric
