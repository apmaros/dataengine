import typing as t
from dataclasses import asdict
from typing import List, Dict, Any

from influxdb_client import Point

from dataengine.common.util import day_to_daytime_str
from dataengine.monzo.api import get_transactions
from dataengine.monzo.model.Merchant import build_merchant
from dataengine.monzo.model.Transaction import build_transaction, Transaction
from dataengine.monzo.security import get_access_token, get_account_id


def get_txs_as_points(request, since=None, before=None):
    txs = _get_txs(request, since=since, before=before)
    return to_points(txs)


def to_points(transactions: t.List[Transaction]):
    return list(map(transaction_as_record, transactions))


def transaction_as_record(transaction: Transaction) -> Point:
    return (
        Point("transactions")
            .time(transaction.time)
            .tag('type', transaction.type)
            .tag('category', transaction.category)
            .tag('name', transaction.name)
            .field('amount', transaction.amount)
            .field('abs_amount', transaction.abs_amount))


def _get_txs(request, since=None, before=None) -> List[Dict[Any, Any]]:
    txs_raw = get_transactions(
        day_to_daytime_str(since) if since else None,
        day_to_daytime_str(before, True) if before else None,
        get_access_token(request),
        get_account_id(request),
    )

    txs = []
    for tx_raw in txs_raw['transactions']:
        txs.append(build_transaction_with_merchant(tx_raw))

    return txs


def build_transaction_with_merchant(raw_transaction):
    tx = build_transaction(raw_transaction).to_plot_dict()

    merchant = {}
    if raw_transaction["merchant"] is not None:
        merchant = build_merchant(raw_transaction.get('merchant', {}))
        tx['name'] = merchant.name
        merchant = asdict(merchant)

    return {**tx, **merchant}
