import pandas as pd
from typing import cast


def transform_fred_data(raw_data: list, series_id: str) -> pd.DataFrame:
    df = pd.DataFrame(raw_data)
    if df.empty:
        print("Warning: Empty DataFrame! Nothing to transform.")
        return df
    df = df[["date", "value"]].copy()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    df = df.ffill()
    df["series_id"] = series_id
    df = df.dropna()
    print(f"Successfully transformed {len(df)} records for {series_id}.")

    return cast(pd.DataFrame, df)
