from dataclasses import dataclass
import pandas as pd
import numpy as np
from collections import Counter


@dataclass
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
