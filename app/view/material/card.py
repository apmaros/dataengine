import pandas as p
import dash_html_components as html


def transactions_summary_card(in_txs_df: p.DataFrame, out_txs_df: p.DataFrame):
    return html.Div(className='card blue-grey darken-1', children=[
        html.Div(className='card-content white-text', children=[
            html.Div(className='card-title', children=[
                "Transactions Summary",
            ]),
            html.P(children=[
                html.P(f"Received £{in_txs_df.abs_amount.sum().round(2)} in {len(in_txs_df)} transactions"),
                html.P(f"Spent £{out_txs_df.abs_amount.sum().round(2)} in {len(out_txs_df)} transactions"),
            ])
        ]),
    ])
