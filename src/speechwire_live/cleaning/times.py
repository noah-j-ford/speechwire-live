import re

import numpy as np
import pandas as pd

from .standardization import Standardizer

COLUMNS = [
    "Event", "Section", "Spkr Pos.", "Rd", "Speaker Code", "Entry", "Team",
    "Time", "Seconds", "Rank", "Overtime", "Judge Code", "Judge",
]

# Minutes allowed per event; a 30 second grace period is added when checking.
TIME_LIMITS = {
    "IMP": 5, "N-IMP": 5,
    "EXT": 7, "N-EXT": 7,
    "ENT": 8, "N-ENT": 8, "POE": 8, "N-POE": 8,
    "DI": 10, "N-DI": 10, "HI": 10, "N-HI": 10, "POI": 10, "N-POI": 10,
    "INF": 10, "N-INF": 10, "OO": 10, "N-OO": 10,
    "DUO": 10, "N-DUO": 10, "Duet": 12,
    "OID": 15,
}


def process_time(time):
    time = time.replace(" ", "")
    if ":" not in time and time != "":
        if "." in time and len(time) <= 5:
            time = time.replace(".", ":")
        elif ";" in time and len(time) <= 5:
            time = time.replace(";", ":")
        elif len(time) in [3, 4]:
            time = time[:-2] + ":" + time[-2:]
        elif len(time) == 1 or time == "10":
            time = time + ":00"
    for char in ["ish", "forgot:(", "-", '"']:
        time = time.replace(char, "")
    if "." in time and len(time) >= 5:
        time = time.split(".")[0]
    if "!" in time:
        if time.index("!") + 1 != len(time):
            time = time.replace("!", "1")
        else:
            time = time.replace("!", "")
    return time


def convert_time_to_seconds(time):
    if time == 55 or time == "55":
        time = "0:55"
    try:
        seconds = int(time.split(":")[0]) * 60 + int(time.split(":")[1])
    except ValueError:
        seconds = np.nan
    except AttributeError:
        seconds = np.nan
    return seconds


def add_overtime_column(df):
    std = Standardizer()
    overtime_column, seconds_column = [], []
    for i in range(0, len(df)):
        event_name = df["Event"][i]
        seconds = convert_time_to_seconds(df["Time"][i])
        time_limit = np.inf  # events without a known limit are never flagged
        try:
            time_limit = TIME_LIMITS[event_name] * 60 + 30
        except KeyError:
            try:
                if event_name[-1] == " ":
                    event_name = event_name[:-1]
                    event_name = std.standardize_event_name_during_tournament(event_name)
                    time_limit = TIME_LIMITS[event_name] * 60 + 30
            except (KeyError, IndexError, TypeError):
                pass
        overtime_column.append("X" if seconds > time_limit else "")
        seconds_column.append(seconds)
    df["Overtime"] = overtime_column
    df["Seconds"] = seconds_column
    return df


def clean_up_formatting(df):
    std = Standardizer()
    df = df.copy()
    df["Event"] = df["Event"].apply(std.standardize_event_name_during_tournament)
    for replacement in [" Speech", " Team", " High School"]:
        df["Team"] = df["Team"].str.replace(replacement, "")
    entry_split = df.Entry.apply(lambda x: re.split(" ", x))
    df["Speaker Code"] = entry_split.apply(lambda x: x[0])
    df["Entry"] = entry_split.apply(
        lambda x: " ".join(x[1:]) if isinstance(x, list) and len(x) > 1 else ""
    )
    judge_split = df.Judge.apply(lambda x: re.split(" ", x))
    df["Judge Code"] = judge_split.apply(lambda x: x[0])
    df["Judge"] = judge_split.apply(
        lambda x: " ".join(x[1:]) if isinstance(x, list) and len(x) > 1 else ""
    )
    df = df.reset_index(drop=True)
    df["Time"] = df["Time"].apply(process_time)
    df = add_overtime_column(df)
    return df[COLUMNS].sort_values(["Event", "Team", "Entry", "Rd"]).reset_index(drop=True)
