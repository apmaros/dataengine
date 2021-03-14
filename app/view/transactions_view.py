from datetime import datetime, date, timedelta

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from dateutil.relativedelta import relativedelta

from app.server import dash_app
from app.view.component.date_range_picker import get_transactions_dfs, build_date_picker, _last_week_date
from app.view.constants import TXSGraphConstants


@dash_app.callback(
    Output(component_id=TXSGraphConstants.TABLE, component_property='children'),
    Output(component_id=TXSGraphConstants.BY_NAME, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_NAME_AND_CATEGORY, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_CATEGORY, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_DATE_AGG, component_property='figure'),
    Output(component_id=TXSGraphConstants.MERCHANT_MAP, component_property='figure'),
    Output(component_id=TXSGraphConstants.SUMMARY_CARD, component_property='children'),
    Output(component_id=TXSGraphConstants.SUMMARY_BY_CATEGORY_CARD, component_property='children'),
    Output(component_id='date-picker', component_property='children'),
    [
        Input(component_id='txs-date-range', component_property='start_date'),
        Input(component_id='txs-date-range', component_property='end_date'),
        Input(component_id='txs-this-month', component_property='n_clicks'),
        Input(component_id='txs-this-year', component_property='n_clicks'),
    ]
)
def update_output_div(start_date_raw, end_date_raw, this_month, this_year):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == "txs-this-month":
        start_date = datetime.today().replace(day=28) - relativedelta(months=1)
        end_date = datetime.today()

    else:
        if start_date_raw:
            start_date = date.fromisoformat(start_date_raw)
        else:
            start_date = date.today() - timedelta(days=7)

        if end_date_raw is not None:
            end_date = date.fromisoformat(end_date_raw)
        else:
            end_date = date.today()

    dataframes = get_transactions_dfs(start_date, end_date)
    return dataframes + (build_date_picker(start_date, end_date),)


def init(app):
    app.layout = html.Div(className='container', children=[
        html.H1("Transactions Summary"),
        html.Div(className="row", children=[
            html.Div(id="date-picker", className="input-field", children=[
                html.Div(["Date: ", build_date_picker()]),
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className="col s6", children=[
                html.A("This Budget Month", id="txs-this-month", className="waves-effect waves-light btn"),
                html.A("This Year", id="txs-this-year", className="waves-effect waves-light btn"),
                html.Br(),
                html.Div(id=TXSGraphConstants.SUMMARY_CARD)
            ]),
            html.Div(className="col s6", children=[
                html.Div(id=TXSGraphConstants.SUMMARY_BY_CATEGORY_CARD)
            ])
        ]),

        dcc.Graph(id=TXSGraphConstants.BY_DATE_AGG),
        html.H2(children="Transactions"),
        html.Div(id=TXSGraphConstants.TABLE),
        dcc.Graph(id=TXSGraphConstants.BY_NAME),
        dcc.Graph(id=TXSGraphConstants.BY_NAME_AND_CATEGORY),
        dcc.Graph(id=TXSGraphConstants.BY_CATEGORY),
        html.H2("Merchants"),
        dcc.Graph(id=TXSGraphConstants.MERCHANT_MAP),
    ])

    app.run_server(debug=True)
