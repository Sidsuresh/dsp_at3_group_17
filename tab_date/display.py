import streamlit as st

from tab_date.logics import DateColumn

def display_tab_date_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_date_content (function): Function that will instantiate tab_date.logics.DateColumn class, save it into Streamlit session state and call its tab_date.logics.DateColumn.find_date_cols() method in order to find all datetime columns.
    Then it will display a Streamlit select box with the list of datetime columns found.
    Once the user select a datetime column from the select box, it will call the tab_date.logics.DateColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_date.logics.DateColumn.get_summary() as a Streamlit Table
    - the graph from tab_date.logics.DateColumn.histogram using Streamlit.altair_chart()
    - the results of tab_date.logics.DateColumn.frequent using Streamlit.write
 
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

    # Instantiate DateColumn class and set it into Streamlit session state
    st.session_state["date_column"] = DateColumn(file_path=file_path, df=df)

    # Call find_date_cols() method to find all datetime columns
    st.session_state.date_column.find_date_cols()

    # If no datetime columns found, show message
    if not st.session_state.date_column.cols_list:
        st.warning("No datetime columns found in the dataset.")
        return
    
    # Select box to choose datetime column
    selected_col = st.selectbox(
        label="Which datetime column do you want to explore?",
        options=st.session_state.date_column.cols_list
    )

    # Set selected column in session state
    st.session_state["selected_date_col"] = selected_col
    
    if st.session_state.selected_date_col:
        st.session_state.date_column.set_data(st.session_state.selected_date_col)

        with st.expander("Datetime Column Overview", expanded=True):

            # Display summary information as a table
            summary_df = st.session_state.date_column.get_summary()
            st.subheader("Summary Information")
            if summary_df is not None:
                st.table(summary_df)

            # Display barchart
            st.subheader("Barchart")
            st.altair_chart(st.session_state.date_column.barchart, use_container_width=True)

            # Display frequent values
            st.subheader("Most Frequent Values")
            st.dataframe(st.session_state.date_column.frequent, use_container_width=True)