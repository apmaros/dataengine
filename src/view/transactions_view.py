import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
from src.server import dash_app
from src.view.component.date_range_picker import get_transactions_dfs, build_date_picker
from src.view.constants import TXSGraphConstants


@dash_app.callback(
    Output(component_id=TXSGraphConstants.TABLE, component_property='children'),
    Output(component_id=TXSGraphConstants.BY_NAME, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_NAME_AND_CATEGORY, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_CATEGORY, component_property='figure'),
    Output(component_id=TXSGraphConstants.BY_DATE_AGG, component_property='figure'),
    Output(component_id=TXSGraphConstants.MERCHANT_MAP, component_property='figure'),
    [
        Input(component_id='txs-date-range', component_property='start_date'),
        Input(component_id='txs-date-range', component_property='end_date')
    ]
)
def update_output_div(start_date_raw, end_date_raw):
    return get_transactions_dfs(start_date_raw, end_date_raw)


def init(app):
    app.layout = html.Div(className='ui container', children=[
        html.Div(id='foo', className="ui sizer vertical segment", children=[
            html.Div(className="ui huge header", children="Transactions Summary")
        ]),

        html.Div(["Date: ", build_date_picker()]),
        dcc.Graph(id=TXSGraphConstants.BY_DATE_AGG),
        html.H2(children="Transactions"),
        html.Div(id=TXSGraphConstants.TABLE),
        dcc.Graph(id=TXSGraphConstants.BY_NAME),
        dcc.Graph(id=TXSGraphConstants.BY_NAME_AND_CATEGORY),
        dcc.Graph(id=TXSGraphConstants.BY_CATEGORY),
        dcc.Graph(id=TXSGraphConstants.MERCHANT_MAP)
    ])

    app.run_server(debug=True)
