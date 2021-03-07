import dash_table


def generate_table(dataframe):
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_size=50,
        filter_action='native',
        sort_action='native'
    )