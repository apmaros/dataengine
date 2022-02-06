import typing
import uuid

from sqlalchemy import select, func, desc

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.heart_pressure_reading import HeartPressureReading


def put_heart_rate_reading(user_id: str, args: typing.Dict[str, str]):
    hp_reading = HeartPressureReading(
        id=uuid.uuid4(),
        user_id=user_id,
        systolic=int(args['systolic']),
        diastolic=int(args['diastolic']),
        heart_rate=int(args['heart-rate']),
        last_activity=args.get('last-activity', None),
        created_at=func.now()
    )

    with Context.db_session() as session:
        session.add(hp_reading)
        session.commit()


def get_heart_rate_readings_since(user_id, days_ago) -> typing.List[HeartPressureReading]:
    stmt = get_model_items_since_stmt(HeartPressureReading, user_id, days_ago)

    with Context.db_session() as session:
        events = session.execute(stmt).scalars().all()

    return events


def get_model_items_since_stmt(model: typing.Any, user_id: str, days_ago: int) -> typing.List:
    return (select(model)
            .filter(model.user_id == user_id)
            .filter(model.created_at > days_ago_datetime(days_ago))
            .order_by(desc(model.created_at))
            )
