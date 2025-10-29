import streamlit as st

from tab_num.logics import NumericColumn

def display_tab_num_content(file_path=None, df=None):
    """
    --------------------
    Description
    --------------------
    -> display_tab_num_content (function): Function that will instantiate tab_num.logics.NumericColumn class, save it into Streamlit session state and call its tab_num.logics.NumericColumn.find_num_cols() method in order to find all numeric columns.
    Then it will display a Streamlit select box with the list of numeric columns found.
    Once the user select a numeric column from the select box, it will call the tab_num.logics.NumericColumn.set_data() method in order to compute all the information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    - the results of tab_num.logics.NumericColumn.get_summary() as a Streamlit Table
    - the graph from tab_num.logics.NumericColumn.histogram using Streamlit.altair_chart()
    - the results of tab_num.logics.NumericColumn.frequent using Streamlit.write
 
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

    # Instantiate NumericColumn class and set it into Streamlit session state
    st.session_state["num_column"] = NumericColumn(file_path=file_path, df=df)

    # Call find_num_cols() method to find all numeric columns
    st.session_state.num_column.find_num_cols()

    # If no numeric columns found, show message
    if not st.session_state.num_column.cols_list:
        st.warning("No numeric columns found in the dataset.")
        return
    
    # Select box to choose numeric column
    selected_col = st.selectbox(
        label="Which numeric column do you want to explore?",
        options=st.session_state.num_column.cols_list
    )

    # Set selected column in session state
    st.session_state["selected_num_col"] = selected_col
    
    
    if st.session_state.selected_num_col:
        st.session_state.num_column.set_data(st.session_state.selected_num_col)

        with st.expander("Numeric Column Overview", expanded=True):

            # Display summary information as a table
            summary_df = st.session_state.num_column.get_summary()
            st.subheader("Summary Information")
            if summary_df is not None:
                st.table(summary_df)

            st.subheader("Feature Distribution")
             # Display histogram using altair_chart
            st.altair_chart(st.session_state.num_column.histogram, use_container_width = True)

            st.subheader("Most Frequent Values")
            # Display frequent values
            st.dataframe(st.session_state.num_column.frequent)





    



    