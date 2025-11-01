import streamlit as st

from tab_df.logics import Dataset

def display_tab_df_content(file_path):
    """
    --------------------
    Description
    --------------------
    -> display_overall_df (function): Function that will instantiate tab_df.logics.Dataset class, save it into Streamlit session state and call its tab_df.logics.Dataset.set_data() method in order to compute all information to be displayed.
    Then it will display a Streamlit Expander container with the following contents:
    1. the results of tab_df.logics.Dataset.get_summary() as a Streamlit Table
    2. the results of tab_df.logics.Dataset.table using Streamlit.write()
    Finally it will display a second Streamlit Expander container with a slider to select the number of rows to be displayed and a radio button to select the method (head, tail, sample).
    According to the values selected on the slider and radio button, display the subset of the dataframe accordingly using Streamlit.dataframe
    
    --------------------
    Parameters
    --------------------
    -> file_path (str): File path to uploaded CSV file

    --------------------
    Returns
    --------------------
    -> None
    
    """
    
    # Instantiate Dataset class and set it into Streamlit session state
    st.session_state["dataset"] = Dataset(file_path=file_path)

    # Call set_df() method to load the dataframe
    st.session_state.dataset.set_df()

    if st.session_state.dataset.df is None:
        st.warning("No valid CSV loaded. Please upload a CSV file to see analysis.")
        return
    
    # Call set_data() method to compute all information
    st.session_state.dataset.set_data()

    with st.expander("DataFrame Overview", expanded=True):
        # Display summary information as a table
        st.subheader("Summary Information")
        summary_df = st.session_state.dataset.get_summary()
        st.table(summary_df)

        # Display column information
        st.subheader("Columns Information")
        st.table(st.session_state.dataset.table)
    
    with st.expander("Explore Dataframe", expanded=True):
        
        # Slider to select number of rows
        n_rows = st.slider(label = "Select the number of rows to display", min_value = 5, max_value = 50)

        # Radio button to select method
        method = st.radio(label = "Exploration Method", options = ["Head", "Tail", "Sample"])

        if method == "Head":
            # st.write("Top Rows from the Dataframe")
            st.dataframe(st.session_state.dataset.get_head(n_rows), use_container_width=True)
        elif method == "Tail":
            # st.write("Bottom Rows from the Dataframe")
            st.dataframe(st.session_state.dataset.get_tail(n_rows), use_container_width=True)
        elif method == "Sample":
            # st.write("Random Sample of Rows from the Dataframe")
            st.dataframe(st.session_state.dataset.get_sample(n_rows), use_container_width=True)
