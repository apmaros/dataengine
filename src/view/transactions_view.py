from datetime import date, timedelta
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from src.server import dash_app
from src.view.component.datepicker_callback import get_transactions_dfs
from src.view.constants import TXSGraphConstants


@dash_app.callback(
    Output(component_id=TXSGraphConstants.TABLE, component_property='children'),
    Output(component_id=TXSGraphConstants.BY_NAME, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_NAME_AND_CATEGORY, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_CATEGORY, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_DATE_AGG, component_property='figure'),
    [
        Input(component_id='txs-date-range', component_property='start_date'),
        Input(component_id='txs-date-range', component_property='end_date')
    ]
)
def update_output_div(start_date_raw, end_date_raw):
    return get_transactions_dfs(start_date_raw, end_date_raw)


def init(app):
    app.layout = html.Div(children=[
        html.Div(id='foo', className="ui sizer vertical segment", children=[
            html.Div(className="ui huge header", children="Transactions Summary")
        ]),
        html.H1(children='Transaction Summary'),

        html.H2(children="Date"),
        html.Div([
            "Input: ",
            dcc.DatePickerRange(
                id='txs-date-range',
                min_date_allowed=date(2010, 1, 1),
                max_date_allowed=date.today() + timedelta(days=1),
                initial_visible_month=date.today(),
                end_date=date.today(),
                persistence=True,
                updatemode='bothdates'
            )],
        ),

        dcc.Graph(
            id=TXSGraphConstants.BY_DATE_AGG
        ),

        html.H2(children="Transactions"),

        html.Div(id=TXSGraphConstants.TABLE),

        dcc.Graph(
            id=TXSGraphConstants.BY_NAME
        ),
        dcc.Graph(
            id=TXSGraphConstants.BY_NAME_AND_CATEGORY
        ),
        dcc.Graph(
            id=TXSGraphConstants.BY_CATEGORY
        )
    ])

    app.run_server(debug=True)
