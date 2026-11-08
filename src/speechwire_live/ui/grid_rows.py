import json

import pandas as pd


def to_grid_rows(df: pd.DataFrame, numeric_columns: frozenset[str]) -> list[dict]:
    rows = df.copy()
    for column in numeric_columns & set(rows.columns):
        rows[column] = _numeric_if_lossless(rows[column])
    return json.loads(rows.to_json(orient="records"))


def _numeric_if_lossless(series: pd.Series) -> pd.Series:
    # Only convert when every non-blank value is a number, so text like "DQ" is never dropped.
    cleaned = series.replace("", pd.NA)
    numbers = pd.to_numeric(cleaned, errors="coerce")
    return numbers if numbers.notna().sum() == cleaned.notna().sum() else series
