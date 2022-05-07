import typing as t
import uuid

from sqlalchemy import select, desc

from dataengine import Context
from dataengine.model.dao.user_metric import UserMetric


def get_user_metric(user_metric_id: str) -> UserMetric:
    stmt = (select(UserMetric)
            .filter(UserMetric.id == user_metric_id))

    with Context.db_session() as session:
        user_metric = session.execute(stmt).scalars().one()

    return user_metric


def get_user_metrics(user_id: str) -> t.List[UserMetric]:
    stmt = (select(UserMetric)
            .filter(UserMetric.user_id == user_id)
            .order_by(desc(UserMetric.name)))

    with Context.db_session() as session:
        user_metrics = session.execute(stmt).scalars().all()

    return user_metrics


def put_user_metric(user_id, args):
    user_metric_id = args.get('id', uuid.uuid4())

    user_metric = UserMetric(
        id=user_metric_id,
        user_id=user_id,
        name=args['name'],
    )

    with Context.db_session() as session:
        session.add(user_metric)
        session.commit()
