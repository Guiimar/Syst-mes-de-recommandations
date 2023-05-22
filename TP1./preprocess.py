'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

dataframe_process = pd.read_csv('./assets/data/arbres.csv')
def convert_dates(dataframe):
    '''
        Converts the dates in the dataframe to datetime objects.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with datetime-formatted dates.
    '''
    dataframe['Date_Plantation']=pd.to_datetime(dataframe['Date_Plantation'])
    return dataframe

def filter_years(dataframe, start, end):
    '''
        Filters the elements of the dataframe by date, making sure
        they fall in the desired range.

        Args:
            dataframe: The dataframe to process
            start: The starting year (inclusive)
            end: The ending year (inclusive)
        Returns:
            The dataframe filtered by date.
    '''
    start_date=pd.to_datetime(start, format='%Y')
    end_date=pd.to_datetime(end, format='%Y')+pd.offsets.YearEnd()
    dataframe=dataframe[(dataframe['Date_Plantation']>=start_date)&(dataframe['Date_Plantation']<=end_date)]
    return dataframe
 
def summarize_yearly_counts(dataframe):
    '''
        Groups the data by neighborhood and year,
        summing the number of trees planted in each neighborhood
        each year.

        Args:
            dataframe: The dataframe to process
        Returns:
            The processed dataframe with column 'Counts'
            containing the counts of planted
            trees for each neighborhood each year.
    '''
    dataframe=dataframe.groupby([pd.Grouper(key='Arrond_Nom'), pd.Grouper(key='Date_Plantation',freq='Y')]).size().reset_index(name='Counts')
    return dataframe


def restructure_df(yearly_df):
    '''
        Restructures the dataframe into a format easier
        to be displayed as a heatmap.

        The resulting dataframe should have as index
        the names of the neighborhoods, while the columns
        should be each considered year. The values
        in each cell represent the number of trees
        planted by the given neighborhood the given year.

        Any empty cells are filled with zeros.

        Args:
            yearly_df: The dataframe to process
        Returns:
            The restructured dataframe
    '''
    yearly_df['Year'] = yearly_df['Date_Plantation'].dt.year
    yearly_df = yearly_df.pivot(index='Arrond_Nom',columns='Year',values='Counts').fillna(0)
    
    return yearly_df

def get_daily_info(dataframe, arrond, year):
    '''
        From the given dataframe, gets
        the daily amount of planted trees
        in the given neighborhood and year.

        Args:
            dataframe: The dataframe to process
            arrond: The desired neighborhood
            year: The desired year
        Returns:
            The daily tree count data for that
            neighborhood and year.
    '''
    filtered_df = dataframe[(dataframe['Arrond'] == arrond) & (dataframe['Date_Plantation'].dt.year == year)]
    daily_count = filtered_df.groupby(pd.Grouper(key='Date_Plantation', freq='D')).size().reset_index(name='Counts')
    dataframe = daily_count.set_index('Date_Plantation').resample('D').asfreq().fillna(0).reset_index()
    return dataframe

#TEST
dataframe_date=convert_dates(dataframe_process)
print(convert_dates(dataframe_process)['Date_Plantation'].dtype)
Summarize=summarize_yearly_counts(dataframe_date)
print(Summarize)
print(restructure_df(Summarize))
print(get_daily_info(dataframe_date,1,2009))
