# tab_text/logics.py
from __future__ import annotations
import pandas as pd
import numpy as np
import altair as alt
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TextColumn:
    """
    Manage text-column exploration and compute:
      - summary table
      - value frequency chart (Altair)
      - top-20 frequent values table
    """
    file_path: Optional[str] = None
    df: Optional[pd.DataFrame] = None
    cols_list: List[str] = field(default_factory=list)

    # ---------- lifecycle ----------

    def _ensure_df(self) -> pd.DataFrame:
        if self.df is not None:
            return self.df
        if self.file_path is None:
            raise ValueError("Either df or file_path must be provided.")
        # Lazy CSV load with dtype inference left to pandas
        return pd.read_csv(self.file_path)

    def find_text_cols(self) -> List[str]:
        """
        Detect text-like columns (object, string, category).
        """
        df = self._ensure_df()
        text_df = df.select_dtypes(include=["object", "string", "category"])
        self.cols_list = list(text_df.columns)
        return self.cols_list

    # ---------- computations for a selected column ----------

    def get_summary(self, column: str) -> pd.DataFrame:
        """
        Return a 2-column dataframe with the metrics specified in the assignment.
        All checks are done safely with NA handling.
        """
        s = self._ensure_df()[column]

        # Treat only strings for regex checks, but keep NA logic correct
        s_str = s.astype(str)

        # Metrics
        n_unique = s.nunique(dropna=True)
        n_missing = int(s.isna().sum())
        n_empty = int((s == "").sum(skipna=True))
        n_only_whitespace = int(s_str.str.fullmatch(r"\s+").fillna(False).sum())
        n_only_lower = int(s_str.str.fullmatch(r"[a-z]+").fillna(False).sum())
        n_only_upper = int(s_str.str.fullmatch(r"[A-Z]+").fillna(False).sum())
        n_only_alpha = int(s_str.str.fullmatch(r"[A-Za-z]+").fillna(False).sum())
        n_only_digits = int(s_str.str.fullmatch(r"\d+").fillna(False).sum())

        mode_val = None
        try:
            m = s.mode(dropna=True)
            if not m.empty:
                mode_val = m.iloc[0]
        except Exception:
            mode_val = None

        summary = pd.DataFrame(
            {
                "Description": [
                    "Number of Unique Values",
                    "Number of Rows with Missing Values",
                    "Number of Empty Rows",
                    "Number of Rows with Only Whitespaces",
                    "Number of Rows with Only Lowercases",
                    "Number of Rows with Only Uppercases",
                    "Number of Rows with Only Alphabet",
                    "Number of Rows with Only Digits",
                    "Mode Value",
                ],
                "Value": [
                    n_unique,
                    n_missing,
                    n_empty,
                    n_only_whitespace,
                    n_only_lower,
                    n_only_upper,
                    n_only_alpha,
                    n_only_digits,
                    mode_val,
                ],
            }
        )
        return summary

    def _clean_for_count(self, column: str) -> pd.Series:
        """
        Create a safe series for counting/charting:
          - NaN → "<MISSING>"
          - "" (empty) → "<EMPTY>"
          - whitespace-only → "<WHITESPACE>"
        """
        s = self._ensure_df()[column]
        s = s.astype(object)  # keep None/np.nan
        out = s.copy()

        # Replace NaN
        out = out.where(~pd.isna(out), other="<MISSING>")

        # Convert to string for empties/whitespace detection
        s_str = s.astype(str)
        mask_empty = s_str.eq("")
        mask_ws = s_str.str.fullmatch(r"\s+").fillna(False)

        out = out.astype(str)
        out[mask_empty] = "<EMPTY>"
        out[mask_ws] = "<WHITESPACE>"

        return out

    def bar_chart(self, column: str):
        """
        Return an Altair bar chart of value counts (descending).
        """
        series = self._clean_for_count(column)
        vc = series.value_counts(dropna=False)
        data = vc.reset_index()
        data.columns = [column, "Count"]

        chart = (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X("Count:Q", title="Count of Records"),
                y=alt.Y(f"{column}:N", sort="-x", title=column),
                tooltip=[alt.Tooltip(f"{column}:N"), alt.Tooltip("Count:Q")],
            )
            .properties(height=400)
        )
        return chart

    def frequent(self, column: str, top_n: int = 20) -> pd.DataFrame:
        """
        Return the top-N most frequent values with percentage.
        """
        series = self._clean_for_count(column)
        vc = series.value_counts(dropna=False)
        total = int(vc.sum())
        df_top = (
            vc.head(top_n)
            .reset_index()
            .rename(columns={"index": "value", 0: "occ"})
        )
        df_top.columns = ["value", "occ"]
        df_top["percentage"] = (df_top["occ"] / total).round(4)
        return df_top
