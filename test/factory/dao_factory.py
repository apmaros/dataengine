from dataengine.model.dao.event import Event


def make_event(time, user_id, body, activity=None, duration=None, feel=None):
    event = Event()
    event.time = time
    event.user_id = user_id
    event.body = body
    event.activity = activity
    event.duration = duration
    event.feel = feel

    return event
