from dataclasses import asdict
import pandas as pd
from app.model.Merchant import build_merchant
from app.model.Transaction import build_transaction
from app.monzo.api import get_transactions
from app.util import _day_to_daytime_str


def get_txs_df(req, since=None, before=None) -> pd.DataFrame :
    """
    Returns DataFrame containing all transactions from Monzo
    in given period of time
    :param req:
    :param since: start date for transactions
    :param before: end date for transactions
    :return: transactions in DataFrame
    """
    txs_raw = get_transactions(
        req,
        _day_to_daytime_str(since) if since else None,
        _day_to_daytime_str(before, True) if before else None
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

    return pd.DataFrame(txs)
