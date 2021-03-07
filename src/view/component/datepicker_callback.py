from datetime import date, timedelta
from flask import request
from src.server import dash_app
from src.transaction.transaction_provider import get_txs_df
from src.transaction.transformations import get_out_txs, group_by_category, group_by_date
from src.view.component.table import generate_table
import plotly.express as px


def get_transactions_dfs(start_date_raw, end_date_raw):
    if start_date_raw:
        start_date = date.fromisoformat(start_date_raw)
    else:
        start_date = date.today() - timedelta(days=7)

    if end_date_raw is not None:
        end_date = date.fromisoformat(end_date_raw)
    else:
        end_date = date.today()

    txs_df = get_txs_df(request, start_date, end_date)
    out_txs_df = get_out_txs(txs_df)
    dash_app.logger.info(
        f"since={start_date_raw} until={end_date_raw} txs={len(txs_df)}"
    )

    txs_table = generate_table(out_txs_df[['emoji', 'name', 'abs_amount', 'category', 'date', 'address']])

    out_txs_by_name_fig = px.bar(out_txs_df, x="name", y="abs_amount", barmode="group")

    out_txs_by_name_category_fig = px.scatter(
        out_txs_df, x="date", y='abs_amount', hover_name="name", color='category', size='abs_amount'
    )

    txs_by_category_fig = px.bar(
        group_by_category(out_txs_df), x="category", y="abs_amount", color="category"
    )

    txs_by_date_agg_fig = px.line(group_by_date(out_txs_df), x='date', y="abs_amount")

    return txs_table, out_txs_by_name_fig, out_txs_by_name_category_fig, txs_by_category_fig, txs_by_date_agg_fig
