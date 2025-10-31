"""
tab_text/display.py
====================

Frontend logic for the "Text Serie" tab of the CSV Explorer app.

Responsibilities:
-----------------
• Display a dropdown of text columns detected in the dataset.
• Show summary statistics for the selected text column.
• Display a frequency bar chart using Altair.
• Display the top 20 most frequent text values.

Author: Shakib Ahmed Chowdhury (Student C)
Date: 2025-10-31
"""

import streamlit as st
import pandas as pd
import altair as alt

from tab_text.logics import get_text_columns, build_text_summary, top_frequencies


# ---------------------------------------------------------------------------
# MAIN DISPLAY FUNCTION
# ---------------------------------------------------------------------------

def display_tab_text_content(df: pd.DataFrame):
    """
    Main entry point for the Text Serie tab.
    Allows the user to explore textual columns of the dataset.

    Args:
        df (pd.DataFrame): DataFrame loaded from the uploaded CSV file.
    """

    st.header("📑 Text Series Analysis")

    # -----------------------------------------------------------------------
    # Detect all text columns
    # -----------------------------------------------------------------------
    text_columns = get_text_columns(df)

    if not text_columns:
        st.warning("⚠️ No text columns detected in this dataset.")
        return

    # -----------------------------------------------------------------------
    # Column selection box (dropdown)
    # -----------------------------------------------------------------------
    key_name = "selected_text_col"
    default_idx = 0
    current = st.session_state.get(key_name, text_columns[default_idx])

    selected_col = st.selectbox(
        "Which text column do you want to explore?",
        text_columns,
        index=text_columns.index(current) if current in text_columns else default_idx,
        key=key_name,
    )

    # -----------------------------------------------------------------------
    # Defensive checks to avoid KeyError or crash
    # -----------------------------------------------------------------------
    if selected_col is None:
        st.warning("Please select a text column to explore.")
        return

    if selected_col not in df.columns:
        st.error(f"Column '{selected_col}' not found in the dataset.")
        return

    # -----------------------------------------------------------------------
    # Extract and analyze the selected column
    # -----------------------------------------------------------------------
    series = df[selected_col]

    st.subheader(f"📊 Summary Statistics for '{selected_col}'")
    summary_df = build_text_summary(series)
    st.table(summary_df)

    # -----------------------------------------------------------------------
    # Frequency Chart (Altair)
    # -----------------------------------------------------------------------
    st.subheader("📈 Value Distribution")

    freq_df = top_frequencies(series, top_n=20)
    chart = (
        alt.Chart(freq_df)
        .mark_bar()
        .encode(
            x=alt.X("value:N", sort="-y", title="Text Values"),
            y=alt.Y("occurrence:Q", title="Occurrences"),
            tooltip=["value", "occurrence", "percentage"]
        )
        .properties(width=700, height=400)
    )
    st.altair_chart(chart, use_container_width=True)

    # -----------------------------------------------------------------------
    # Display Top 20 frequent values
    # -----------------------------------------------------------------------
    st.subheader("📋 Top 20 Most Frequent Values")
    st.dataframe(freq_df)
