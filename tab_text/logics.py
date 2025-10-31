"""
tab_text/logics.py
===================
This module contains all backend logic used by the Text Serie tab.
It analyses textual (object/string) columns and produces:
- Summary statistics
- Frequency tables

Author: Sabrin Sultana (Student C)
"""

import pandas as pd
from typing import List


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------

def get_text_columns(df: pd.DataFrame) -> List[str]:
    """
    Identify all text-based columns in a DataFrame.

    Args:
        df (pd.DataFrame): The uploaded dataset.

    Returns:
        List[str]: Column names with dtype 'object' or string-like.
    """
    return [
        col for col in df.columns
        if df[col].dtype == "object" or pd.api.types.is_string_dtype(df[col])
    ]


def _convert_to_string(series: pd.Series) -> pd.Series:
    """
    Convert any Series to pandas StringDtype safely, preserving NaN.

    Args:
        series (pd.Series): Input column.

    Returns:
        pd.Series: Series converted to StringDtype.
    """
    if pd.api.types.is_string_dtype(series):
        return series.astype("string")
    return series.astype("string", errors="ignore")


# ---------------------------------------------------------------------------
# Core Analysis Functions
# ---------------------------------------------------------------------------

def build_text_summary(series: pd.Series) -> pd.DataFrame:
    """
    Compute all summary metrics for a text column.

    Metrics returned follow professor’s assignment specification:
    - Number of Unique Values
    - Number of Rows with Missing Values
    - Number of Empty Rows
    - Number of Rows with Only Whitespaces
    - Number of Rows with Only Lowercases
    - Number of Rows with Only Uppercases
    - Number of Rows with Only Alphabet
    - Number of Rows with Only Digits
    - Mode Value

    Args:
        series (pd.Series): Text column selected by the user.

    Returns:
        pd.DataFrame: Two-column summary table: Description | Value
    """
    s = _convert_to_string(series)
    total = len(s)
    missing = s.isna().sum()
    s_filled = s.fillna("")

    # pattern checks
    empty = (s_filled == "").sum()
    whitespace_only = s_filled.str.fullmatch(r"\s+").sum()
    lower_only = s_filled.str.fullmatch(r"[a-z]+").sum()
    upper_only = s_filled.str.fullmatch(r"[A-Z]+").sum()
    alpha_only = s_filled.str.fullmatch(r"[A-Za-z]+").sum()
    digits_only = s_filled.str.fullmatch(r"\d+").sum()

    # mode value
    mode_val = "N/A"
    mode_series = s.dropna().mode()
    if not mode_series.empty:
        mode_val = str(mode_series.iloc[0])

    summary = [
        ("Number of Unique Values", int(s.nunique(dropna=True))),
        ("Number of Rows with Missing Values", int(missing)),
        ("Number of Empty Rows", int(empty)),
        ("Number of Rows with Only Whitespaces", int(whitespace_only)),
        ("Number of Rows with Only Lowercases", int(lower_only)),
        ("Number of Rows with Only Uppercases", int(upper_only)),
        ("Number of Rows with Only Alphabet", int(alpha_only)),
        ("Number of Rows with Only Digits", int(digits_only)),
        ("Mode Value", mode_val),
    ]

    return pd.DataFrame(summary, columns=["Description", "Value"])


def top_frequencies(series: pd.Series, top_n: int = 20) -> pd.DataFrame:
    """
    Generate frequency table for top N values of a text column.

    Args:
        series (pd.Series): Text column.
        top_n (int, optional): Number of top items to return. Default = 20.

    Returns:
        pd.DataFrame: Columns [value, occurrence, percentage]
    """
    total = len(series)
    counts = series.value_counts(dropna=False).head(top_n)
    df_out = pd.DataFrame({
        "value": counts.index.astype(str),
        "occurrence": counts.values,
        "percentage": (counts.values / total).round(4),
    })
    return df_out
