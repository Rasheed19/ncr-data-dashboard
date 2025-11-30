from dataclasses import dataclass

import folium
import leafmap.foliumap as leafmap
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from folium import plugins
from plotly.subplots import make_subplots


@dataclass(frozen=True)
class SummaryData:
    counties: list[str]
    total_chargers: int
    in_service_chargers: int
    county_with_most_chargers: str
    non_payment_chargers: int
    all_day_chargers: int
    top_ten: dict[str, pd.DataFrame]


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except Exception:
        return False


def get_column_value_counts(
    df: pd.DataFrame,
    column_name: str,
    top_n: int | None = 10,
) -> pd.DataFrame:
    column_count = df[column_name].value_counts()

    df_count = pd.DataFrame()
    df_count[column_name] = column_count.index
    df_count["Count"] = column_count.values
    df_count.dropna(axis=0, inplace=True)

    if top_n is None:
        return df_count

    df_count.sort_values(by="Count", ascending=False, inplace=True)

    return df_count.head(top_n)


def get_summary_data(df: pd.DataFrame) -> SummaryData:
    counties = df["County"].unique()
    counties = counties[~np.vectorize(is_number)(counties)].tolist()

    total_chargers = df.shape[0]
    in_service_chargers = df[df["Device Status"] == "In service"].shape[0]
    county_with_most_chargers = df.groupby(by="County").size().idxmax()
    non_payment_chargers = df[df["Payment Required"] == "No"].shape[0]
    all_day_chargers = df[df["24-hour Access"] == "Yes"].shape[0]

    column_names = [
        "County",
        "Location Type",
        "Device Manufacturer",
        "Device Owner",
        "Device Controller",
    ]
    top_ten = {k: get_column_value_counts(df, k, top_n=10) for k in column_names}

    return SummaryData(
        counties=counties,
        total_chargers=total_chargers,
        in_service_chargers=in_service_chargers,
        county_with_most_chargers=county_with_most_chargers,
        non_payment_chargers=non_payment_chargers,
        all_day_chargers=all_day_chargers,
        top_ten=top_ten,
    )


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
            title_text="Chargepoint count",
            row=1,
            col=1,
        )
        fig.update_layout(template="simple_white")

    return fig


def plot_accessibility(df: pd.DataFrame, access_columns: list[str]) -> go.Figure:
    fig = make_subplots(
        rows=1,
        cols=5,
        specs=[
            [
                {"type": "pie"},
            ]
            * 5
        ],
        subplot_titles=access_columns,
    )
    for i, k in enumerate(
        access_columns,
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
