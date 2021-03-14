from typing import List
import dash_html_components as html
import pandas as p


def transactions_by_category_table(df: p.DataFrame):
    return html.Table(className="highlight striped", children=[
        html.Thead(children=[
            html.Tr(children=[
                html.Td("Category"),
                html.Td("Name")
            ])
        ]),
        html.Tbody(
            children=build_rows(df[['category', 'abs_amount']].to_numpy())
        )
    ])


def build_rows(rows: List):
    formatted_rows = []
    for row in rows:
        children = []
        for column in row:
            children.append(html.Td(_round_if_float(column)))
        formatted_rows.append(
            html.Tr(children=children)
        )

    return formatted_rows


def _round_if_float(v):
    if isinstance(v, float):
        return round(v, 2)
    else:
        return v
