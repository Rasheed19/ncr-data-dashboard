import io
from pathlib import Path

import pandas as pd
import requests

from utils.definitions import Definition


def load_csv_from_url(url: str) -> pd.DataFrame:
    req = requests.get(url).content

    return pd.read_csv(
        io.StringIO(req.decode("utf-8")),
        header=0,
        low_memory=False,
        lineterminator="\n",
    )


def clean_ncr_data() -> None:
    data = load_csv_from_url(
        "https://chargepoints.dft.gov.uk/api/retrieve/registry/format/csv"
    )
    data.columns = data.columns.str.lower()
    data_refined = data[list(Definition.COLUMNS_NEEDED.keys())]
    print(f"input dimension: {data_refined.shape}")

    # rectify incorrect lat and long
    data_refined = data_refined[
        data_refined["latitude"].between(*(49, 61), inclusive="both")
        & data_refined["longitude"].between(*(-8, 2), inclusive="both")
    ]

    # drop rows without charge device ID and county
    data_refined = data_refined.dropna(subset=["chargedeviceid"], axis=0)

    # remove trailing spaces from certain columns
    for col in [
        "county",
        "town",
        "devicemanufacturer",
        "deviceownername",
        "devicecontrollername",
        "locationtype",
        "connector1type",
        "connector2type",
        "connector3type",
    ]:
        data_refined[col] = data_refined[col].str.strip()

    # replace some bad county names
    data_refined["county"] = data_refined["county"].replace(
        Definition.MISSPELT_COUNTY_NAMES
    )

    # remove . from counties and towns
    # replace & with and
    # capitalize the beginning of every word in counties and towns
    for col in ["county", "town"]:
        data_refined[col] = data_refined[col].str.replace(
            '[.&`"]', lambda x: "and" if x.group() == "&" else "", regex=True
        )
        data_refined[col] = data_refined[col].str.title()

    # # remove couties and towns with numbers
    # for col_name in ["county", "town"]:
    #     data_refined = remove_rows_with_numbers(data_refined, col_name)

    # rename columns
    data_refined.rename(
        columns=Definition.COLUMNS_NEEDED,
        inplace=True,
    )

    zero_one_cols = [
        f"Connector {i} Tethered Cable" for i in range(1, 4)
    ] + Definition.TAB_NAMES["Accessibility"]
    data_refined[zero_one_cols] = data_refined[zero_one_cols].replace(
        {0: "No", 1: "Yes"}
    )

    print(f"output shape: {data_refined.shape}")
    print(f"{data.shape[0] - data_refined.shape[0]} rows removed")

    data_refined.to_csv(
        Path().resolve() / "data" / "ncr_data_cleaned.csv",
        index=False,
    )

    print("cleaning...done")
    print("<<<cleaned data saved in 'data' folder>>>")

    return None
