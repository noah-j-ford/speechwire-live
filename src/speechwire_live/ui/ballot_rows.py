from dataclasses import dataclass

import pandas as pd


def status_style(status: str) -> dict[str, str]:
    value = status.strip()
    if value == "IN":
        return {"backgroundColor": "#006400", "color": "#ffffff"}
    if value == "NOT STARTED":
        return {"backgroundColor": "#4a4a4a", "color": "#ffffff"}
    return {"backgroundColor": "#00ff00", "color": "#000000"}


@dataclass(frozen=True)
class SlotTable:
    slot: int
    title: str
    rows: list[dict]


def split_into_slot_tables(df: pd.DataFrame) -> list[SlotTable]:
    tables = []
    for slot, group in df.groupby("Slot", sort=True):
        rows = group[["Section", "Rm", "Judge", "Status"]].to_dict("records")
        for row in rows:
            row["statusStyle"] = status_style(row["Status"])
        tables.append(SlotTable(int(slot), str(group["Title"].iloc[0]), rows))
    return tables
