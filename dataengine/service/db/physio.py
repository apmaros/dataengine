import typing
import uuid

from sqlalchemy import func

from dataengine import Context
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
