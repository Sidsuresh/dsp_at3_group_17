# AT3 - Collaborative Development of Data Explorer Web App

## Authors

Group 17 :

- Siddharth Suresh Nair (25548684)
- Saurav Parajuli (25143443)
- Sabrin Sultana (25762651)

## Description

This is an interactive **Streamlit**-based application that enables users to **upload, inspect, and analyse CSV datasets** through a simple and intuitive interface. It provides automated exploratory data analysis across four tabs:

1. **DataFrame Tab** – Displays dataset-level information such as shape, duplicates, missing values and memory usage, along with an interactive data preview.
2. **Numeric Series Tab** – Allows users to select a numeric column to view descriptive statistics, distributions and value frequency tables with an Altair histogram.
3. **Text Series Tab** – Enables exploration of textual data, including counts of unique, empty and whitespace-only values, along with an Altair bar chart and frequency table.
4. **Datetime Series Tab** – Provides insights into temporal data, including range, weekend/weekday counts and presence of specific reference dates, along with an Altair histogram.

### Challenges faced

- Handling mixed or incorrectly inferred data types (especially datetime columns).
- Ensuring UTC awareness in datetime comparisons and conversions.
- Maintaining synchronisation between Streamlit session states and uploaded data objects.
- Implementing modularized code across multiple team members while maintaining consistent coding style and logic.

### Future Improvements

- Automated data cleaning suggestions based on detected anomalies.
- Expanded support for large datasets through pagination or chunked reading.
- Additional visualizations such as box plots and correlation heatmaps.

## How to Setup

### Setup

- Clone the private GitHub repository:

```bash
git clone https://github.com/Sidsuresh/dsp_at3_group_17.git
cd dsp_at3_group17
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Verify installation:

```bash
streamlit --version
python --version
```

### Python version

- 3.9 or above (tested with Python 3.12)

### Packages and version

- -i https://pypi.org/simple
- altair==4.2.0
- pandas==2.0.3
- streamlit==1.13.0

## How to Run the Program

To start the Streamlit web app, run the following command in the project’s root directory:

```bash
streamlit run app/streamlit_app.py
```

Once launched, a browser window will open automatically at:
[STREAMLIT](http://localhost:8501/)

## Example Usage

1. **Upload** a CSV file from your local system.
2. **Navigate between the tabs** to explore:
   - **DataFrame tab:** Dataset overview
   - **Numeric tab:** Numerical data analysis
   - **Text tab:** Textual insights
   - **Datetime tab:** Temporal patterns

## Project Structure

```bash
dsp_at3_group17/
│
├── README.md                   # Project overview and setup instructions
├── requirements.txt            # Python package dependencies
│
├── app/
│   └── streamlit_app.py        # Main entry point for the Streamlit app
│
├── tab_df/
│   ├── display.py              # Display logic for dataset overview tab
│   └── logics.py               # Backend logic for computing dataset stats
│
├── tab_numeric/
│   ├── display.py              # Display logic for numeric column tab
│   └── logics.py               # Backend logic for numeric computations
│
├── tab_text/
│   ├── display.py              # Display logic for text column tab
│   └── logics.py               # Backend logic for text statistics
│
└── tab_date/
    ├── display.py              # Display logic for datetime column tab
    └── logics.py               # Backend logic for datetime computations
```

## Citations

- [Streamlit Documentation](https://docs.streamlit.io)
- [Altair Visualization Library](https://altair-viz.github.io)
- [Pandas Library](https://pandas.pydata.org)
