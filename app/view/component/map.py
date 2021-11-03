import plotly.express as px

from app.config import MAPBOX_TOKEN

MARGIN = 20


def build_txs_map(df):
    return px.scatter_mapbox(
        df,
        lat="latitude",
        lon="logitude",
        hover_name="name",
        hover_data=["name", 'address', 'date'],
        color_discrete_sequence=["fuchsia"], zoom=12, height=600)\
        .update_mapboxes(center_lon=-0.118092, center_lat=51.509865)\
        .update_layout(mapbox_style="dark", mapbox_accesstoken=MAPBOX_TOKEN)\
        .update_layout(margin={"r": MARGIN, "t": MARGIN, "l": MARGIN, "b": MARGIN})
