"""
tab_text/display.py
====================
Front-end Streamlit component for the Text Serie tab.
It lets the user:
1. Select a text column
2. View summary statistics
3. See a frequency bar chart
4. Inspect the top 20 most frequent values

Author: Sabrin Sultana (Student C)
"""

import streamlit as st
import pandas as pd
import altair as alt

from tab_text.logics import get_text_columns, build_text_summary, top_frequencies


# ---------------------------------------------------------------------------
# Streamlit Rendering
# ---------------------------------------------------------------------------

def display_tab_text_content(df: pd.DataFrame) -> None:
    """
    Render Text Serie tab content inside the Streamlit application.

    Args:
        df (pd.DataFrame): The uploaded dataset stored in session_state["df"].
    """
    st.header("Text Serie")

    text_columns = get_text_columns(df)
    if not text_columns:
        st.warning("No text columns detected in this dataset.")
        return

    # persist previous selection for better UX
    key_name = "selected_text_col"
    default_idx = 0
    current = st.session_state.get(key_name, text_columns[default_idx])

    selected_col = st.selectbox(
        "Which text column do you want to explore",
        text_columns,
        index=text_columns.index(current) if current in text_columns else default_idx,
        key=key_name,
    )

if selected_col is None:
    st.warning("Please select a text column to explore.")
    return

if selected_col not in df.columns:
    st.error(f"Column '{selected_col}' not found in the dataset.")
    return  

series = df[selected_col]

    # -----------------------------------------------------------------------
    # 1️⃣ Summary Table
    # -----------------------------------------------------------------------
    with st.expander("Text Column", expanded=True):
        st.caption("Summary statistics for selected text column.")
        summary_df = build_text_summary(series)
        st.table(summary_df)

    # -----------------------------------------------------------------------
    # 2️⃣ Frequency Bar Chart
    # -----------------------------------------------------------------------
    st.subheader("Bar Chart")
    freq = series.value_counts(dropna=False).reset_index()
    freq.columns = [selected_col, "Count"]

    chart = (
        alt.Chart(freq)
        .mark_bar(color="#4C78A8")  # maintain blue tone from professor’s theme
        .encode(
            x=alt.X(f"{selected_col}:N", sort="-y", title=selected_col),
            y=alt.Y("Count:Q", title="Count of Records"),
            tooltip=[selected_col, "Count"],
        )
        .properties(width="container", height=420)
    )
    st.altair_chart(chart, use_container_width=True)

    # -----------------------------------------------------------------------
    # 3️⃣ Top-20 Frequency Table
    # -----------------------------------------------------------------------
    st.subheader("Most Frequent Values")
    top20_df = top_frequencies(series, top_n=20)
    st.dataframe(top20_df, use_container_width=True)
