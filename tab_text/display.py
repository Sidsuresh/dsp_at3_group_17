# tab_text/display.py
from __future__ import annotations
import streamlit as st
import pandas as pd

from tab_text.logics import TextColumn


def display_tab_text_content(file_path: str | None = None, df: pd.DataFrame | None = None):
    """
    UI for the Text Series tab.

    Fixes included:
      - Stable 'selectbox' keyed via session_state so selection doesn't reset.
      - Avoids rebuilding options with a changing default on each rerun.
      - Works whether the app passes a loaded df or just a CSV file_path.
    """
    st.header("📝 Text Series Analysis")

    # Instantiate once per run and cache on session_state
    if "text_column_mgr" not in st.session_state:
        st.session_state["text_column_mgr"] = TextColumn(file_path=file_path, df=df)
    else:
        # Keep df/file_path up to date if caller re-runs with new values
        mgr: TextColumn = st.session_state["text_column_mgr"]
        if df is not None:
            mgr.df = df
        if file_path is not None:
            mgr.file_path = file_path

    mgr: TextColumn = st.session_state["text_column_mgr"]
    text_cols = mgr.find_text_cols()

    if not text_cols:
        st.warning("No text columns found in the dataset.")
        return

    # Persist selection across reruns with a unique key
    # Initialize the default selection exactly once
    if "text_col_selected" not in st.session_state:
        st.session_state["text_col_selected"] = text_cols[0]

    selected_col = st.selectbox(
        "Which text column do you want to explore?",
        options=text_cols,
        index=text_cols.index(st.session_state["text_col_selected"])
        if st.session_state["text_col_selected"] in text_cols
        else 0,
        key="text_col_selected",
        help="Choose a text column to see summary, an interactive bar chart, and top-20 frequent values.",
    )

    # Guard: nothing selected
    if not selected_col:
        st.info("Please select a text column to explore.")
        return

    # ----- Summary expander -----
    with st.expander("Text Column", expanded=True):
        try:
            summary_df = mgr.get_summary(selected_col)
            st.table(summary_df)
        except Exception as e:
            st.error(f"Failed to compute summary for '{selected_col}': {e}")
            return

    # ----- Chart expander -----
    with st.expander("Bar Chart", expanded=True):
        try:
            chart = mgr.bar_chart(selected_col)
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to render chart for '{selected_col}': {e}")

    # ----- Top frequent -----
    with st.expander("Most Frequent Values", expanded=True):
        try:
            top_df = mgr.frequent(selected_col, top_n=20)
            st.dataframe(top_df, use_container_width=True)
        except Exception as e:
            st.error(f"Failed to compute frequent values for '{selected_col}': {e}")
