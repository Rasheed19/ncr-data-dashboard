import folium
from folium import plugins
import pandas as pd
import leafmap.foliumap as leafmap
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from .processor import get_column_value_counts
from .definitions import Definition


def plot_bar_chart(
    data: pd.DataFrame, x_axis: str, y_axis: str, y_axis_title: str = None
):
    bar = px.bar(
        data_frame=data,
        x=x_axis,
        y=y_axis,
    )
    bar.update_layout(yaxis_title=y_axis if y_axis_title is None else y_axis_title)

    return bar.update_xaxes(tickangle=-45)


def plot_gauge_chart(value: int | float, title: str) -> go.Figure:
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title},
            gauge={
                "bar": {"color": "dodgerblue"},
            },
        )
    )


def plot_top_ten(top_ten: dict[str, pd.DataFrame]) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=len(top_ten),
        specs=[[{"type": "bar"}] * len(top_ten)],
    )
    for i, (k, v) in enumerate(
        top_ten.items(),
        start=1,
    ):

        fig.add_trace(
            go.Bar(
                x=v[k].values,
                y=v["Count"].values,
                name=k,
                showlegend=False,
                marker=dict(color=["dodgerblue"] * v[k].values.shape[0]),
            ),
            row=1,
            col=i,
        )

        fig.update_xaxes(title_text=k, row=1, col=i, tickangle=-90)
        fig.update_yaxes(
            title_text="Number of charge devices",
            row=1,
            col=1,
        )
        fig.update_layout(template="simple_white")

    return fig


def plot_accessibility(df: pd.DataFrame):
    fig = make_subplots(
        rows=1,
        cols=5,
        specs=[
            [
                {"type": "pie"},
            ]
            * 5
        ],
        subplot_titles=Definition.TAB_NAMES["Accessibility"],
    )
    for i, k in enumerate(
        Definition.TAB_NAMES["Accessibility"],
        start=1,
    ):

        df_count = get_column_value_counts(
            df=df,
            column_name=k,
            top_n=None,
        )

        fig.add_trace(
            go.Pie(
                labels=df_count[k].values,
                values=df_count["Count"].values,
                hole=0.6,
            ),
            row=1,
            col=i,
        )

    return fig


def get_map(
    df: pd.DataFrame,
) -> folium.Map:

    location_map = leafmap.Map(
        center=[df["Latitude"].mean(), df["Longitude"].mean()], zoom=10
    )

    # add geocoder
    plugins.Geocoder().add_to(location_map)

    for _, row in df.iterrows():
        tooltip_html = "<br>".join(
            [
                f"<b>{key}:</b> {value}"
                for key, value in row.to_dict().items()
                if str(value) != "nan"
            ]
        )
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            tooltip=tooltip_html,
        ).add_to(location_map)

    return location_map
