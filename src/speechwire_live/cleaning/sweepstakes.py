import pandas as pd

COLUMNS = ["Headers", "Rows"]


def clean_sweepstakes(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    cleaned = df.copy()
    cleaned["Rows"] = cleaned["Rows"].apply(
        lambda rows: tuple(
            tuple("" if pd.isna(value) else value for value in row)
            for row in rows
        )
    )
    return cleaned[COLUMNS] if any(cleaned["Rows"]) else pd.DataFrame(columns=COLUMNS)
