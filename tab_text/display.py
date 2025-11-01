import streamlit as st

from tab_text.logics import TextColumn

def display_tab_text_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_text_content (function): Function that will instantiate tab_text.logics.TextColumn class, save it into Streamlit session state and call its tab_text.logics.TextColumn.find_text_cols() method in order to find all text columns.
    Then it will display a Streamlit select box with the list of text columns found.
    Once the user select a text column from the select box, it will call the tab_text.logics.TextColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_text.logics.TextColumn.get_summary() as a Streamlit Table
    - the graph from tab_text.logics.TextColumn.histogram using Streamlit.altair_chart()
    - the results of tab_text.logics.TextColumn.frequent using Streamlit.write
 
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file (optional)
    -> df (pd.DataFrame): Loaded dataframe (optional)

    --------------------
    Returns
    --------------------
    -> None

    """
    
    # Check if df is provided
    if df is None:
        st.warning("No valid CSV loaded. Please upload a CSV file to see analysis.")
        return
    
    # Instantiate TextColumn class and set it into Streamlit session state
    st.session_state["text_column"] = TextColumn(file_path=file_path, df=df)

    # Call find_text_cols() method to find all textual columns
    st.session_state.text_column.find_text_cols()

    # If no textual columns found, show message
    if not st.session_state.text_column.cols_list:
        st.warning("No textual columns found in the dataset.")
        return
    
    # Select box to choose numeric column
    selected_col = st.selectbox(
        label="Which textual column do you want to explore?",
        options=st.session_state.text_column.cols_list
    )

    # Set selected column in session state
    st.session_state["selected_text_col"] = selected_col

    if st.session_state.selected_text_col:
        st.session_state.text_column.set_data(st.session_state.selected_text_col)

        with st.expander("Textual Column Overview", expanded=True):

            st.subheader("Summary Information")
            # Display summary information as a table
            summary_df = st.session_state.text_column.get_summary()
            if summary_df is not None:
                summary_df = summary_df.astype(str)
                st.table(summary_df)

            st.subheader("Value Distribution")
             # Display histogram using altair_chart
            st.altair_chart(st.session_state.text_column.barchart, use_container_width = True)

            st.subheader("Most Frequent Values")
            # Display frequent values
            st.dataframe(st.session_state.text_column.frequent.astype(str), width='stretch')