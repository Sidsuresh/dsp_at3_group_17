import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pandas")

import pandas as pd
import altair as alt

class DateColumn:
    """
    --------------------
    Description
    --------------------
    -> DateColumn (class): Class that manages a column from a dataframe of datetime data type

    --------------------
    Attributes
    --------------------
    -> file_path (str): Path to the uploaded CSV file (optional)
    -> df (pd.Dataframe): Pandas dataframe (optional)
    -> cols_list (list): List of columns names of dataset that are text type (default set to empty list)
    -> serie (pd.Series): Pandas serie where the content of a column has been loaded (default set to None)
    -> n_unique (int): Number of unique value of a serie (optional)
    -> n_missing (int): Number of missing values of a serie (optional)
    -> col_min (int): Minimum value of a serie (optional)
    -> col_max (int): Maximum value of a serie (optional)
    -> n_weekend (int): Number of times a serie has dates falling during weekend (optional)
    -> n_weekday (int): Number of times a serie has dates not falling during weekend (optional)
    -> n_future (int): Number of times a serie has dates falling in the future (optional)
    -> n_empty_1900 (int): Number of times a serie has dates equal to '1900-01-01' (optional)
    -> n_empty_1970 (int): Number of times a serie has dates equal to '1970-01-01' (optional)
    -> barchart (int): Altair barchart displaying the count for each value of a serie (optional)
    -> frequent (int): Dataframe containing the most frequest value of a serie (optional)

    """
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df
        self.cols_list = []
        self.serie = None
        self.n_unique = None
        self.n_missing = None
        self.col_min = None
        self.col_max = None
        self.n_weekend = None
        self.n_weekday = None
        self.n_future = None
        self.n_empty_1900 = None
        self.n_empty_1970 = None
        self.barchart = alt.Chart()
        self.frequent = pd.DataFrame(columns=['value', 'occurrence', 'percentage'])
    
    def find_date_cols(self):
        """
        --------------------
        Description
        --------------------
        -> find_date_cols (method): Class method that will load the uploaded CSV file as Pandas DataFrame and store it as attribute (self.df) if it hasn't been provided before.
        Then it will find all columns of datetime data type. If it can't find any datetime then it will look for all columns of text time. Then it will store the results in the relevant attribute (self.cols_list).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        # Load dataframe if not provided
        if self.df is None and self.file_path is not None:
            self.df = pd.read_csv(self.file_path)
        
        # Find datetime columns
        if self.df is not None:
            # Find columns with datetime data type
            self.cols_list = self.df.select_dtypes(include=['datetime64[ns]', 'datetime64[ns, UTC]']).columns.tolist()

            # If no datetime columns found, look for text columns that can be converted to datetime
            if not self.cols_list:
                for col in self.df.select_dtypes(include=['object']).columns:
                    try: 
                        parsed = pd.to_datetime(self.df[col], errors='coerce')
                        date_ratio = parsed.notna().mean()  # fraction of parsable dates
                        if date_ratio >= 0.8:
                            self.cols_list.append(col)
                    except (ValueError, TypeError):
                        continue
            


    def set_data(self, col_name):
        """
        --------------------
        Description
        --------------------
        --------------------
        Description
        --------------------
        -> set_data (method): Class method that sets the self.serie attribute with the relevant column from the dataframe and then computes all requested information from self.serie to be displayed in the Date section of Streamlit app 

        --------------------
        Parameters
        --------------------
        -> col_name (str): Name of the text column to be analysed

        --------------------
        Returns
        --------------------
        -> None
        """
        if self.df is not None and col_name in self.df.columns:
            # Set the serie attribute
            self.serie = self.df[col_name]

            # Convert serie to datetime
            self.convert_serie_to_date()

            # Compute all requested information
            self.set_unique()
            self.set_missing()
            self.set_min()
            self.set_max()
            self.set_weekend()
            self.set_weekday()
            self.set_future()
            self.set_empty_1900()
            self.set_empty_1970()
            self.set_barchart()
            self.set_frequent()
        

    def convert_serie_to_date(self):
        """
        --------------------
        Description
        --------------------
        -> convert_serie_to_date (method): Class method that convert a Pandas Series to datetime data type and store the results in the relevant attribute (self.serie).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """

        if not self.is_serie_none():
            # Convert serie to datetime
            self.serie = pd.to_datetime(self.serie, errors='coerce')
        

    def is_serie_none(self):
        """
        --------------------
        Description
        --------------------
        -> is_serie_none (method): Class method that checks if self.serie is empty or none 

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (bool): Flag stating if the serie is empty or not

        """
        # Check if serie is None or empty
        return self.serie is None or self.serie.empty
        

    def set_unique(self):
        """
        --------------------
        Description
        --------------------
        -> set_unique (method): Class method that computes the number of unique value of a serie and store the results in the relevant attribute(self.n_unique).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute number of unique values
            self.n_unique = self.serie.nunique()

    def set_missing(self):
        """
        --------------------
        Description
        --------------------
        -> set_missing (method): Class method that computes the number of missing value of a serie and store the results in the relevant attribute(self.n_missing).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute number of missing values
            self.n_missing = self.serie.isnull().sum()
        

    def set_min(self):
        """
        --------------------
        Description
        --------------------
        -> set_min (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_min).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute minimum value
            self.col_min = self.serie.min()
        

    def set_max(self):
        """
        --------------------
        Description
        --------------------
        -> set_max (method): Class method that computes the minimum value of a serie and store the results in the relevant attribute(self.col_max).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute maximum value
            self.col_max = self.serie.max()
        

    def set_weekend(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekend (method): Class method that computes the number of times a serie has dates falling during weekend and store the results in the relevant attribute(self.n_weekend).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute number of weekend dates
            self.n_weekend = self.serie.dt.dayofweek.isin([5, 6]).sum()
        

    def set_weekday(self):
        """
        --------------------
        Description
        --------------------
        -> set_weekday (method): Class method that computes the number of times a serie has dates not falling during weekend and store the results in the relevant attribute(self.n_weekday).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute number of weekday dates
            self.n_weekday = self.serie.dt.dayofweek.isin([0, 1, 2, 3, 4]).sum()
        

    def set_future(self):
        """
        --------------------
        Description
        --------------------
        -> set_future (method): Class method that computes the number of times a serie has dates falling in the future and store the results in the relevant attribute(self.n_future).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():

            # Compute number of future dates
            if self.serie.dt.tz is not None:
                # self.serie has timezone → make current_date timezone-aware
                current_date = pd.Timestamp.now(tz=self.serie.dt.tz)
            else:
                # self.serie has no timezone → make current_date naive
                current_date = pd.Timestamp.now().tz_localize(None)

            self.n_future = (self.serie > current_date).sum()
        
    
    def set_empty_1900(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1900 (method): Class method that computes the number of times a serie has dates equal to '1900-01-01' and store the results in the relevant attribute(self.n_empty_1900).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute number of times '1900-01-01' appears
            self.n_empty_1900 = (self.serie == pd.Timestamp('1900-01-01')).sum()
        

    def set_empty_1970(self):
        """
        --------------------
        Description
        --------------------
        -> set_empty_1970 (method): Class method that computes the number of times a serie has only digit characters and store the results in the relevant attribute(self.n_empty_1970).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute number of times '1970-01-01' appears
            self.n_empty_1970 = (self.serie == pd.Timestamp('1970-01-01')).sum()
        

    def set_barchart(self):  
        """
        --------------------
        Description
        --------------------
        -> set_barchart (method): Class method that computes the Altair barchart displaying the count for each value of a serie and store the results in the relevant attribute(self.barchart).

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute barchart
            self.barchart = alt.Chart(pd.DataFrame({'value': self.serie.dropna()})).mark_bar().encode(
                alt.X('value:T', title = self.serie.name),
                alt.Y('count()', title='Count of Records')
            ).properties(
                title='Barchart of Date Serie'
            )
        
      
    def set_frequent(self, end=20):
        """
        --------------------
        Description
        --------------------
        -> set_frequent (method): Class method that computes the Dataframe containing the most frequest value of a serie and store the results in the relevant attribute(self.frequent).

        --------------------
        Parameters
        --------------------
        -> end (int):
            Parameter indicating the maximum number of values to be displayed

        --------------------
        Returns
        --------------------
        -> None

        """
        if not self.is_serie_none():
            # Compute frequent values
            freq_series = self.serie.value_counts(dropna=True).head(end)
            # Compute total count for percentage calculation
            total_count = len(self.serie.dropna())
            # Create dataframe for frequent values
            self.frequent = pd.DataFrame({
                'value': freq_series.index,
                'occurrence': freq_series.values,
                'percentage': (freq_series.values / total_count * 100).round(2)
            })

        

    def get_summary(self):
        """
        --------------------
        Description
        --------------------
        -> get_summary (method): Class method that formats all requested information from self.serie to be displayed in the Overall section of Streamlit app as a Pandas dataframe with 2 columns: Description and Value

        --------------------
        Parameters
        --------------------
        -> None

        --------------------
        Returns
        --------------------
        -> (pd.DataFrame): Formatted dataframe to be displayed on the Streamlit app

        """
        if not self.is_serie_none():
            # Create summary dataframe
            data = {
                'Description': [
                    'Number of Unique Values',
                    'Number of Rows with Missing Values',
                    'Number of Weekend Dates',
                    'Number of Weekday Dates',
                    'Number of Dates in Future',
                    "Number of '1900-01-01' Dates",
                    "Number of '1970-01-01' Dates",
                    'Minimum Value',
                    'Maximum Value'
                ],
                'Value': [
                    f"{int(self.n_unique)}",
                    f"{int(self.n_missing)}",
                    f"{int(self.n_weekend)}",
                    f"{int(self.n_weekday)}",
                    f"{int(self.n_future)}",
                    f"{int(self.n_empty_1900)}",
                    f"{int(self.n_empty_1970)}",
                    f"{self.col_min}",
                    f"{self.col_max}"
                ]
            }
            summary_df = pd.DataFrame(data)
            return summary_df
        
