from datetime import date, timedelta
from flask import request
from app.server import dash_app
from app.transaction.transaction_provider import get_txs_df
from app.transaction.transformations import get_out_txs, group_by_category, group_by_date, get_in_txs
from app.util import _last_week_date
from app.view.component.map import build_txs_map
from app.view.component.table import generate_table
import plotly.express as px
import dash_core_components as dcc

from app.view.component.transactions_by_category_table import transactions_by_category_table
from app.view.material.card import transactions_summary_card


# TODO better name e.g. load_transactions
def get_transactions_dfs(start_date, end_date):
    txs_df = get_txs_df(request, start_date, end_date)
    out_txs_df = get_out_txs(txs_df)
    dash_app.logger.info(
        f"since={start_date} until={end_date} txs={len(txs_df)}"
    )

    txs_table = generate_table(out_txs_df)

    out_txs_by_name_fig = px.bar(out_txs_df, x="name", y="abs_amount", barmode="group")

    out_txs_by_name_category_fig = px.scatter(
        out_txs_df, x="date", y='abs_amount', hover_name="name", color='category', size='abs_amount'
    )

    txs_by_category_df = group_by_category(out_txs_df)

    txs_by_category_fig = px.bar(
        txs_by_category_df, x="category", y="abs_amount", color="category"
    )

    txs_by_date_agg_fig = px.line(group_by_date(out_txs_df), x='date', y="abs_amount")

    txs_map = build_txs_map(out_txs_df)

    summary_card = transactions_summary_card(get_in_txs(txs_df), out_txs_df)

    summary_by_category_card = transactions_by_category_table(txs_by_category_df)

    return \
        txs_table,\
        out_txs_by_name_fig, \
        out_txs_by_name_category_fig, \
        txs_by_category_fig, \
        txs_by_date_agg_fig, \
        txs_map, \
        summary_card, \
        summary_by_category_card


def build_date_picker(start_date=_last_week_date(), end_date=date.today()):
    return dcc.DatePickerRange(
            start_date_placeholder_text="Since",
            end_date_placeholder_text="Until",
            id='txs-date-range',
            min_date_allowed=date(2010, 1, 1),
            max_date_allowed=date.today() + timedelta(days=1),
            initial_visible_month=date.today(),
            start_date=start_date,
            end_date=end_date,
            updatemode='bothdates',
            clearable=True,
            className="txs-date-range-picker"
        )

