import dash_table


def generate_table(df):
    df = df[['emoji', 'name', 'abs_amount', 'category', 'date', 'address']]
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        page_size=50,
        filter_action='native',
        sort_action='native'
    )
