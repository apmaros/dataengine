import typing
from datetime import datetime

from sqlalchemy import select, desc

from dataengine import Context
from dataengine.common.util import days_ago_datetime
from dataengine.model.dao.metric import Metric


def put_metric(user_id: str, args: typing.Dict[str, str]):
    metric = _args_to_metric(user_id, args)

    with Context.db_session() as session:
        session.add(metric)
        session.commit()


def get_metrics_since(
        user_id: str,
        metric_name: str,
        days_ago: int
) -> typing.List[Metric]:
    stmt = (select(Metric)
            .filter(Metric.user_id == user_id)
            .filter(Metric.name == metric_name)
            .filter(Metric.time > days_ago_datetime(days_ago))
            .order_by(desc(Metric.time)))

    with Context.db_session() as session:
        metrics = session.execute(stmt).scalars().all()

    return metrics


def get_metrics_by_user_metric_id_since(
        user_id: str,
        user_metric_id: str,
        days_ago: int
) -> typing.List[Metric]:
    stmt = (select(Metric)
            .filter(Metric.user_id == user_id)
            .filter(Metric.user_metric_id == user_metric_id)
            .filter(Metric.time > days_ago_datetime(days_ago))
            .order_by(desc(Metric.time)))

    with Context.db_session() as session:
        metrics = session.execute(stmt).scalars().all()

    return metrics


def _args_to_metric(user_id: str, args: typing.Dict[str, str]) -> Metric:
    time = args.get('time')

    return Metric(
        user_id=user_id,
        name=args['metric-name'],
        value=args['value'],
        event=args['event'],
        time=time if time else datetime.utcnow(),
    )
