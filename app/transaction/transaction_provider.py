from dataclasses import asdict
import pandas as pd
from influxdb_client import Point
import typing as t
from app.model.Merchant import build_merchant
from app.model.Transaction import build_transaction, Transaction
from app.monzo.api import get_monzo_config, get_transactions
from app.monzo.security import get_access_token, get_account_id
from app.util import _day_to_daytime_str


def get_txs_df(request, since=None, before=None) -> pd.DataFrame:
    """
    Returns DataFrame containing all transactions from Monzo
    in given period of time
    :param request:
    :param since: start date for transactions
    :param before: end date for transactions
    :return: transactions in DataFrame
    """
    return pd.DataFrame(_get_txs(request=request, since=since, before=before))


def get_txs_as_points(request, since=None, before=None) -> pd.DataFrame:
    txs = _get_txs(request, since=since, before=before)
    return list(map(
        lambda tx: Point("transactions")
            .time(tx['time'])
            .tag('type', tx['type'])
            .tag('category', tx['category'])
            .tag('name', tx['name'])
            .field('amount', tx['amount'])
            .field('abs_amount', tx['abs_amount']),
        txs))


config = get_monzo_config()


# TODO - remove request from the method
def _get_txs(request, since=None, before=None) -> t.List[Transaction]:
    txs_raw = get_transactions(
        _day_to_daytime_str(since) if since else None,
        _day_to_daytime_str(before, True) if before else None,
        get_access_token(request),
        get_account_id(request),
    )

    txs = []
    for tx_raw in txs_raw['transactions']:
        tx = build_transaction(tx_raw).to_plot_dict()

        merchant = {}
        if tx_raw["merchant"] is not None:
            merchant = build_merchant(tx_raw.get('merchant', {}))
            tx['name'] = merchant.name
            merchant = asdict(merchant)

        txs.append({**tx, **merchant})

    return txs
